import tarfile , sys , dircache , time , gzip , cStringIO
from struct import pack , unpack
from cparser import CParser
from heapq import heappush,heappop
from pipeline import Pipeline
from merger import Merger
import os

BUFF_SIZE = 5000000

def extract_all(file):
	f = tarfile.open(file,"r")
	f.extractall("./tmp")

class FileParser:
    
  def extract(self,file,path):
    f = tarfile.open(file,"r")
    f.extractall(path)

  def getFiles(self,path):
    queue = []
    for file in dircache.listdir(path):
      if file == "indexlist.inf": 
        break
      file_index, file_type = file.split("_")
	    
      if not file_type == "data":
		    continue
      queue.append((path+"/"+file_index+"_index",path+"/"+file))
    return queue

class UrlTable:

  def __init__(self,path="url_index",mode="url"):
    self.path = path
    self.urls = {}
    self.cid = 0
    self.file = None
    if mode == "url":
      self.load()
    elif mode =="index":
      self.indexLoad()

  def write(self,url,size):
    if url in self.urls:
      return 0

    self.cid+=1

    if not self.file:
      self.file = open(self.path,"a")

    self.file.write(url+" "+str(size)+" " + str(self.cid)+"\n")
    return self.cid

  def load(self):
    file = open(self.path)
    for line in file.readlines():
      url , size, cid = line.split()
      self.cid = int(cid)
      self.urls[url] = (self.cid,size)

  def indexLoad(self):
    file = open(self.path)
    for line in file.readlines():
      url , size, cid = line.split()
      self.cid = int(cid)
      self.urls[self.cid] = (url,size)
    

class IndexBuilder:
  
  def __init__(self,files,table,parser,pipeline,uid=1):
    self.uid = uid
    self.pipe = pipeline
    self.parser = parser
    self.files = files
    self.table = table
    self.id = 0
    self.page_id = 0
  
  def openNext(self):
    if(len(self.files) > 0):
      file = self.files.pop()
      self.index = gzip.open(file[0], "r")
      self.data = gzip.open(file[1], "r")
      return 1
    else:
      return 0

  def read(self):
    info = self.index.readline().split()
    while info:
      yield (info[0],self.data.read(int(info[3])),info[3])
      info = self.index.readline().split()
      self.page_id += 1
    
    self.close()
  
  def close(self):
    self.data.close()
    self.index.close()

  def writeUrl(self,url,size):
    return self.table.write(url,size)
  
  def reduce(self,url,html,size):
    data = self.parser.parse(url,html)
    
    if data[0] == 0 : 
      #print "error"
      return 0
    
    if not url in self.table.urls:
      self.table.urls[url] = (self.writeUrl(url,size),size)

    urlid= self.table.urls[url][0]
    #print urlid

    stream = cStringIO.StringIO(data[1])

    words = {}
    for line in stream:
      word = line.split()
      if not word: continue
      elif word[0]:
        if word[0] in words:
          words[word[0]]+=1
        else:
          words[word[0]] = 1
    
    lines = []

    for word in words:
      lines.append((word,words[word],urlid,self.uid))
      self.uid += 1

    return lines

  def process(self):
    lines = []
    while self.openNext():
      for item in self.read():
        line = r.reduce(item[0],item[1],item[2])
        if line == 0: continue
        lines.extend(line)

      printf('#')

      if len(lines) > BUFF_SIZE:
        self.flush(lines,"tmp/index_"+ str(self.id))
        lines = []

    self.flush(lines,"tmp/index_"+ str(self.id))

  def flush(self,lines,path):
    lines.sort()
    self.pipe.write(lines,path)
    self.id += 1

def printf(str):
  sys.stdout.write(str)
  sys.stdout.flush()

def cleanup(dir):
  os.system("rm -r %s" % dir)

def build_index(index):
  p = Pipeline(index)
  alphabat ="abcdefghijklmnopqrstuvwxyz"
  n = 0
  l = []
  while n < len(alphabat):
    item = p.read()
    if not item: return
    if item[0][0] == alphabat[n]:
      print item
      l.append((alphabat[n],p.file.tell() - 32))
      n+=1

  f = open("iindex",'w')
  for i in l:
    print i
    f.write("%s %s\n" %(i[0],i[1]))
  f.close()

if __name__ == "__main__":

  if len(sys.argv) != 2:
    print "usage: python builder.py [filename]"

  archive = sys.argv[1]

  fp = FileParser()
  fp.extract(archive,'tmp')
  extract_all(archive)
  #get filename from archive: nz.tar => tmp/nz_merged
  files = fp.getFiles('tmp/'+archive.split(".")[0]+"_merged")

  t = time.time()
  r = IndexBuilder(files, UrlTable(), CParser(), Pipeline())
  printf("parsing %d files:" % len(r.files) ) 
  r.process()

  print "\nparsed %d pages in %d files for %f seconds" % (r.page_id, r.id ,time.time() - t)
  print "avarage %f second for parsing each files" % ( (time.time() -t) / r.id )
  print "started to build revert_index: "
  
  t = time.time()
  m = Merger("tmp")
  m.merge()
  print "\nbuild reverted index for %d records in %f seconds" % (r.uid,(time.time() - t))
  cleanup("tmp")

  build_index("rindex")
