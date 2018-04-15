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
import time
import unittest
from contextlib import contextmanager

import relay_modbus

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
        cls._serial_port = os.environ['RELAY_SERIAL_PORT']
        cls._serial_port_monitor = os.environ['RELAY_SERIAL_PORT_MONITOR']
        cls._address = int(os.environ['RELAY_ADDRESS'])

    def test_modbus_check_properties(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        self.assertEqual(modbus_test.serial_port, self._serial_port)
        self.assertEqual(modbus_test.baudrate, 9600)

    def test_crc(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        self.assertListEqual(modbus_test.crc([]), [0xFF, 0xFF])
        self.assertListEqual(modbus_test.crc([0x00]), [0xBF, 0x40])
        self.assertListEqual(modbus_test.crc([0x12, 0x34, 0x56, 0x67]), [0x3A, 0xD8])
        self.assertListEqual(modbus_test.crc([0x12, 0x34, 0x56, 0x67, 0x3A, 0xD8]), [0x00, 0x00])

    def test_crc_no_argument(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        self.assertRaises(TypeError, modbus_test.crc)

    def test_crc_invalid_type(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        self.assertRaises(AssertionError, modbus_test.crc, 0x00)

    def test_send_receive(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        tx_data = [0x01, 0x06, 0x00, 0x01, 0x01, 0x00]

        modbus_test.send(tx_data)
        rx_data = modbus_test.receive(len(tx_data))

        self.assertListEqual(tx_data, rx_data[:len(tx_data)])

    def test_send_receive_no_append_crc(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        tx_data = [0x01, 0x06, 0x00, 0x01, 0x02, 0x00, 0xD9, 0x6A]

        modbus_test.send(tx_data, append_crc_to_frame=False)
        rx_data = modbus_test.receive(len(tx_data))

        self.assertListEqual(tx_data, rx_data)

    def test_send_no_data(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        self.assertRaises(AssertionError, modbus_test.send, None)

    def test_send_verbose(self):
        modbus_verbose = relay_modbus.Modbus(self._serial_port, verbose=True)
        modbus_verbose.open()

        with captured_output() as (out, err):
            modbus_verbose.send([0x01, 0x06, 0x00, 0x01, 0x01, 0x00])
            output = out.getvalue().strip()
            self.assertEqual(output, 'TX  8 Bytes:  01 06 00 01 01 00 D9 9A')

    def test_transfer_verbose(self):
        modbus_verbose = relay_modbus.Modbus(self._serial_port, verbose=True)
        modbus_verbose.open()

        with captured_output() as (out, err):
            modbus_verbose.transfer([0x01, 0x06, 0x00, 0x01, 0x01, 0x00])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 01 00 D9 9A\n'
                             'RX  8 Bytes:  01 06 00 01 01 00 D9 9A')

    def test_receive_timeout(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        with captured_output() as (out, err):
            errmsg = None
            try:
                modbus_test.receive(100)
            except relay_modbus.TransferException as err:
                errmsg = str(err)
            self.assertEqual(errmsg, 'RX error: Receive timeout')

    def test_transfer_timeout(self):
        modbus_test = relay_modbus.Modbus(self._serial_port, verbose=False)
        modbus_test.open()

        with captured_output() as (out_, err_):
            errmsg = None
            try:
                modbus_test.transfer([0x01], rx_length=100)
            except relay_modbus.TransferException as err:
                errmsg = str(err)
            self.assertEqual(errmsg, 'RX error: Receive timeout')

    def test_monitor(self):
        modbus_send = relay_modbus.Modbus(self._serial_port)
        modbus_monitor = relay_modbus.Modbus(self._serial_port_monitor)

        modbus_send.open()
        modbus_monitor.open()

        for address in [0, self._address]:
            with captured_output() as (out, err):
                # Start monitor
                modbus_monitor.monitor_start(address, blocking=False)

                # Send message
                modbus_send.send([0x01, 0x06, 0x00, 0x01, 0x01, 0x00])

                # Wait some time to process the frame
                time.sleep(0.1)

                # Stop monitor
                modbus_monitor.monitor_stop()

                if address == 0:
                    msg_start = 'Monitor receiving frames from all addresses.'
                else:
                    msg_start = 'Monitor receiving frames from address {} only.'.format(address)

                # Check stdout
                output = out.getvalue().strip()
                self.assertEqual(output,
                                 '{}\n'
                                 'Press CTRL+C to abort.\n'
                                 'RX 16 Bytes:  01 06 00 01 01 00 D9 9A 01 06 00 01 01 00 D9 9A'.
                                 format(msg_start))

                # Wait for test completion
                time.sleep(0.05)
