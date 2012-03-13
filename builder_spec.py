import unittest
import os
from builder import *
from pipeline import Pipeline
from cparser import CParser

class BuilderSpec(unittest.TestCase):

  def setUp(self):
    self.path ="testfiles"
    os.mkdir(self.path)
    os.system("touch " + self.path+"/1_index")
    os.system("touch " + self.path+"/1_data")
    self.files = [(self.path+"/1_index",self.path+"/1_data")]

  def tearDown(self):
    os.system("rm -r " + self.path)

  def test_FileParser_can_read_file_index_under_path(self):
    fp = FileParser()
    files = fp.getFiles(self.path)
    file = files.pop(0)
    self.assertEqual(file[0],'testfiles/1_index')
    self.assertEqual(file[1],'testfiles/1_data')

  def test_builder_can_pass_parser_and_files_to_initialize(self):
    b = IndexBuilder(self.files,None,None,None)
    self.assertEqual(b.files,self.files)
    self.assertEqual(b.uid,1)
    self.assertTrue(b.openNext())
    self.assertFalse(b.openNext())

  def test_UrlTable_can_load_url_file(self):
    t = UrlTable("testUrl")
    self.assertEqual(len(t.urls),3)
    url = t.urls.pop("http://test.google.com")
    self.assertEqual(url[1],"10000")

  def test_UrlTable_can_write_url_into_file(self):
    t = UrlTable("testUrl")
    t.write("http://test3.facebook.com",65525)

if __name__ == "__main__":
  unittest.main()
