import re
import json
import datetime
from scrapy.selector import Selector
try:
	from scrapy.spider import Spider
except:
	from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http.request import Request
from websites import FlipKartScrapper
from websites import SnapDealScrapper
from websites import AmazonScrapper
import os.path
import csv
import logging



class ImageScrapper(CrawlSpider):
	
	name = "ImageScrapper"
	outputFilePath = "/home/stratdecider/ScrapperOutput/ImageScrappers/"
	def start_requests(self):
		AppProducts = self.getImageURLS()
		# AppProducts = [['Blackberry', 'Blackberry Q10', 'http://www.snapdeal.com/product/lg-google-nexus-5-16/848745269'],
		# ['Apple','iPhone 5','http://www.flipkart.com/apple-iphone-5/p/itme7zmtvp6utrxz?pid=MOBDKMJEXGZWTTTJ'],
		# ['Micromax', 'Canvas Doodle 3 A102',"http://www.amazon.in/Micromax-Canvas-Doodle-A102-White/dp/B00P2HZDOE"]]

		#start_urls = ["http://www.snapdeal.com/product/blackberry-q10/1368483"]
		for items in AppProducts:
			brand = items[0]
			productName = items[1]
			productName = productName.strip()
			url = items[2]
			outputFilePath = self.outputFilePath + productName + ".jpg"
			if not os.path.isfile(outputFilePath) :
				yield Request(url, self.parse, meta = {'outputFilePath': outputFilePath})

	def parse(self,response):
		outputFilePath = response.meta['outputFilePath']
		#+ "/" + dateStr + "/" 
		if ("flipkart" in response.url):
			flipKartScrapper = FlipKartScrapper()
			flipKartScrapper.downloadProductList(response, outputFilePath)
		if ("snapdeal" in response.url):
			snapdealScrapper = SnapDealScrapper()
			snapdealScrapper.downloadProductList(response, outputFilePath)
		if ("amazon" in response.url):
			amazonScrapper = AmazonScrapper()
			amazonScrapper.downloadProductList(response, outputFilePath)

	def getImageURLS(self):
		inputFile = "/home/stratdecider/ScrapperInput/ImageScrapper/ImageScrapper.csv"
		fileObj = open(inputFile)
		ProductList = []
		reader = csv.reader(fileObj)

		for row in reader:
			brand = row[1]
			productName = row[2]
			pdURL = row[6]
			if not pdURL:
				pdURL = row[10]
				
			if not pdURL:
				pdURL = row[12]
			if not pdURL:
				print productName
			else:
				ProductList.append([brand,productName,pdURL])

		return ProductList
