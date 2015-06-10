from scrapy.selector import HtmlXPathSelector
import urllib

class SnapDealScrapper:
	def downloadProductDetails(self,response, productName, brand, snapDealMatch):
		hxs = HtmlXPathSelector(response)
		SpecTableDIV = hxs.select("//div[@class='detailssubbox']/table/tr/td/table[@class='product-spec']").extract()
		specDict = {}
		specDictVal = {}
		for specs in SpecTableDIV:
			specs = HtmlXPathSelector(text = specs)
			fields = specs.select("//tr").extract()
			
			keyValDict = {}

			for field in fields:
				field = HtmlXPathSelector(text = field)
				keyVal = field.select("//td/text()").extract()
				if keyVal:
					key = keyVal[0]
					value = keyVal[1]

					try:
						snapDealVal = snapDealMatch[key]
					except:
						snapDealVal = []
					if snapDealVal:
						try:
							specDictVal = specDict[snapDealVal[0]]	
						except:
							specDictVal = {}
						if specDictVal:
							snapDealDictKey = snapDealVal[1]
							specDictVal[snapDealDictKey] = value
							specDict[snapDealVal[0]] = specDictVal
						else:
							specDictVal = {}
							snapDealDictKey = snapDealVal[1]
							specDictVal[snapDealDictKey] = value
							specDict[snapDealVal[0]] = specDictVal


					
		# print specDict
		specificationList = []
		for specs in specDict:
			specificationDict = {}
			specificationDict[specs] = specDict[specs]
			specificationList.append(specificationDict)
		allSpecification = {}
		for specs in specificationList:
			try:
				specs["GENERAL FEATURES"]["Brand"] = brand
				specs["GENERAL FEATURES"]["Model Name"] = productName
			except:
				specDictVal = {}
				specDictVal["Brand"] = brand
				specDictVal["Model Name"] = productName
				specs["GENERAL FEATURES"] = specDictVal
		allSpecification['specification'] = specificationList
		return allSpecification


			
		#/img[contains(@class,"current")]/@src