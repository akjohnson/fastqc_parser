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
        self.parser = FastQCParser(filename = self.file)

    def test_version(self):
        self.assertEqual(self.parser.version, '0.10.1')

    def test_modules_present(self):
        self.assertItemsEqual(self.parser.modules.keys(), self.expected_results.keys())

    def test_module_results(self):
        for module in self.expected_results.keys():
            self.assertEqual(self.expected_results[module], self.parser.module_results[module])

    def test_basic_statistics(self):
        table = self.parser.get_module_table('Basic Statistics')

        self.assertIsNotNone(table)

        self.assertEqual(table[0]['Measure'], 'Filename')
        self.assertEqual(table[0]['Value'], 'ExampleSample_ATCGTC_L005_R1_001.fastq.gz')

        self.assertEqual(table[1]['Measure'], 'File type')
        self.assertEqual(table[1]['Value'], 'Conventional base calls')

        self.assertEqual(table[2]['Measure'], 'Encoding')
        self.assertEqual(table[2]['Value'], 'Sanger / Illumina 1.9')

        self.assertEqual(table[3]['Measure'], 'Total Sequences')
        self.assertEqual(table[3]['Value'], '22068720')

        self.assertEqual(table[4]['Measure'], 'Filtered Sequences')
        self.assertEqual(table[4]['Value'], '5853084')

        self.assertEqual(table[5]['Measure'], 'Sequence length')
        self.assertEqual(table[5]['Value'], '36')

        self.assertEqual(table[6]['Measure'], '%GC')
        self.assertEqual(table[6]['Value'], '48')

        headers = self.parser.get_module_table_headers('Basic Statistics')
        self.assertItemsEqual(['Measure', 'Value'], headers)

class TestContentParsing(TestBasicParsing):
"""Run the same tests as above, except on passed content instead of a file loaded."""

    def setUp(self):
        self.file = "examples/basic.txt"
        content = open(self.file, 'r').read()
        self.parser = FastQCParser(content = content) 

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "fastqc_parser" ).setLevel( logging.DEBUG )
    unittest.main()
