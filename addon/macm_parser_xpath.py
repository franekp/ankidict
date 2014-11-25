from lxml import html
import lxml
import requests
import json

class word_sense(object):
	
	def from_html(self, element,ks=[]): #element - div.SENSE-BODY | div.SUB-SENSE-CONTENT
		self.definition = element.xpath(
		"span[@class='DEFINITION']//text()")
		self.definition = "".join(self.definition)
		self.keys = element.xpath("./strong/text() | \
		./span[@class='SENSE-VARIANT']//span[@class='BASE']/text() | \
		./span[@class='MULTIWORD']//span[@class='BASE']/text()")
		self.keys = self.keys + ks
		def mk_example(el):
			fst = el.xpath("./strong//text()")
			fst = "".join(fst)
			snd = "".join(el.xpath(".//p//text()"))
			return (fst,snd)
		self.examples = map(mk_example, element.xpath("./div[@class='EXAMPLES']"))
	
	def from_primitive(self,data):
		raise "UNIMPL"
	
	def to_primitive(self):
		return (self.definition,self.examples)
	
	def __init__(self,inp,ks=[]):
		if isinstance(inp,lxml.html.HtmlElement) :
			self.from_html(inp,ks)
		else: self.from_json(inp)
	
	def write(self):
		print self.keys
		print self.definition
		print self.examples
		print "___________________\n"
	
	def __str__(self):
		#TODO: print words also here
		return str(self.definition)+"\n"+str(self.examples)+"\n___\n"
	
	def __repr__(self):
		return self.__str__()


class dict_entry(object):
	
	def from_url(self,url):
		self.senses = []
		page_text = requests.get(url)
		page_tree = html.fromstring(page_text.text)
		sense_bodies = page_tree.xpath("//ol[@class='senses']//div[@class='SENSE-BODY'] |\
		//ol[@class='senses']//div[@class='SUB-SENSE-CONTENT']")
		self.senses = map(lambda a: word_sense(a) , sense_bodies)
		self.related = page_tree.xpath( \
		"//div[@class='entrylist']//ul//a[@title]")
		def mk_related(el):
			li = el.xpath(".//span[@class!='PART-OF-SPEECH']/text()")
			return "".join(li)
		self.related = map(mk_related, self.related)
		# self.phrases = 
		phr_list = page_tree.xpath("//div[@id='phrases_container']/ul/li")
		self.phrases = []
		def mk_phrase(el):
			phr_names = map(lambda s: "".join(s.xpath(".//text()")) , \
			el.xpath(".//span[@class='BASE']"))
			sbodies = el.xpath(".//div[@class='SENSE-BODY']")
			phr_senses = map(lambda a: word_sense(a, phr_names) , sbodies)
			self.phrases = self.phrases + phr_senses
		map(mk_phrase, phr_list)
	
	def __init__(self,url):
		self.from_url(url)
		
	def write(self):
		print "	[[[ self.senses ]]]"
		for i in self.senses:
			i.write()
		print len(self.senses)
		print "	[[[ self.related ]]]"
		print self.related
		print len(self.related)
		print "	[[[ self.phrases ]]]"
		for i in self.phrases:
			i.write()
		print len(self.phrases)

def main():
	page_url = 'http://www.macmillandictionary.com/dictionary/british/make'
	dict_entry(page_url).write()

main()



