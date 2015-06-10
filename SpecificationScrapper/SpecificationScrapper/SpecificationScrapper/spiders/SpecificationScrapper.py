import re
import json
import datetime
import json,os
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
class SpecificationScrapper(CrawlSpider):
	
	name = "SpecificationScrapper"
	outputFilePath = "/home/stratdecider/ScrapperOutput/SpecificationScrapper/"
	snapDealMatchFileName = "/home/stratdecider/ScrapperInput/SpecificationScrapper/SpecificationMatchSnapDeal.csv"
	amazonMatchFileName = "/home/stratdecider/ScrapperInput/SpecificationScrapper/SpecificationMatchAmazon.csv"
	def start_requests(self):
		AppProducts = self.getURLS()
		# AppProducts = [['Blackberry', 'Blackberry Q11', 'http://www.snapdeal.com/product/lg-google-nexus-5-16/848745269']
		# ,['Apple','iPhone 54','http://www.flipkart.com/apple-iphone-5/p/itme7zmtvp6utrxz?pid=MOBDKMJEXGZWTTTJ'],
		#AppProducts = [['Micromax', 'Canvas Doodle 33 A102',"http://www.amazon.in/Micromax-Canvas-Doodle-A102-White/dp/B00P2HZDOE"]]
		snapDealMatch = self.createMatchDict(self.snapDealMatchFileName)
		amazonMatch = self.createMatchDict(self.amazonMatchFileName)
		#start_urls = ["http://www.snapdeal.com/product/blackberry-q10/1368483"]
		for items in AppProducts:
			brand = items[0]
			productName = items[1]
			productName = productName.replace(brand+ " ", "")
			url = items[2]

			outputFilePath = self.outputFilePath + productName + ".json"

			if not os.path.isfile(outputFilePath):
				print url
				yield Request(url, self.parse, meta = {'outputFilePath': outputFilePath,'productName':productName, 'brand':brand,'snapDealMatch':snapDealMatch, 'amazonMatch':amazonMatch})

	def parse(self,response):
		outputFilePath = response.meta['outputFilePath']
		productName = response.meta['productName']
		brand = response.meta['brand']
		snapDealMatch = response.meta['snapDealMatch']
		amazonMatch = response.meta['amazonMatch']
		print response.url
		
		
		productJSON = {}
		
		
		if ("flipkart" in response.url):
			flipKartScrapper = FlipKartScrapper()
			productJSON = flipKartScrapper.downloadProductDetails(response, productName)
		if ("snapdeal" in response.url):
			snapdealScrapper = SnapDealScrapper()
			productJSON = snapdealScrapper.downloadProductDetails(response, productName, brand, snapDealMatch)
		if ("amazon" in response.url):
			amazonScrapper = AmazonScrapper()
			productJSON = amazonScrapper.downloadProductDetails(response, productName, brand, amazonMatch)
		

		self.saveOutPut(productJSON, outputFilePath)

	def getURLS(self):
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

	def saveOutPut(self,productJSON, filePath):
		with open(filePath, 'a+') as fManager:
			json.dump(productJSON, fManager, sort_keys = True, indent = 4, ensure_ascii=False)

	def createMatchDict(self, fileName):
		fileObj = open(fileName)
		ProductList = []
		MatchDict = {}
		reader = csv.reader(fileObj)
		for row in reader:
			if row[2]:
				try:
					MatchDict[row[0]] = [row[1],row[2]]
				except:
					print row[0]
		return MatchDict

