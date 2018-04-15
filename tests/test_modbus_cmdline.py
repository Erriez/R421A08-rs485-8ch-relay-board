import os
import sys
import unittest
from contextlib import contextmanager

import modbus

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

    def test_modbus_send_ascii(self):
        with captured_output() as (out, err):
            modbus.argument_parser([self._serial_port, 'send', ':010600010100'])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 01 00 D9 9A\n'
                             'RX  8 Bytes:  01 06 00 01 01 00 D9 9A')

    def test_modbus_send_hex_spaces(self):
        with captured_output() as (out, err):
            modbus.argument_parser([self._serial_port, 'send', '01 06 00 01 03 00'])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 03 00 D8 FA\n'
                             'RX  8 Bytes:  01 06 00 01 03 00 D8 FA')

    def test_modbus_send_hex_comma(self):
        with captured_output() as (out, err):
            modbus.argument_parser([self._serial_port,
                                            'send',
                                            '0x01, 0x06, 0x00, 0x01, 0x02, 0x00'])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 02 00 D9 6A\n'
                             'RX  8 Bytes:  01 06 00 01 02 00 D9 6A')

    def test_modbus_send_ascii_no_append_crc(self):
        with captured_output() as (out, err):
            modbus.argument_parser([self._serial_port,
                                            'send',
                                            ':010600010100D99a',
                                            '--no-append-crc'])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 01 00 D9 9A\n'
                             'RX  8 Bytes:  01 06 00 01 01 00 D9 9A')

    def test_modbus_send_hex_spaces_no_append_crc(self):
        with captured_output() as (out, err):
            modbus.argument_parser([self._serial_port,
                                            'send',
                                            '01 06 00 01 03 00 D8 fa',
                                            '--no-append-crc'])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 03 00 D8 FA\n'
                             'RX  8 Bytes:  01 06 00 01 03 00 D8 FA')

    def test_modbus_send_hex_comma_no_append_crc(self):
        with captured_output() as (out, err):
            modbus.argument_parser([self._serial_port,
                                            'send',
                                            '0x01, 0x06, 0x00, 0x01, 0x02, 0x00, 0xD9, 0x6a',
                                            '--no-append-crc'])
            output = out.getvalue().strip()
            self.assertEqual(output,
                             'TX  8 Bytes:  01 06 00 01 02 00 D9 6A\n'
                             'RX  8 Bytes:  01 06 00 01 02 00 D9 6A')

    def test_modbus_send_hex_invalid_string(self):
        with captured_output() as (out, err):
            with self.assertRaises(SystemExit) as cm:
                modbus.argument_parser([self._serial_port, 'send', '0xZZ'])
            self.assertEquals(cm.exception.code, 1)
            output = str(out.getvalue().strip())
            self.assertTrue(output.startswith('Incorrect send argument'))

    def test_modbus_send_wrong_serial_port(self):
        with captured_output() as (out, err):
            serial_port = 'WRONG'
            with self.assertRaises(SystemExit) as cm:
                modbus.argument_parser([serial_port,
                                                'send',
                                                '0x01, 0x06, 0x00, 0x01, 0x02, 0x00'])
            self.assertEquals(cm.exception.code, 1)
            output = out.getvalue().strip()
            self.assertEquals(output, '')
            output = err.getvalue().strip()
            self.assertEquals(output, 'Error: Cannot open serial port: {}'.format(serial_port))
