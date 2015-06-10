from scrapy.selector import HtmlXPathSelector
from decimal import Decimal
import urllib

class AmazonScrapper:
	def getPrice(self,response, productName):
		hxs = HtmlXPathSelector(response)
		stock = 1 
		priceText = hxs.select('//span[@id="priceblock_ourprice"]/text()').extract()
		stockDiv = hxs.select('//div[@id="availability"]/span/text()').extract()

		if not priceText:
			priceText = hxs.select('//span[@class="a-color-price"]/text()').extract()
		if not priceText:
			priceText = hxs.select('//span[@class="a-color-price"]/text()').extract()
		try:
			priceText = priceText[0]
			priceText = priceText.strip()
			priceText = priceText.replace(",","")

			priceText = priceText.replace("Rs ","")

			price = Decimal(priceText)
			price = int(price)

			print price
		except:
			price = 0
		if stockDiv:
			stock = 0
		return price,stock