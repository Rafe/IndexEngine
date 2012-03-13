from struct import *
from heapq import *
import gzip

def isInt(x):
  try:
    int(x)
    return True
  except:
    return False

class Pipeline:

  INT = type(3)
  fmt = "14sHI"
  SIZE = 20

  def __init__(self,path="",debug=False):
    self.debug = debug
    if path != "":
      self.open(path)

  def open(self,path,compress=False):
    if compress:
      self.file = gzip.open(path)
    else:
      self.file = open(path)
  
  def checkItem(self,item):
    if len(item) < 3 : return False
    #if type(item[1]) != self.INT : return False
    if len(item[0]) > 14 : return False
    return True
      
  def pack(self,item):
    if not self.debug:
      return pack(self.fmt,item[0],item[1],item[2])
    else:
      return "%s %s %s\r\n" % (item[0],item[1],item[2])

  def write(self,items,path):
    file = open(path,"w")
    for item in items:
      if not self.checkItem(item): continue
      file.write(self.pack(item))
    file.close
  
  def flushHeap(self,heap,path,compress=False):
    if compress:
      file = gzip.open(path,"a")
    else:
      file = open(path,"a")
    while len(heap) > 0:
      item = heappop(heap)
      if not self.checkItem(item): continue
      file.write(self.pack(item))
    file.close

  def read(self):
    if not self.debug:
      item = self.file.read(self.SIZE)
      if item != "":
        return unpack(self.fmt,item)
    else:
      item = self.file.readline().split()
      if len(item) ==3:
        return item
    self.file.close()
    return None
