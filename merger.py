from heapq import *
from pipeline import Pipeline
import dircache
import sys

HEAP_SIZE = 2000000

def printf(str):
  sys.stdout.write(str)
  sys.stdout.flush()

def compare(a,b):
  if a[0] == b[0]:
    if a[1] == b[1]: return 0
    return 1 if (a[1] < b[1]) else -1
  
  if a[0] < b[0]:
    return 1
  else :
    return -1

class Merger:

  def __init__(self,path):
    self.path = path
    self.queue = self.getFiles(dircache.listdir(path))
    self.heap = []
    self.pipe = Pipeline()
  
  def getFiles(self,files):
    queue = []
    for f in files:
      if f[:5] == "index":
        queue.append(f)
    return queue

  def merge(self):  
    id = 1
    printf("processing %d index files:" % len(self.queue) )
    while len(self.queue) > 1:
      p1 = Pipeline(self.path+"/"+self.queue.pop(0))
      p2 = Pipeline(self.path+"/"+self.queue.pop(0))
      # output final rindex to main folder
      if len(self.queue) == 0:
        self.path = "."
        self.merge_file(p1,p2,"rindex")
      else:
        self.merge_file(p1,p2,"rindex_"+str(id))
        printf("#")
      self.queue.append("rindex_"+str(id))
      id+=1

  def merge_file(self,p1,p2,filename,compress=False):
    item = p1.read()
    item2 = p2.read()
    heap = []
    while True:
      if item == None and item2 == None : break
      elif item == None: c = -1
      elif item2 == None: c = 1
      else:
        c = compare(item,item2)

      if c > 0: 
        heap.append(item)
        item = p1.read()
      if c < 0:
        heap.append(item2)
        item2 = p2.read()
      
      if c == 0:
        heappush(heap,item)
        heappush(heap,item2)
        item = p1.read()
        item2 = p2.read()

      if len(heap) > HEAP_SIZE:
        self.flush(heap,filename,compress)
        heap = []
        #print "saved index heap to " + filename

    self.flush(heap,filename,compress)
    heap = []

  def flush(self,heap,filename,compress=False):
    printf("#")
    self.pipe.flushHeap(heap,self.path+"/"+filename,compress)
