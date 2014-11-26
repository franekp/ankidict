# -*- coding: utf-8 -*- 
import bs4
import lxml
import lxml.html
import requests
import json

USE_SOUP = True


def parse_func(txt):
	if(USE_SOUP):
		return bs4.BeautifulSoup(txt)
	else:
		return lxml.html.fromstring(txt)


def select_func(self,query):
	#1 [DONE] ogar czy soup dopuszcza select siebie, jeśli nie(najprawdopodobniej), to
	#1 [DONE] trzea zrobić to tak, że opakowujemy go (bierzemy 'parent')
	# 		i potem jedziemy z selectem.
	#2 [DONE] zrobić dobre sel_css(">...")
	#3 TODO przepisać i sprawdzić cały kod, żeby się zgadzał z xpathem
	#4 ew. koniec query typu txt i to jakoś jeszcze... (ale raczej nie)
	id_obscure = "asdfgh1234"
	while query[0] == ' ':
		query = query[1:]
	if(USE_SOUP):
		if(query[0] != '>'):
			return self.select(query)
		else:
			tmp_id = None
			if 'id' in self.attrs:
				tmp_id = self.attrs['id']
			self.attrs['id'] = id_obscure
			# tutaj jest "parent", bo wygląda na to, że nie można zaznaczyć samego siebie
			res = self.parent.select("#"+id_obscure+" "+query)
			if tmp_id:
				self.attrs['id'] = tmp_id
			else:
				del self.attrs['id']
			return res
	else:
		#TODO: precompiling queries and caching them in some dict
		if(query[0] != '>'):
			return self.cssselect(query)
		else:
			tmp_id = None
			if 'id' in self.attrib:
				tmp_id = self.attrib['id']
			self.attrib['id'] = id_obscure
			res = self.cssselect("#"+id_obscure+" "+query)
			if tmp_id:
				self.attrib['id'] = tmp_id
			else:
				del self.attrib['id']
			return res


def map_get_text(li):
	def f(el):
		return el.get_text()
	return map(f,li)


if(USE_SOUP):
	bs4.BeautifulSoup.sel_css = select_func
	bs4.element.Tag.sel_css = select_func
else :
	lxml.html.HtmlElement.sel_css = select_func
	def gettextmethod(self):
		return "".join(self.xpath(".//text()"))
	lxml.html.HtmlElement.get_text = gettextmethod

class word_sense(object):
	
	def from_html(self, element,ks=[]): #element - div.SENSE-BODY | div.SUB-SENSE-CONTENT
		'''
		self.definition = element.xpath(
		"span[@class='DEFINITION']//text()")
		'''
		#print element.sel_css("span.DEFINITION")
		self.definition = "".join(map_get_text(element.sel_css(" > span.DEFINITION")))
		#print self.definition
		'''
		self.keys = element.xpath("./strong/text() | \
		./span[@class='SENSE-VARIANT']//span[@class='BASE']/text() | \
		./span[@class='MULTIWORD']//span[@class='BASE']/text()")
		'''
		self.keys = element.sel_css(" > strong")
		self.keys += element.sel_css(" > span.SENSE-VARIANT span.BASE")
		self.keys += element.sel_css(" > span.MULTIWORD span.BASE")
		self.keys = map_get_text(self.keys)
		self.keys = self.keys + ks
		def mk_example(el):
			'''
			fst = el.xpath("./strong//text()")
			fst = "".join(fst)
			'''
			fst = map_get_text(el.sel_css(" > strong"))
			fst = "".join(fst)
			'''
			snd = "".join(el.xpath(".//p//text()"))
			'''
			snd = map_get_text(el.sel_css("p"))
			snd = "".join(snd)
			return (fst,snd)
		'''
		self.examples = map(mk_example, element.xpath("./div[@class='EXAMPLES']"))
		'''
		self.examples = map(mk_example, element.sel_css(" > div.EXAMPLES"))
	
	def from_primitive(self,data):
		raise "UNIMPL"
	
	def to_primitive(self):
		return (self.definition,self.examples)
	
	def __init__(self,inp,ks=[]):
		'''
		if isinstance(inp,lxml.html.HtmlElement) :
			self.from_html(inp,ks)
		else:
		self.from_json(inp)
		'''
		self.from_html(inp)
	
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
		page_text = requests.get(url).text
		page_tree = parse_func(page_text)
		#senses:
		'''
		sense_bodies = page_tree.xpath("//ol[@class='senses']//div[@class='SENSE-BODY'] |\
		//ol[@class='senses']//div[@class='SUB-SENSE-CONTENT']")
		'''
		''' nested_sbodies = page_tree.sel_css("ol.senses div.SUB-SENSE-CONTENT") '''
		# tego póki co nie włączamy:
		'''
		if USE_SOUP:
			for i in nested_sbodies:
				i['class'] = "SENSE-BODY"
		if not USE_SOUP:
			for i in nested_sbodies:
				i.attrib['class'] = "SENSE-BODY"
		'''
		
		sense_bodies = page_tree.sel_css("ol.senses div.SENSE-BODY")
		def get_nested(a):
			return a.sel_css("div.SUB-SENSE-CONTENT")
		nsense_bodies = [ [i]+get_nested(i) for i in sense_bodies]
		# flatten sense_bodies
		sense_bodies = [item for sublist in nsense_bodies for item in sublist]
		self.senses = map(lambda a: word_sense(a) , sense_bodies)
		#related:
		'''
		self.related = page_tree.xpath( \
		"//div[@class='entrylist']//ul//a[@title]")
		'''
		self.related = page_tree.sel_css("div.entrylist ul a[title]")
		def mk_related(el):
			'''
			li = el.xpath(".//span[@class!='PART-OF-SPEECH']/text()")
			return "".join(li)
			'''
			if USE_SOUP:
				return el.attrs['title']
			else:
				return el.attrib['title']
		self.related = map(mk_related, self.related)
		#phrases:
		'''
		phr_list = page_tree.xpath("//div[@id='phrases_container']/ul/li")
		'''
		phr_list = page_tree.sel_css("div#phrases_container > ul > li")
		self.phrases = []
		def mk_phrase(el):
			'''
			phr_names = map(lambda s: "".join(s.xpath(".//text()")) , \
			el.xpath(".//span[@class='BASE']"))
			'''
			# FIXME: może być czasem strong zamiast span.base
			phr_names = map(lambda s: s.get_text(), el.sel_css("span.BASE"))
			'''
			sbodies = el.xpath(".//div[@class='SENSE-BODY']")
			'''
			sbodies = el.sel_css("div.SENSE-BODY")
			sbodies += el.sel_css("div.SUB-SENSE-CONTENT")
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
	words = ['take-on', # multiple keys in last sense
	'Yours', # big error
	'take off', # informal senses
	''
	]
	
	page_url = 'http://www.macmillandictionary.com/dictionary/british/Yours'
	dict_entry(page_url).write()

main()



