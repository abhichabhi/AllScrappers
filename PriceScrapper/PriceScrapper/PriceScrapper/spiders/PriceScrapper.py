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
import os
import os.path
import csv
import logging
import csv
class PriceScrapper(CrawlSpider):
	name = "PriceScrapper"
	outputFilePath = "/home/stratdecider/ScrapperOutput/PriceScrapper/PriceScrapper.csv"
	header = ["Brand","Model Name","ECommerceName","ECommercePrice","ECommerceStatus","ECommercePdURL"]
	def start_requests(self):
		self.writeToFile(self.header, self.outputFilePath)
		AppProducts = self.getImageURLS()
		# AppProducts = [['Blackberry', 'Blackberry Q10', 'http://www.snapdeal.com/product/lg-google-nexus-5-16/848745269'],
		# ['Adcom','Thunder A430 IPS','http://www.flipkart.com/adcom-thunder-a430-ips/p/itmdw88fabbdjcn2?pid=MOBDW88FHMNYPTBD'],
		# ['Micromax', 'Canvas Doodle 3 A102 (White, 8GB)',"http://www.amazon.in/Apple-iPhone-5s-Gold-16GB/dp/B00FXLCD38"]]
		# AppProducts = [['Micromax', 'Canvas Doodle 3 A102 (White, 8GB)',"http://www.amazon.in/BlackBerry-9720-Black/dp/B00FF4ZHCC"]]

		#start_urls = ["http://www.snapdeal.com/product/blackberry-q10/1368483"]
		for items in AppProducts:
			brand = items[0]
			productName = items[1]
			url = items[2]
			outputFilePath = self.outputFilePath + productName + ".jpg"
			yield Request(url, self.parse, meta = {'outputFilePath': outputFilePath,'productName':productName, 'brand':brand})
			

	def parse(self,response):
		outputFilePath = response.meta['outputFilePath']
		productName = response.meta['productName']
		brand = response.meta['brand']
		price = 0
		stock = 1
		csvRow = []
		eComName = ""
		if ("flipkart" in response.url):
			flipKartScrapper = FlipKartScrapper()
			price, stock = flipKartScrapper.getPrice(response, outputFilePath)
			eComName = "flipkart"
		if ("snapdeal" in response.url):
			snapdealScrapper = SnapDealScrapper()
			price, stock = snapdealScrapper.getPrice(response, outputFilePath)
			eComName = "snapdeal"
		if ("amazon" in response.url):
			amazonScrapper = AmazonScrapper()
			price, stock = amazonScrapper.getPrice(response, outputFilePath)
			eComName = "amazon"
		csvRow = [brand,productName,eComName,price,stock,response.url]
		self.writeToFile(csvRow, self.outputFilePath)
		

	def getImageURLS(self):
		inputFile = "/home/stratdecider/ScrapperInput/ImageScrapper/ImageScrapper.csv"
		fileObj = open(inputFile)
		ProductList = []
		reader = csv.reader(fileObj)

		for row in reader:
			brand = row[1]
			productName = row[2]
			FpdURL = row[6]
			SpdURL = row[12]
			ApdURL = row[10]
			if FpdURL:
				ProductList.append([brand,productName,FpdURL])
			if SpdURL:
				ProductList.append([brand,productName,SpdURL])
			if ApdURL:
				ProductList.append([brand,productName,ApdURL])

		return ProductList

	def writeToFile(self,row,destFile):
		if not os.path.exists(os.path.dirname(destFile)):
			os.makedirs(os.path.dirname(destFile))
			# with open(destFile, 'a') as outcsv:
			# 	writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			# 	writer.writerow(self.header)
            #configure writer to write standart csv file
                
		with open(destFile, 'a') as outcsv:
			print row
			writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(row)
            # with open(filename, 'a') as outcsv:
            # #configure writer to write standart csv file
            #     writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')           
            #     writer.writerow(self.amazon_HeadingList)