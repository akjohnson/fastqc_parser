from __future__ import unicode_literals

import re
import logging
import StringIO

from decimal import Decimal

log = logging.getLogger(__name__)

PASS_RESULT="pass"
WARN_RESULT="warn"
FAIL_RESULT="fail"

RESULTS = {
    PASS_RESULT: PASS_RESULT,
    WARN_RESULT: WARN_RESULT,
    FAIL_RESULT: FAIL_RESULT
}

EXPECTED_MODULES = [
    "Basic Statistics",
    "Per base sequence quality",
    "Per sequence quality scores",
    "Per base sequence content",
    "Per base GC content",
    "Per sequence GC content",
    "Per base N content",
    "Sequence Length Distribution",
    "Sequence Duplication Levels",
    "Overrepresented sequences",
    "Kmer Content",
]

class FastQCParser(object):

    def __init__(self, filename = None, content = None):
        
        self.modules = dict()
        self.module_results = dict()

        if filename:
            self.input = open(filename, 'r')
        elif content:
            self.input = StringIO.StringIO(content)
        else:
            raise ValueError('FastQCParser requires a filename or content')

        self._parse()
        self.input.close()

    def _parse(self):

        self._parse_version()

        line = self.input.readline()
        while line:
            self._parse_module_content(line)
            line = self.input.readline()

    def _parse_version(self):

        line = self.input.readline().strip()
        m = re.match('##FastQC\t(?P<version>[0-9a-z.]+)', line)

        if m:
            self.version = m.group('version')
            log.debug("Version: %s" % self.version)
        else:
            self.version = None
            log.error("Could not find version")

        return

    def _parse_module_content(self, line):

        m = re.match('>>(?P<modulename>[-a-zA-Z 0-9%]+)\t(?P<result>pass|warn|fail)', line)

        if not m:
            log.error("Could not find module name for %s" % line)
            return

        modulename = m.group('modulename')
        result = m.group('result')

        log.debug("Module: %s (%s)" % (modulename, result))

        # ensure we are using the values defined as constants
        self.module_results[modulename] = RESULTS[result]

        content = []

        line = self.input.readline()
        while not line.startswith(">>END_MODULE"):
            content.append(line)
            line = self.input.readline()

        self.modules[modulename] = {'raw_content': content}

        return

    def _parse_module_table(self, modulename):

        if not modulename in self.modules:
            log.error("%s does not exist in modules list" % modulename)
            return None

        lines = self.modules[modulename]['raw_content'] 
        
        # some modules that pass end up having no data; return early
        if len(lines) == 0:
            return None

        infolines = []

        # gather up all information lines because of Sequence Duplication Levels
        for line in lines:
            if line.startswith("#"):
                infolines.append(line)
            else:
                break

        if not infolines:
            log.error("Header does not exist for %s content" % modulename) 
            return None

        infovalues = {}

        if len(infolines) > 1:
            for infoline in infolines[:-1]:
                values = infoline.lstrip("#").rstrip().split("\t")
                infovalues[values[0]] = values[1]
                 
        self.modules[modulename]['info_values'] = infovalues

        # table header is always the last infoline
        header = infolines[-1]
        header_values = header.lstrip("#").rstrip().split("\t")
        self.modules[modulename]['table_headers'] = header_values

        table = list()

        for values in lines[1:]:
            table.append(dict(zip(header_values, values.strip().split("\t")))) 

        self.modules[modulename]['table'] = table

        return table

    def get_module_table(self, modulename):

        if 'table' in self.modules[modulename]:
            return self.modules[modulename]['table']
        else:
            return self._parse_module_table(modulename)

    def get_module_table_headers(self, modulename):

        if 'table_headers' in self.modules[modulename]:
            return self.modules[modulename]['table_headers']
        else:
            self._parse_module_table(modulename)
            return self.modules[modulename]['table_headers']

    def get_module_info_values(self, modulename):

        if 'info_values' in self.modules[modulename]:
            return self.modules[modulename]['info_values']
        else:
            self._parse_module_table(modulename)
            return self.modules[modulename]['info_values']

    def get_total_percent_overrepresented_sequences(self):

        overrepresented_sequences = self.get_module_table("Overrepresented sequences")

        total = Decimal('0.0')

        if not overrepresented_sequences:
            return total

        for row in overrepresented_sequences:
           total += Decimal(row['Percentage'])

        return total 
