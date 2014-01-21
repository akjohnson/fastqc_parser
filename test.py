import unittest
import logging
import sys

from fastqc_parser import FastQCParser, PASS_RESULT, FAIL_RESULT, WARN_RESULT

class TestBasicParsing(unittest.TestCase):

    expected_results = {
        'Per base sequence quality': PASS_RESULT,
        'Per sequence quality scores': PASS_RESULT,
        'Per base sequence content': WARN_RESULT,
        'Per base GC content': WARN_RESULT,
        'Per sequence GC content': FAIL_RESULT,
        'Per base N content': PASS_RESULT,
        'Sequence Length Distribution': PASS_RESULT,
        'Basic Statistics': PASS_RESULT,
        'Sequence Duplication Levels': PASS_RESULT,
        'Overrepresented sequences': FAIL_RESULT,
        'Kmer Content': FAIL_RESULT,
    }

    def setUp(self):
        self.file = "examples/basic.txt"
        self.parser = FastQCParser(self.file)

    def test_version(self):
        self.assertEqual(self.parser.version, '0.10.1')

    def test_modules_present(self):
        self.assertItemsEqual(self.parser.modules.keys(), self.expected_results.keys())

    def test_module_results(self):
        for module in self.expected_results.keys():
            self.assertEqual(self.expected_results[module], self.parser.module_results[module])

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "fastqc_parser" ).setLevel( logging.DEBUG )
    unittest.main()
