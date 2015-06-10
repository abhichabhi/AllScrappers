from scrapy.selector import HtmlXPathSelector
import urllib

class AmazonScrapper:
	def downloadProductList(self,response, productName):
		hxs = HtmlXPathSelector(response)
		imageURL = hxs.select('//img[@id="landingImage"]/@src').extract()
		try:
			imageURL = imageURL[0]
			print imageURL
			urllib.urlretrieve(imageURL,productName)
		except:
			print "image could not be found for " + productName
		#/img[contains(@class,"current")]/@src