#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2018 Erriez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import sys
import unittest
from contextlib import contextmanager

import relay

try:
    if sys.version_info[0] >= 3:
        from io import StringIO
    else:
        from StringIO import StringIO
except ImportError as import_err:
    print(str(import_err))
    sys.exit(1)


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class RelayBoardOffTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._serial_port = str(os.environ['RELAY_SERIAL_PORT'])
        cls._address = str(os.environ['RELAY_ADDRESS'])
        cls._commands = ['on', 'off', 'toggle', 'latch', 'momentary', 'delay']

    @classmethod
    def tearDownClass(cls):
        with captured_output() as (out, err):
            relay.argument_parser([cls._serial_port, cls._address, 'off', '*'])

    def test_invalid_relay(self):
        for relay_id in ['0', '9', '10']:
            for cmd in self._commands:
                with captured_output() as (out, err):
                    with self.assertRaises(SystemExit):
                        relay.argument_parser([self._serial_port,
                                               self._address,
                                               cmd,
                                               relay_id])
                    output_stdout = out.getvalue().strip()
                    output_stderr = err.getvalue().strip()
                    self.assertEqual(output_stdout, '')
                    self.assertGreaterEqual(len(output_stderr), 1)

    def test_valid_address(self):
        for address in ['0', '63']:
            if address != str(self._address):
                for cmd in self._commands:
                    with captured_output() as (out, err):
                        relay.argument_parser([self._serial_port, address, cmd, '1'])
                        output_stdout = out.getvalue().strip()
                        output_stderr = err.getvalue().strip()
                        self.assertEqual(output_stdout, 'Relay 1 {}...'.format(cmd))
                        self.assertEqual(output_stderr, 'RX error: Receive timeout')

    def test_invalid_address(self):
        for cmd in self._commands:
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit):
                    relay.argument_parser([self._serial_port, '65', cmd, '1'])
                output_stdout = out.getvalue().strip()
                output_stderr = err.getvalue().strip()
                self.assertEqual(output_stdout, '')
                self.assertGreaterEqual(len(output_stderr), 1)

    def test_relay_1(self):
        for cmd in self._commands:
            with captured_output() as (out, err):
                relay.argument_parser([self._serial_port, self._address, cmd, '1'])
                output = out.getvalue().strip()
                self.assertEqual(output, 'Relay 1 {}...'.format(cmd))

    def test_relay_2(self):
        for cmd in self._commands:
            with captured_output() as (out, err):
                relay.argument_parser([self._serial_port, self._address, cmd, '2'])
                output = out.getvalue().strip()
                self.assertEqual(output, 'Relay 2 {}...'.format(cmd))

    def test_relay_8(self):
        for cmd in self._commands:
            with captured_output() as (out, err):
                relay.argument_parser([self._serial_port, self._address, cmd, '8'])
                output = out.getvalue().strip()
                self.assertEqual(output, 'Relay 8 {}...'.format(cmd))

    def test_relay_all(self):
        for cmd in self._commands:
            with captured_output() as (out, err):
                relay.argument_parser([self._serial_port, self._address, cmd, '*'])
                output = out.getvalue().strip()
                self.assertEqual(output, 'All relays {}...'.format(cmd))

    def test_relay_status(self):
        relay.argument_parser([self._serial_port, self._address, 'off', '*'])
        with captured_output() as (out, err):
            relay.argument_parser([self._serial_port, self._address, 'status', '*'])
            output = out.getvalue().strip()
            expected = \
                'Status relays:\n' \
                '  Relay 1: OFF\n' \
                '  Relay 2: OFF\n' \
                '  Relay 3: OFF\n' \
                '  Relay 4: OFF\n' \
                '  Relay 5: OFF\n' \
                '  Relay 6: OFF\n' \
                '  Relay 7: OFF\n' \
                '  Relay 8: OFF'
            self.assertEqual(output, expected)
