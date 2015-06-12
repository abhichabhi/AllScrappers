from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy.http import Request
import requests
import json
import re
import ast,time
class FlipkartScrapper():
    name = "Flipkart"
    monthDict = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11, "december":12}
    
    Headin_Flag = 1
    headingList = ['ProductUrl', 'ProductName', 'SellingPrice','ProductQuantity', 'Productrating', 'ProductMerchantInfo','Availability','Discount','DeliveryCharge']
    def getProductDetailsList(self,response):
        print response.url
        hxs = HtmlXPathSelector(response)
        pDetailList = []
        
        totalpaging = self.getPagination(hxs)
        try:
            totalpaging = totalpaging/10 +2
        except:
            totalpaging = 0
        print totalpaging
        reviewPageList = []
        #totalpaging = min(totalpaging,30)
        print totalpaging
        time.sleep(10)
        
        for iterator in range(0,totalpaging+1):
            page = iterator*10
            pageURL = response.url + "&start=" + str(page)
            print pageURL
            respRating = requests.get(url=pageURL, timeout=20)
            respRatingText = respRating.text
            respRatingText = respRatingText.encode('utf-8', 'ignore')
            ratingHXS = HtmlXPathSelector(text = respRatingText)
            
            #print ratingHXS.select("//div[@class='reviewText']/text()").extract()
            reviewPageList = reviewPageList + self.getReviewListOfPage(ratingHXS)
        
        pDetailList.append(response.url)
        pDetailList.append(self.getProductName(hxs)) #Product Name
        pDetailList.append(self.getRatingList(hxs))  #Rating List
        #pDetailList.append(self.getLastReviewRatingList(hxs))
        #pDetailList.append(self.getReviewJSON(self.getLatestReviewDate(hxs), self.getLatestReviewText(hxs)))
        
        
        
       
        return pDetailList,reviewPageList
        
    def getProductName(self,hxs):
        pName = hxs.select("//h1[@class='title']/text()").extract()[0]
        pName = self.textCleaner(pName)
        return pName
    
    def getReviewListOfPage(self,hxs):
        reviewpageList = []
        reviewDIVlist = hxs.select("//div[@class='review-list']/div").extract()
        
        for reviewDiv in reviewDIVlist:
            reviewDivItemList = []
            reviewDivHXS = HtmlXPathSelector(text = reviewDiv)
            reviewText = reviewDivHXS.select("//span[@class='review-text']/text()").extract()
            reviewText = "".join(reviewText)
            reviewText = reviewText.replace(",",";")
            reviewRating = reviewDivHXS.select("//div[@class='fk-stars']/@title").extract()
            reviewRating = "".join(reviewRating)
            reviewRating = reviewRating.split()
            reviewRating = reviewRating[0]
            reviewRating = int(reviewRating[0])
            reviewHelpFulIndex = reviewDivHXS.select("//div[@class='unit']/strong/text()").extract()
            '''
            reviewHelpFulIndex = "".join(reviewHelpFulIndex)
            
            reviewHelpFulIndex = self.textCleaner(reviewHelpFulIndex)
            '''
            
            if reviewHelpFulIndex:
                reviewHelpFulIndexParticipant = int(reviewHelpFulIndex[1])
                reviewHelpFulIndexPositive = reviewHelpFulIndex[0]
                if '%' in reviewHelpFulIndexPositive:
                    reviewHelpFulIndexPositive = reviewHelpFulIndexPositive.replace("%","")
                    reviewHelpFulIndexPositive = int(reviewHelpFulIndexPositive)*reviewHelpFulIndexParticipant/100
                else:
                    reviewHelpFulIndexPositive = int(reviewHelpFulIndexPositive)
            else:
                reviewHelpFulIndexParticipant = 0
                reviewHelpFulIndexPositive = 0
            
            reviewDate = reviewDivHXS.select("//div[@class='date line fk-font-small']/text()").extract()
            reviewDate = "".join(reviewDate)
            reviewDate = self.textCleaner(reviewDate)
            reviewDate = reviewDate.split(" ")
            try:
                reviewDate[1] = str(self.monthDict[reviewDate[1].lower()])
            except:
                reviewDate[1] = "12"
            reviewDate = ".".join(reviewDate)
            reviewDivItemList.append(reviewDate)
            reviewDivItemList.append(reviewHelpFulIndexParticipant)
            reviewDivItemList.append(reviewHelpFulIndexPositive)
            reviewDivItemList.append(reviewRating)
            reviewDivItemList.append( self.textCleaner(reviewText))
            reviewpageList.append(reviewDivItemList)
            #print reviewDivItemList
        return  reviewpageList
    
    def getRatingList(self,hxs):
        ratingList = hxs.select("//div[@class='rating-bars']/div[contains(@class,'progress')]/text()").extract()
        print ratingList
        ratingList = [rating.replace(",","") for rating in ratingList]
        ratingList = [int(rating) for rating in ratingList]
        
        return ratingList
    
    def getLastReviewRatingList(self,hxs):
        print "#########################"
        reviewRatingList= hxs.select("//div[@class='line']/div[@class='fk-stars']/@title").extract()
        
        ratingList5 = []
        iter = 0
        for rating in reviewRatingList:
            rating = rating.replace(" stars","")
            rating = rating.replace(" star","")
            rating = int(rating)
            ratingList5.append(rating)
            iter = iter+1
            if iter>4:
                break;
        return ratingList5
        
    
    
    def getLatestReviewDate(self,hxs):
        reviewDate = hxs.select("//div[@class='date line fk-font-small']/text()").extract()
        return  reviewDate
    
    
    def getLatestReviewText(self,hxs):
        reviewText = hxs.select("//p[@class='line bmargin10']").extract()
        textFair = []
        for text in reviewText:
            text = self.textCleaner(text)
            textFair.append(text)
        return textFair
    
    def getPagination(self,hxs):
        totalPaging = hxs.select("//div[@class='review-section helpful-review-container']/div[@class='line']/strong/text()").extract()
        for page in totalPaging:
            if "Next" in page:
                totalPaging.remove(page)
            if "-" in page:
                totalPaging.remove(page)
        
        totalPaging = [int(page) for page in totalPaging]
        try:
            totalPaging = max(totalPaging)
        except:
            totalPaging = 1
        return totalPaging
    
    def getReviewJSON(self, reviewDate, reviewText):
        Reviews = []
        iter = 0
        for review in reviewDate:
            reviewBlock= {}
            reviewBlock['uploadDate'] = review
            reviewBlock['review'] = reviewText[iter]
            Reviews.append(reviewBlock)
            iter= iter +1
        reviewJson = {}
        reviewJson['Reviews'] = Reviews
        reviewStr = str(reviewJson)
        return reviewJson
    
    def textCleaner(self,heading):
        heading = heading.replace("\r", "")
        heading = heading.replace("\n", "")
        #heading = heading.replace(",", "")
        heading = heading.strip()
        '  '.join(heading.split())
        '\n'.join(heading.split())
        heading = heading.replace('<p class="line bmargin10">',"")
        heading = heading.replace('<span class="review-text">',"")
        heading = heading.replace('</span>',"")
        heading = heading.replace('</p>',"")
        heading = heading.replace("'","")
        heading = heading.replace('"',"")
        heading = heading.replace('/',"")
        heading = heading.replace('\\',"")
        heading = heading.encode('utf-8')                       
        return heading