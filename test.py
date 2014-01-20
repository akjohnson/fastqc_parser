import unittest
import fastqc_parser

class TestBasicParsing(unittest.TestCase):

    def setUp(self):
        self.file = "examples/basic.txt"
        self.parser = fastqc_parser.FastQCParser(self.file)

    def test_version(self):
        self.assertEqual(self.parser.version, '0.10.1') 

if __name__ == '__main__':
    unittest.main()
