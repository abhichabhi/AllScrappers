from scrapy.selector import HtmlXPathSelector
import urllib

class FlipKartScrapper:
	def downloadProductList(self,response, productName):
		hxs = HtmlXPathSelector(response)
		imageURL = hxs.select('//div[@class="imgWrapper"]/img[contains(@class,"productImage  current")]/@data-src').extract()
		try:
			imageURL = imageURL[0]
			urllib.urlretrieve(imageURL,productName)
		except:
			print "image could not be found for " + productName
		