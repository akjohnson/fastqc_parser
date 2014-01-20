import re
import logging

log = logging.getLogger(__name__)
 
class FastQCParser(object):

    def __init__(self, filename):
        self.input = open(filename, 'r')
        self._parse()
        self.input.close()

    def _parse(self):

        self._parse_version()

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
