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

class AmazonScrapper():
    name = "Amazon"
    monthDict = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11, "december":12}
    # Headin_Flag = 1
    # headingList = ['ProductUrl', 'ProductName', 'SellingPrice','ProductQuantity', 'Productrating', 'ProductMerchantInfo','Availability','Discount','DeliveryCharge']
    def getProductDetailsList(self,response):
        print response.url
        hxs = HtmlXPathSelector(response)
        pDetailList = []
        
        pDetailList.append(response.url)
        pDetailList.append(self.getProductName(hxs)) #Product Name   http://www.amazon.in/product-reviews/B00FXLCG7G?pageNumber=1
        totalpaging = self.getPagination(hxs)
        #totalpaging = min(totalpaging,500)
        reviewPageList = []
        for page in range(1,totalpaging+1):
            pageURL = response.url + "?pageNumber=" + str(page)
            print pageURL
            respRating = requests.get(url=pageURL, timeout=20)
            respRatingText = respRating.text
            respRatingText = respRatingText.encode('utf-8', 'ignore')
            ratingHXS = HtmlXPathSelector(text = respRatingText)
            
            #print ratingHXS.select("//div[@class='reviewText']/text()").extract()
            reviewPageList = reviewPageList + self.getReviewListOfPage(ratingHXS)
        
        pDetailList.append(self.getRatingList(hxs))  #Rating List
        #pDetailList.append(self.getLastReviewRatingList(hxs))
        #pDetailList.append(self.getReviewJSON(self.getLatestReviewDate(hxs), self.getLatestReviewText(hxs)))
        #print pDetailList
                
        
       
        return pDetailList, reviewPageList
    def getProductName(self,hxs):
        pName = hxs.select("//h1/div/a/text()").extract()[0]
        pName = self.textCleaner(pName)
        pName = pName.replace(',',';')
        return pName
    
    def getReviewListOfPage(self,hxs):
        reviewpageList = []
        reviewDIVlist = hxs.select("//table[@id='productReviews']/tr/td/div").extract()
        for reviewDiv in reviewDIVlist:
            reviewDivItemList = []
            reviewDivHXS = HtmlXPathSelector(text = reviewDiv)
            reviewText = reviewDivHXS.select("//div[@class='reviewText']/text()").extract()
            reviewText = "".join(reviewText)
            reviewText = reviewText.replace(",",";")
            reviewRating = reviewDivHXS.select("//span[@style='margin-right:5px;']/span/span/text()").extract()
            reviewRating = "".join(reviewRating)
            reviewRating = reviewRating.split()
            reviewRating = reviewRating[0]
            reviewRating = int(reviewRating[0])
            reviewHelpFulIndex = reviewDivHXS.select("//div[@style='margin-bottom:0.5em;']/text()").extract()
            reviewHelpFulIndex = "".join(reviewHelpFulIndex)
            reviewHelpFulIndex = self.textCleaner(reviewHelpFulIndex)
            if reviewHelpFulIndex:
                reviewHelpFulIndex = reviewHelpFulIndex.split()
                reviewHelpFulIndexParticipant = int(reviewHelpFulIndex[2])
                reviewHelpFulIndexPositive = int(reviewHelpFulIndex[0])
            else:
                reviewHelpFulIndexParticipant = 0
                reviewHelpFulIndexPositive = 0
            reviewDate = reviewDivHXS.select("//nobr/text()").extract()
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
        return  reviewpageList
        
    def getPagination(self,hxs):
        totalPaging = hxs.select("//span[@class='paging']/a/text()").extract()
        
        for page in totalPaging:
            if "Next" in page:
                totalPaging.remove(page)
        totalPaging = [int(page) for page in totalPaging]
        try:
            totalPaging = max(totalPaging)
        except:
            totalPaging=1
        return totalPaging
    
    
    def getRatingList(self,hxs):
        ratingList = hxs.select("//div[@class='histoCount']/text()").extract()
        ratingList = [(rating.replace(" star","")) for rating in ratingList]
        return ratingList
    
    def getLastReviewRatingList(self,hxs):
        reviewRatingList= hxs.select("//span[@style='margin-right:5px;']/span/span/text()").extract()
        reviewRatingList = [review[0] for review in reviewRatingList]
        #print reviewRatingList
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
        reviewDate = hxs.select("//span[@style='vertical-align:middle;']/nobr/text()").extract()
        return  reviewDate
    
    
    def getLatestReviewText(self,hxs):
        reviewText = hxs.select("//div[@class='reviewText']").extract()
        textFair = []
        for text in reviewText:
            text = self.textCleaner(text)
            textFair.append(text)
        return textFair
    
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
        heading = heading.replace("|", "")
        heading = heading.replace("\r", "")
        heading = heading.replace("\n", "")
        #heading = heading.replace(",", "")
        heading = heading.strip()
        '  '.join(heading.split())
        '\n'.join(heading.split())
        heading = heading.replace('<div class="reviewText">',"")
        heading = heading.replace('<div>',"")
        heading = heading.replace('</div>',"")
        heading = heading.replace('</p>',"")
        heading = heading.replace("'","")
        heading = heading.replace('"',"")
        heading = heading.replace('/',"")
        heading = heading.replace('\\',"")
        heading = heading.encode('utf-8')                       
        return heading