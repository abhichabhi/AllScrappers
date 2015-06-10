from scrapy.selector import HtmlXPathSelector
import urllib

class FlipKartScrapper:
	def downloadProductDetails(self,response, productName):
		hxs = HtmlXPathSelector(response)
		specTableList = hxs.select("//table[@class='specTable']").extract()
		AllProductSpecs = {}
		AllProductSpecsList = []
		for specTable in specTableList:
			specTable = HtmlXPathSelector(text = specTable)
			specHead = specTable.select("//th[@class='groupHead']/text()").extract()
			if specHead:
				specSubCollection = {}
				specHead = specHead[0]
				specSubList = specTable.select("//tr").extract()
				
				if specSubList:

					specSubCollectionDict = {}
					specSubDict = {}
					for specSub in specSubList:
						
						specSub = HtmlXPathSelector(text = specSub)
						try:
							key = specSub.select("//td[@class='specsKey']/text()").extract()
							val = specSub.select("//td[@class='specsValue']/text()").extract()
						except:
							print
						if key and val:
							if key[0] == "Model Name":
								val = [productName]
							specSubDict[key[0]] = val[0].strip()
					specSubCollection[specHead] = specSubDict
					AllProductSpecsList.append(specSubCollection)
		AllProductSpecs['specification'] = AllProductSpecsList
		return AllProductSpecs

		
