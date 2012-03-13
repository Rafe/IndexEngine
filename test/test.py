import gzip
import dircache
import parser

path = "nz2_merged"
files = dircache.listdir(path)

data = gzip.open(path+ "/0_data", "r") #decompress(indata)
index = gzip.open(path+ "/0_index","r")
info = index.readline().split()

line = data.readline()
while(line != '\r\n'):
	line = data.readline()

html = data.read(int(info[3]) - data.tell())
pool = html + html + "1"

p = parser.parser(info[0],html,pool,len(html) + 1)

#[url,?,?,position,ip,port,ok]
#left = data.read(info[3])
	
#data.close()
#index.close()
	
