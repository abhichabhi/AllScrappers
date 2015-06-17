import sys, re, os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy.http import Request
from websites import FlipkartScrapper
from websites import AmazonScrapper
from time import sleep
import itertools
import csv
import logging
import datetime

class ReviewScrapper(CrawlSpider):
    name = "ReviewScrapper"
    destFilePath = "/home/stratdecider/ScrapperOutput/ReviewScrapper/PhoneReviews/"
    ratingDestFile = "/home/stratdecider/ScrapperOutput/ReviewScrapper/PhoneRating/"
    ReviewLinksFile = "/home/stratdecider/ScrapperInput/ReviewScrapper/ReviewScapper.csv"
    
    def start_requests(self):
        #rowList = [["Samsung", "Samsung Galaxy S5", "http://www.flipkart.com/samsung-galaxy-s5/product-reviews/ITME3H4RJPV7BQ5D","http://www.amazon.in/product-reviews/B00K3FZ72S","http://www.amazon.in/Samsung-Galaxy-S5-Shimmery-White/product-reviews/B00JB6RXBI"]]
        rowList = self.getListFromCSV(self.ReviewLinksFile)
        for row in rowList:
            product = row[:2]
            Links = row[2:]
            Links = list(set(Links))
            Links =  [x for x in Links if x != ""]
            brand = row[0]
            productName = row[1]
            outputFilePath = self.destFilePath + productName + ".csv"
            if  os.path.isfile(outputFilePath):
                continue;
            ulrList = Links
            print ulrList
            for url in ulrList:
                if url:
                    try:
                        yield Request(url, meta={"brand":brand, "productName" : productName})#,meta={'db':db,'dbOperation':dbOperation,'cursor':cursor,'product_ecom':product_ecom})
                    except:
                        pass
    
            
    def parse(self,response):
        pDetailList = []
        reviewPageList = []
        brand = response.meta["brand"]
        productName = response.meta["productName"]
        destFilePath = self.destFilePath + productName + ".csv"
        ratingDestFile = self.ratingDestFile + productName + ".csv"
        if ("amazon" in response.url):
            amazonScrapper = AmazonScrapper()
            pDetailList, reviewPageList = amazonScrapper.getProductDetailsList(response)
        if ("flipkart" in response.url):
            flipKartScrapper = FlipkartScrapper()
            pDetailList,reviewPageList = flipKartScrapper.getProductDetailsList(response)
        self.writeToFile([response.url], ratingDestFile)
        self.writeToFile(pDetailList[2], ratingDestFile)
        # print pDetailList
        self.writeToFile([response.url], destFilePath)
        for reviewList in reviewPageList:
            self.writeToFile(reviewList, destFilePath)
        
    def getListFromCSV(self, filename):
        profileLinks = []
        with open(filename, 'r') as f:
            readColumns = (csv.reader(f, delimiter=','))
            iter = 0
            for row in readColumns:
                profileLinks.append(row)
            return profileLinks

    def writeToFile(self,row,filename):
        fileName = filename
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))
            # with open(filename, 'a') as outcsv:
            # #configure writer to write standart csv file
            #     writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')            
            #     writer.writerow(self.amazon_HeadingList)
            
        with open(filename, 'a') as outcsv:   
            #configure writer to write standart csv file
            print list
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')            
            writer.writerow(row)
    
                
                
                