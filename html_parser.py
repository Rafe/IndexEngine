from HTMLParser import HTMLParser
class Parser(HTMLParser):
	
	def __init__(self):
		HTMLParser.__init__(self)
		self.urls=[]
		self.words = {}
		self.inscript = False
		self.inbody = False
	
	def handle_starttag(self, tag , attrs):
		if tag == "script":
			self.inscript = True
		if tag == "body":
			self.inbody = True

	def handle_data(self,data):
		if self.inscript : return
		for word in data.split():
			w = word.strip(' ,.?!-:\'\\\/').lower()
			if w in self.words:
				self.words[w] += 1
			else:
				self.words[w] = 1

	def handle_endtag(self, tag):
		if tag == "script":
			self.inscript = False
		if tag == "body":
			self.inbody = False

