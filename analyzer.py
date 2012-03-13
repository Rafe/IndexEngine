from pipeline import Pipeline
from struct import *
from builder import UrlTable
import os,math,time
import operator

fmt = "14sHI"
SIZE = 20

def nextWord(char):
  c = chr(ord(char) + 1)
  if c >= 'z':
    return 0
  else :return c

class Analyzer:
  def open(self,index):
    self.table = UrlTable("url_index",mode = "index")
    self.index = open(index)
    self.size = os.path.getsize(index) / SIZE
    self.total = self.size / SIZE
    self.indexList = {}
    f = open("iindex")
    for l in f.readlines():
      word , pos = l.split(" ")
      self.indexList[word] = pos
    f.close()

  def close(self):
    self.index.close()

  def nextGEQ(self,query):
    self.count = 0
    self.sum = 0
    self.avgsize = 1
    n = 0
    start = int(self.indexList[query[0]]) / SIZE or 0
    found = False
    end = (int(self.indexList[nextWord(query[0])]) / SIZE) - 1 or self.size
    mid = math.floor(end / 2) 
    self.index.seek((mid - 1) * SIZE)
    item = unpack(fmt,self.index.read(SIZE))
    while item:
      word = item[0].strip('\x00')
      if word == query:
        break
      elif word < query:
        start = mid + 1
        mid = math.floor((start + end )/2)
      elif word > query:
        end = mid - 1
        mid = math.floor((start + end )/2)
      
      if start >= end:
        break  
      #print (start,mid,end)
      self.index.seek(mid * SIZE)
      item = unpack(fmt,self.index.read(SIZE))
      n += 1
      if n > 1000:
        break

    #go to head:
    while item[0].strip('\x00') == query:
      mid -= 1
      self.index.seek(mid * SIZE)
      item = unpack(fmt,self.index.read(SIZE))

    #read from head
    item = unpack(fmt,self.index.read(SIZE))
    n = 0
    while item[0].strip('\x00') == query:
      if not item[2] in self.table.urls:
        item = unpack(fmt,self.index.read(SIZE))
        continue
      url , size = self.table.urls[item[2]]
      yield (item[0],item[1], url,size)
      item = unpack(fmt,self.index.read(SIZE))
      self.count += 1
      #print item
      self.sum += int(size)
    if self.count == 0 : self.count = 1
    self.avgsize = self.sum / self.count

  def BM25(self,freq,size):
    K =  1.2 * ((1 - 0.75) + 0.75) * self.count/self.avgsize 
    return math.log10(self.size - self.count + 0.5) / (self.count + 0.5) * ((1.2 +1) * freq )/ (K + freq)

if __name__ == "__main__":
  a = Analyzer()
  a.open("rindex")
  while True:
    query = raw_input("please enter search query:")
    if query == "": exit()
    
    querys = query.split(" ")

    m = {}
    t = time.time()
    for q in querys:

      r = a.nextGEQ(q)

      for i in r:
        BM = a.BM25(i[1],int(i[3]))
        if i[2] in m:
          m[i[2]] += BM
        else:
          m[i[2]] = BM

    m = sorted(m.iteritems(), key = operator.itemgetter(1),reverse=True)
    t = time.time() - t
    n = 0
    print "results for query: %s , search time:%s" %(query,t)

    for i in m:
      print "in %s : BM=%s" %(i[0],i[1])
      n+=1
      if n >= 10:break
