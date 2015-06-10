from scrapy.selector import HtmlXPathSelector
import urllib

class SnapDealScrapper:
	def getPrice(self,response, productName):
		hxs = HtmlXPathSelector(response)
		status = 1 
		stockStatus = hxs.select("//div[@class='notifyMe-soldout']/text()").extract()
		if stockStatus:
			status = 0
		priceText = hxs.select('//span[@id="selling-price-id"]/text()').extract()
		
		try:
			priceText = priceText[0]
			priceText = priceText.strip()
			priceText = priceText.replace(",","")
			priceText = priceText.replace("Rs. ","")
			price = int(priceText)
		except:
			price = 0
		return price, status

		#/img[contains(@class,"current")]/@src