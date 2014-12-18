# -*- coding: utf-8 -*-

USE_SOUP = True

if USE_SOUP:
	import bs4
else:
	import lxml
	import lxml.html

# import requests
import urllib2



__all__ = ["DictEntry", "DictEntrySense", "dict_query"]

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
	#3 [DONE] przepisać i sprawdzić cały kod, żeby się zgadzał z xpathem
	#  [DONE] dodać obsługę senses typu yours, z jakimś ogólnym akapitem na początku
	#  [DONE] dodać support dla dopisków typu infml, fml, etc
	#  [DONE] ogar wyników wyszukiwania
	#  [TODO] ogar innych dopisków (offensive, american, british, vulgar,
	#			abbr, euph, etc.)
	#  [TODO] ogar czegoś, co pozwoli robić łatwe linki z tekstu w tych głupich
	#				kontrolkach Qt - do related i SearchResults
	#  [TODO] kontrolki Qt
	#  [TODO] generowanie jakiegoś prostego html z DictEntrySense
	#  [TODO] komunikacja z anki
	#	[TODO] tryb testing - podzielone okienko w Qt na nasze oraz na stronę ściągniętą żywcem (do porównywania)
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

def init():
	if(USE_SOUP):
		bs4.BeautifulSoup.sel_css = select_func
		bs4.element.Tag.sel_css = select_func
	else :
		lxml.html.HtmlElement.sel_css = select_func
		def gettextmethod(self):
			return "".join(self.xpath(".//text()"))
		lxml.html.HtmlElement.get_text = gettextmethod

init()


class DictEntrySense(object):
	
	def __from_html(self, element,ks=[],style_lvl=""):
		#element - div.SENSE-BODY | div.SUB-SENSE-CONTENT
		
		'''
		self.definition = element.xpath(
		"span[@class='DEFINITION']//text()")
		'''
		self.definition = "".join(map_get_text(element.sel_css(" > span.DEFINITION")))
		self.definition += "".join(map_get_text(
			element.sel_css(" > span.QUICK-DEFINITION")))
		
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
		
		self.style_level = "".join(map_get_text(element.sel_css(" > span.STYLE-LEVEL")))
		self.style_level += style_lvl
		
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
	
	def __from_intro_paragraph(self, intro):
		self.keys = []
		self.style_level = ""
		self.definition = intro
		self.examples = []
	
	def __init__(self,inp=None,ks=[],style_lvl="",intro=None):
		if intro is not None:
			self.__from_intro_paragraph(intro)
		if inp is not None:
			self.__from_html(inp,ks,style_lvl)
	
	def print_txt(self):
		'''
		print self.keys
		print self.style_level
		print self.definition
		print self.examples
		'''
		print self.get_html()
		print "___________________\n"
	
	def get_html(self):
		wyn = ""
		wyn += "<strong>"+("</strong> <i> or  </i> <strong>".join(self.keys))+"</strong>"
		wyn += " --- "
		if self.style_level != "":
			wyn += "<i> "+self.style_level+" </i>"
		wyn += self.definition
		wyn += "<br />"
		wyn += '<font color="blue"><i>'
		wyn += "<br />".join(map(lambda (a,b): "<strong>"+a+"</strong>"+b, self.examples))
		wyn += "</i></font>"
		return wyn
	
	def get_word_html(self):
		return "<strong>"+(" </strong ><i> or </i> <strong> ".join(self.keys))+"</strong>"
	
	def get_def_html(self):
		wyn = ""
		if self.style_level != "":
			wyn += "<i>"+self.style_level+"</i>"
		tmp_def = self.definition
		for i in self.keys:
			tmp_def = " ____ ".join(tmp_def.split(i))
		return wyn + tmp_def
	
	def get_full_def_html(self):
		wyn = ""
		if self.style_level != "":
			wyn += "<i>"+self.style_level+"</i>"
		return wyn + self.definition
	
	def set_key_if_needed(self, k):
		if self.keys == []:
			self.keys = [k]
		else:
			pass



class DictEntry(object):
	
	def __from_html(self, page_tree):
		self.senses = []
		#senses:
		'''
		sense_bodies = page_tree.xpath("//ol[@class='senses']//div[@class='SENSE-BODY'] |\
		//ol[@class='senses']//div[@class='SUB-SENSE-CONTENT']")
		'''
		''' nested_sbodies = page_tree.sel_css("ol.senses div.SUB-SENSE-CONTENT") '''
		
		sense_bodies = page_tree.sel_css("ol.senses div.SENSE-BODY")
		
		def get_nested(a):
			return a.sel_css("div.SUB-SENSE-CONTENT")
		nsense_bodies = [ [i]+get_nested(i) for i in sense_bodies]
		# flatten sense_bodies
		sense_bodies = [item for sublist in nsense_bodies for item in sublist]
		self.senses = map(lambda a: DictEntrySense(a) , sense_bodies)
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
				return (el.attrs['title'], el.attrs['href'])
			else:
				return (el.attrib['title'], el.attrib['href'])
		self.related = map(mk_related, self.related)
		#div.HEAD-INFO - też spis treści
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
			phr_names = map_get_text(el.sel_css("span.BASE"))
			phr_style_level = "".join(map_get_text(el.sel_css(" span.STYLE-LEVEL")))
			'''
			sbodies = el.xpath(".//div[@class='SENSE-BODY']")
			'''
			sbodies = el.sel_css("div.SENSE-BODY")
			sbodies += el.sel_css("div.SUB-SENSE-CONTENT")
			phr_senses = map(lambda a: DictEntrySense(a, phr_names, phr_style_level)
				, sbodies)
			self.phrases = self.phrases + phr_senses
		map(mk_phrase, phr_list)
		
		global_key = "".join(map_get_text(page_tree.sel_css("div#headword div#headwordleft span.BASE")))
		self.word = global_key
		# setting keys for senses that don't have one 
		for i in self.senses:
			i.set_key_if_needed(global_key)
		#intro_paragraph:
		self.intro_paragraph = "\n".join(map_get_text(
			page_tree.sel_css("div.SUMMARY div.p")))
		if self.intro_paragraph != "":
			self.intro_paragraph_sense_l = [DictEntrySense(intro=self.intro_paragraph)]
			self.intro_paragraph_sense_l[0].set_key_if_needed(global_key)
		else:
			self.intro_paragraph_sense_l = []
		
	
	def __init__(self, node):
		self.__from_html(node)
	
	def print_txt(self):
		print "	[[[ self.intro_paragraph ]]]"
		print self.intro_paragraph
		print "	[[[ self.senses ]]]"
		for i in self.senses:
			i.print_txt()
		print len(self.senses)
		print "	[[[ self.related ]]]"
		print self.related
		print len(self.related)
		print "	[[[ self.phrases ]]]"
		for i in self.phrases:
			i.print_txt()
		print len(self.phrases)


class SearchResults(object):
	
	def __from_html(self, node):
		self.results = map_get_text(node.sel_css("div#search-results > ul > li > a"))
		def make_addr(el):
			a = ""
			if USE_SOUP:
				a = (el.attrs['href'])
			else:
				a = (el.attrib['href'])
		def make_addr2(a):
			a = a.replace(" ","-")
			a = a.replace("/","-")
			a = "http://www.macmillandictionary.com/dictionary/british/" + a
			return a
		#self.links = map(make_addr, node.sel_css("div#search-results > ul > li > a"))
		self.links = map(make_addr2, self.results)
		self.links = zip(self.results, self.links)
	
	def __init__(self, node, q):
		self.__from_html(node)
		self.word = q
	
	def print_txt(self):
		print "[[[ did you mean ]]]"
		for i in self.results:
			print i
			print "_______"


def dict_query(query):
	# do normalnego wyszukiwania
	normal_prefix = "http://www.macmillandictionary.com/search/british/direct/?q="
	# do wyszukiwania listy podobnych (jak trafisz, to i tak masz 'did you mean')
	search_prefix = "http://www.macmillandictionary.com/spellcheck/british/?q="
	url = ""
	if query[:7] == "http://":
		url = query
	else:
		url = normal_prefix + query.replace(" ","+")
	
	def fetch_webpage(addr):
		response = urllib2.urlopen(addr)
		return response.read()
		
	def fetch_webpage_old(addr):
		return requests.get(addr).text
	
	root = parse_func(fetch_webpage(url))
	
	if root.sel_css("div#didyoumean") == [] :
		return DictEntry(root)
	else:
		return SearchResults(root, query)


def main():
	words = [
		'take-on', # multiple keys in last sense
		'yours', # intro paragraph, informal phrase
		'take off', # informal
		'air', # plural, singular, nested senses
		'reference', # american nested, [only before noun] nested, cntable, uncntable,
						# formal phrase
		'my', # intro_paragraph
		'then', # multiple phrases one sense
		'since when', # phrase finding in entry for 'since'
	]
	q = "take on"
	dict_query(q).print_txt()

if __name__ == "__main__":
	main()

'''
interfejs:

class DictEntrySense
	
	keys :: [string]
		dodatkowe uszczegółowienia słowa: np. yours -> Sincerely yours
	
	style_level :: string
		'formal' | 'informal' | 'literary' | 'spoken' | ''
	
	definition :: string
		definicja słowa w stringu
	
	examples :: [(key :: string, ex :: string)]
		przykłady użycia słowa
		key - dodatkowo uszczegółowione słowo na potrzeby przykładu
		ex - treść przykładu


class DictEntry
	
	word :: string
		dane słowo
	
	senses :: [DictEntrySense]
		znaczenia słowa (bez fraz)
	
	phrases :: [DictEntrySense]
		znaczenia fraz zrobionych z tego słowa
		(jak jakaś fraza ma kilka znaczeń, to każde z
		nich jest na tej liście)
	
	related :: [(title::string, href::string)]
		slowa/frazy powiązane z danym słowem
	
	intro_paragraph :: string
		to, co jest czasem na początku napisane,
		zwykle jakieś uwagi gramatyczne
	
	intro_paragraph_sense_l :: [DictEntrySense]
		j. w. (dodane, żeby było mniej kodu w dict_window.py)
		zawsze zachodzi: len(intro_paragraph_sense_l) in {0,1}


class SearchResults
	
	word :: string
	
	results :: [string]
		lista 'czy chodziło Ci o ...'

'''


