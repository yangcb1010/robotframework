import sys
from os import remove
from os.path import exists
import unittest
from StringIO import StringIO


class RunningTestCase(unittest.TestCase):

    remove_files = []

    def setUp(self):
        self.orig__stdout__ = sys.__stdout__
        self.orig__stderr__ = sys.__stderr__
        self.orig_stdout = sys.stdout
        self.orig_stderr = sys.stderr
        sys.__stdout__ = StringIO()
        sys.__stderr__ = StringIO()
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        self._remove_files()

    def tearDown(self):
        sys.__stdout__ = self.orig__stdout__
        sys.__stderr__ = self.orig__stderr__
        sys.stdout = self.orig_stdout
        sys.stderr = self.orig_stderr
        self._remove_files()

    def _assert_outputs(self, stdout=None, stderr=None):
        self._assert_output(sys.__stdout__, stdout)
        self._assert_output(sys.__stderr__, stderr)
        self._assert_output(sys.stdout, None)
        self._assert_output(sys.stderr, None)

    def _assert_output(self, stream, expected):
        output = stream.getvalue()
        if expected:
            self._assert_output_contains(output, expected)
        else:
            self._assert_no_output(output)

    def _assert_no_output(self, output):
        if output:
            raise AssertionError('Expected output to be empty:\n%s' % output)

    def _assert_output_contains(self, output, expected):
        for content, count in expected:
            if output.count(content) != count:
                raise AssertionError("'%s' not %d times in output:\n%s"
                                     % (content, count, output))

    def _remove_files(self):
        for path in self.remove_files:
            if exists(path):
                remove(path)
