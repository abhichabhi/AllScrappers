from scrapy.selector import HtmlXPathSelector
import urllib

class SnapDealScrapper:
	def downloadProductList(self,response, productName):
		hxs = HtmlXPathSelector(response)
		imageURL = hxs.select('//ul[@id="product-slider"]/li/img/@src').extract()
		try:
			imageURL = imageURL[0]
			urllib.urlretrieve(imageURL,productName)
		except:
			print "image could not be found for " + productName
		#/img[contains(@class,"current")]/@src