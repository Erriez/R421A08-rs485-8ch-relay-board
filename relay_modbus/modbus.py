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

##
# This is a Simple MODBUS implementation
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import sys
import threading
import time

from print_stderr import print_stderr

try:
    import serial
except ImportError:
    print_stderr('Error: Cannot import serial from pySerial.')
    if sys.platform.startswith('linux'):
        print_stderr('To install pyserial, type:')
        if sys.version_info[0] >= 3:
            print_stderr('  sudo apt-get install python3-pip')
            print_stderr('  sudo pip3 install pyserial')
        else:
            print_stderr('  sudo python -m pip install pyserial')
    elif sys.platform.startswith('win'):
        print_stderr('To install pyserial, type:')
        print_stderr('  python.exe -m pip install pyserial')
    else:
        print_stderr('Install pySerial manually')
    sys.exit(1)


# Typical MODBUS baudrates are 9600 or 19200
DEFAULT_BAUDRATE = 9600

# According to MODBUS specification:
# Wait at least 3.5 char between frames
# However, some USB - RS485 dongles requires at least 10ms to switch between TX and RX, so use a
# save delay between frames
FRAME_DELAY = 0.025

# Frame receive timeout
FRAME_RX_TIMEOUT = 0.050

# MODBUS CRC tables
CRC_HI = [
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40
]

CRC_LOW = [
    0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06, 0x07, 0xC7, 0x05, 0xC5, 0xC4, 0x04,
    0xCC, 0x0C, 0x0D, 0xCD, 0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09, 0x08, 0xC8,
    0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A, 0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC,
    0x14, 0xD4, 0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3, 0x11, 0xD1, 0xD0, 0x10,
    0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3, 0xF2, 0x32, 0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4,
    0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A, 0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38,
    0x28, 0xE8, 0xE9, 0x29, 0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF, 0x2D, 0xED, 0xEC, 0x2C,
    0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26, 0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0,
    0xA0, 0x60, 0x61, 0xA1, 0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67, 0xA5, 0x65, 0x64, 0xA4,
    0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F, 0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68,
    0x78, 0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA, 0xBE, 0x7E, 0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C,
    0xB4, 0x74, 0x75, 0xB5, 0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71, 0x70, 0xB0,
    0x50, 0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92, 0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54,
    0x9C, 0x5C, 0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B, 0x99, 0x59, 0x58, 0x98,
    0x88, 0x48, 0x49, 0x89, 0x4B, 0x8B, 0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
    0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42, 0x43, 0x83, 0x41, 0x81, 0x80, 0x40
]


class SerialOpenException(Exception):
    pass


class TransferException(Exception):
    pass


class Modbus(object):
    """ Modbus class """

    def __init__(self, serial_port=None, baud_rate=DEFAULT_BAUDRATE, verbose=False):
        """
            Modbus constructor
        :param serial_port: Serial port such as 'COM1' on Windows and '/dev/ttyUSB0' on Linux.
        :param baud_rate: Serial baudrate
        :param verbose: Print transmit and receive frames to console
        """
        # Make sure previous prints are flushed to the console
        if sys.stderr:
            sys.stderr.flush()
        if sys.stdout:
            sys.stdout.flush()

        # Argument checks
        assert type(verbose) == bool

        # Store variables
        self._serial_port = serial_port

        # Create serial
        self._ser = serial.Serial()
        self._ser.baudrate = int(baud_rate)
        self._ser.bytesize = 8
        self._ser.stopbits = 1
        self._ser.parity = serial.PARITY_NONE
        self._ser.timeout = 0.1
        self._verbose = verbose
        self._tx_data = []
        self._rx_data = []
        self._monitor_thread = None

        # Create lock
        self._lock = threading.Lock()

    def __del__(self):
        """
            Modbus destructor
        :return: None
        """

        # Try to close the serial port gracefully with a maximum of 1 second
        for _ in range(0, 10):
            time.sleep(0.1)
            self._ser.close()
            if not self._ser.is_open:
                break

    # ----------------------------------------------------------------------------------------------
    # MODBUS properties
    # ----------------------------------------------------------------------------------------------
    @property
    def serial_port(self):
        """
            Get serial port
        :return: Serial port
        """
        return self._serial_port

    @serial_port.setter
    def serial_port(self, serial_port):
        """
            Set serial port
        :return: Serial port
        """
        if serial_port and type(serial_port) == str:
            self._serial_port = serial_port

    @property
    def baudrate(self):
        """
            Get baudrate of the serial port
        :return: Baudrate
        """
        return self._ser.baudrate

    @property
    def last_tx_frame(self):
        """
            Get last transmitted frame
        :return: Frame string
        """
        if self._tx_data:
            return get_frame_str('TX:', self._tx_data)
        else:
            return ''

    @property
    def last_rx_frame(self):
        """
            Get last received frame
        :return: Frame string
        """
        if self._rx_data:
            return get_frame_str('RX:', self._rx_data)
        else:
            return ''

    # ----------------------------------------------------------------------------------------------
    # MODBUS functions
    # ----------------------------------------------------------------------------------------------
    def open(self):
        # Open serial port
        try:
            self._ser.port = self._serial_port
            self._ser.open()
        except serial.SerialException as err:
            raise SerialOpenException('Error: Cannot open serial port: ' + str(err))

    def close(self):
        self._ser.close()

    def is_open(self):
        return self._ser.is_open

    @staticmethod
    def crc(data):
        """
            brief Calculate MODBUS crc
        :param data: Data
        :return: List CRC high Byte, CRC low Byte
        """
        assert type(data) == list

        crc_high = 0xFF
        crc_low = 0xFF

        for i in range(0, len(data)):
            index = crc_high ^ data[i]
            crc_high = crc_low ^ CRC_HI[index]
            crc_low = CRC_LOW[index]

        return [crc_high, crc_low]

    def send(self, tx_data, append_crc_to_frame=True):
        """
            MODBUS send
        :param tx_data: List data (int)
        :param append_crc_to_frame: Append CRC to TX frame
        :return: None
        """
        assert type(tx_data) == list

        self._tx_data = tx_data

        if append_crc_to_frame:
            # Append CRC to transmit frame
            self._tx_data += self.crc(self._tx_data)

        # Print transmit frame
        if self._verbose:
            print(get_frame_str('TX', self._tx_data))

        try:
            # Clear receive
            while self._ser.read_all():
                time.sleep(0.010)
        except serial.SerialException:
            # Windows: Serial exception
            raise TransferException('RX error: Read failed')
        except AttributeError:
            # Ubuntu: Attribute error (Not documented)
            raise TransferException('RX error: Read failed')

        # Write binary command to relay card over serial port
        try:
            self._ser.write(tx_data)
        except serial.SerialTimeoutException:
            raise TransferException('TX error: Serial write timeout')
        except serial.SerialException:
            raise TransferException('TX error: Serial write failed')

        # Wait between transmitting frames
        time.sleep(FRAME_DELAY)

    def receive(self, rx_length):
        """
            MODBUS receive
        :param rx_length: Receive length
        :return: List received data (int)
        """
        assert type(rx_length) == int
        if rx_length:
            assert 0 < rx_length < 255

        # Read response with timeout
        try:
            if rx_length:
                rx_data = self._ser.read(rx_length)
            else:
                # Wait for response without known receive length
                time.sleep(FRAME_RX_TIMEOUT)
                rx_data = self._ser.read_all()
        except serial.SerialException:
            raise TransferException('RX error: Serial read failed')

        # Check read timeout
        if not rx_data:
            raise TransferException('RX error: Receive timeout')

        # Convert bytearray to list
        if sys.version_info[0] >= 3:
            # Python 3 and higher
            self._rx_data = [int(i) for i in rx_data]
        else:
            # Python 2 and lower
            self._rx_data = [ord(i) for i in rx_data]

        # Print receive frame
        if self._verbose:
            print(get_frame_str('RX', self._rx_data))

        # Check response: TX data must be the same as RX data
        if rx_length and len(self._rx_data) != rx_length:
            raise TransferException('RX error: Incorrect receive length {} '
                                    'Bytes, expected {} Bytes.'.format(len(self._rx_data),
                                                                       rx_length))

        return self._rx_data

    def transfer(self, tx_data, append_crc_to_tx_frame=True, rx_length=0):
        """
            Send MODBUS frame and return receive frame with timeout
        :param tx_data:
        :param append_crc_to_tx_frame:
        :param rx_length:
        :return:
        """
        self.send(tx_data, append_crc_to_tx_frame)
        return self.receive(rx_length)

    def transfer_begin(self):
        self._lock.acquire()

    def transfer_end(self):
        self._lock.release()

    def monitor_start(self, address, blocking=True):
        """
            Snoop and print incoming frames in an endless loop
        :param address:
            0: Print all addresses
            1..255: Print address only
        :param blocking:
            True: Blocking until a user presses CTRL+C or exit terminal
            False: Not blocking for unittest
        :return: None
        """
        assert type(address) == int
        assert 0 <= address <= 255

        # Create MODBUS monitor thread
        self._monitor_thread = MonitorThread(self._ser, address)

        # Configure monitor thread s deamon to allow CTRL+C with KeyboardInterrupt event
        self._monitor_thread.daemon = True

        # Start the monitor thread
        self._monitor_thread.start()

        # Wait in an endless loop for KeyboardInterrupt when user presses CTRL+C
        # Note: The KeyboardInterrupt event can only be caught in the main thread
        try:
            while blocking and not self._monitor_thread.is_stopped:
                # Give the system idle time
                time.sleep(0.050)
        except KeyboardInterrupt:
            # User pressed CTRL+C, stop monitor thread
            self._monitor_thread.stop()

            # Wait until monitor thread exit
            self._monitor_thread.join()

    def monitor_stop(self):
        """
            Stop monitor thread
        :return: None
        """
        if self._monitor_thread:
            self._monitor_thread.stop()


def get_frame_str(msg, data):
    """
        Get frame as string
    :param msg: Message before the data
    :param data: List data (int)
    :return: None
    """
    assert type(msg) == str
    assert type(data) == list

    # Print MODBUS frame
    line = '{} {:2d} Bytes: '.format(msg, len(data))
    for i in range(0, len(data)):
        if line:
            line += ' '
        line += '{:02X}'.format(data[i])
    return line


class MonitorThread(threading.Thread):
    """ MODBUS monitor thread """

    def __init__(self, ser, address):
        super(MonitorThread, self).__init__()

        # Create stop event
        self._stop_event = threading.Event()

        # Store variables
        self._ser = ser
        self._address = address

    @property
    def is_stopped(self):
        """
           Is stop event generated
        :return:
            True: Stop event generated
            False: No stop event generated
        """
        return self._stop_event.is_set()

    def stop(self):
        """
            Stop monitor thread by generating stop event
        :return: None
        """
        self._stop_event.set()

    def run(self):
        """
            Monitor thread
        :return: None
        """

        if not self._address:
            print('Monitor receiving frames from all addresses.')
        else:
            print('Monitor receiving frames from address {} only.'.format(self._address))
        print('Press CTRL+C to abort.')

        # Set read timeout
        self._ser.timeout = FRAME_DELAY

        # Endless loop
        rx_data = []
        while not self.is_stopped and self._ser.is_open:
            try:
                # Read one Byte from serial port with read timeout
                c = self._ser.read(1)
            except serial.SerialException as err:
                if not self.is_stopped:
                    # A serial error error occurred
                    print_stderr('Error: Serial read failed')
                    print_stderr(str(err))
                    self.stop()
                break

            if c:
                # Add received data
                rx_data.append(ord(c))
            if rx_data and not c:
                # Print received frame
                if not self._address or rx_data[0] == self._address:
                    print(get_frame_str('RX', rx_data))
                rx_data = []
