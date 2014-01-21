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
            self._parse_module(line)
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

    def _parse_module(self, line):

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

        self.modules[modulename] = {'raw_content': "".join(content)}

        return
