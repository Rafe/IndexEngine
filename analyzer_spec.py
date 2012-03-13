import unittest

class AnalyzerSpec(unittest.TestCase):

  def test_analyzer_can_take_query_and_return_top_10_result(self):
    a = Analyzer()
    a.open('test_index')
    results = a.query("test").limit(10)
    assertEqual(len(results),10)

if __name__ == "__main__":
  unittest.main()
