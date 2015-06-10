from scrapy.selector import HtmlXPathSelector
import urllib

class FlipKartScrapper:
	def getPrice(self,response, productName):
		hxs = HtmlXPathSelector(response)
		stockStatus = hxs.select('//div[@class="out-of-stock"]').extract()
		status = 1 
		if stockStatus:
			status =  0
		priceText = hxs.select('//span[contains(@class,"selling-price")]/text()').extract()
		try:
			priceText = priceText[0]
			priceText = priceText.strip()
			priceText = priceText.replace(",","")
			priceText = priceText.replace("Rs. ","")
			price = int(priceText)
		except:
			price = 0
		return price, status
		