import parser

url="http://cis.poly.edu/cs912/"

f=open("sample.html")
page=f.read()
f.close()
pool= page+page+"1"
p = parser.parser(url, page,pool, len(page)+1)

