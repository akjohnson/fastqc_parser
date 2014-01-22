import re
import logging

log = logging.getLogger(__name__)

PASS_RESULT="pass"
WARN_RESULT="warn"
FAIL_RESULT="fail"

RESULTS = {
  PASS_RESULT: PASS_RESULT,
  WARN_RESULT: WARN_RESULT,
  FAIL_RESULT: FAIL_RESULT
}

class FastQCParser(object):

    def __init__(self, filename):

        self.modules = dict()
        self.module_results = dict()
        self.input = open(filename, 'r')
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

        header = lines[0]

        if not header.startswith("#"):
            log.error("Header does not start with # for %s content" % modulename) 
            return None

        header_values = header.lstrip("#").rstrip().split("\t")

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
