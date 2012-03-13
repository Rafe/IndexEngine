from parser import parser
import cStringIO

class CParser:

  def __init__(self,uid=0):
    self.uid = uid

  def parse(self,url,html):
    try:
      return parser(url,html,html+html+"1",len(html))
    except TypeError as e:
      return (0,0)

  def reduce(self,url,html,urls,cid):
    data = self.parse(url,html)
    if data[0] == 0 : return 0

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
      lines.append((word,words[word],urls[url],uid))
      self.uid += 1
    return lines
