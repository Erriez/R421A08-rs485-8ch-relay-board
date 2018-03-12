#!/usr/bin/python3

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
# 8 Channel RS485 RTU relay board type R421A08.
#
# This is a Python example to control the relay board with a USB - RS485 dongle.
# Python 2.7 and Python 3.6 are supported.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import argparse
import serial
import sys
import time

# Fixed number of relays on the R421A08 board
NUM_RELAYS = 8

# Commands
CMD_ON = 0x01
CMD_OFF = 0x02
CMD_TOGGLE = 0x03
CMD_LATCH = 0x04
CMD_MOMENTARY = 0x05
CMD_DELAY = 0x06
CMD_READ_STATUS = 0x07

# According to MODBUS specification:
# Wait at least 3.5 char between frames
# However, some USB - RS485 dongles requires at least 10ms to switch between TX and RX, so use a
# save delay between frames
FRAME_DELAY = 0.010

# R421A08 supports MODBUS control command and read status only
FUNCTION_CONTROL_COMMAND = 0x06
FUNCTION_READ_STATUS = 0x03

# Fixed receive frame length
RX_LEN_CONTROL_COMMAND = 8
RX_LEN_READ_STATUS = 7

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


def modbus_crc(data):
    """
        brief Calculate MODBUS crc
    :param data: Data
    :return: List CRC high Byte, CRC low Byte
    """
    crc_high = 0xFF
    crc_low = 0xFF

    for i in range(0, len(data)):
        index = crc_high ^ data[i]
        crc_high = crc_low ^ CRC_HI[index]
        crc_low = CRC_LOW[index]

    return [crc_high, crc_low]


def print_frame(msg, data):
    """
        Print frame
    :param msg: Message before the data
    :param data: List data (int)
    :return: None
    """
    line = '%s %d: ' % (msg, len(data))
    for i in range(0, len(data)):
        if line:
            line += ' '
        line += '%02X' % data[i]
    print(line)


def modbus_send(ser, tx_data, verbose=False):
    """
        MODBUS send
    :param ser: Serial
    :param tx_data: List data (int)
    :param verbose: Print TX frame
    :return: None
    """
    # Print transmit frame
    if verbose:
        print_frame('TX', tx_data)

    # Write binary command to relay card over serial port
    try:
        ser.write(tx_data)
    except serial.SerialTimeoutException:
        print('TX error: Serial write timeout')
    except serial.SerialException:
        print('TX error: Serial write failed')

    # Wait between transmitting frames
    time.sleep(FRAME_DELAY)


def modbus_receive(ser, rx_length, verbose=False):
    """
        MODBUS receive
    :param ser: Serial
    :param rx_length: Receive length
    :param verbose: Print RX frame
    :return: List received data (int)
    """
    # Read response with timeout
    rx_data = None
    try:
        if rx_length:
            rx_data = ser.read(rx_length)
        else:
            # Wait for response without known receive length
            time.sleep(0.050)
            rx_data = ser.read_all()
    except serial.SerialException:
        print('RX error: Serial read failed')

    # Check read timeout
    if rx_data:
        # Convert bytearray to list
        if sys.version_info[0] >= 3:
            # Python 3 and higher
            rx_data = [int(i) for i in rx_data]
        else:
            # Python 2 and lower
            rx_data = [ord(i) for i in rx_data]

        # Print receive frame
        if verbose:
            print_frame('RX', rx_data)

        # Check response: TX data must be the same as RX data
        if rx_length and len(rx_data) != rx_length:
            print('RX error: Incorrect receive length {} Bytes, expected {} Bytes.'.format(
                len(rx_data),
                rx_length))
    else:
        print('RX error: Receive timeout')

    return rx_data


def modbus_listen(ser, address):
    """
        Listen for incoming packages in an endless loop
    :param ser: Serial
    :param address:
        0: Print all addresses
        1..255: Print address only
    :return: None
    """
    ser.timeout = FRAME_DELAY
    rx_data = []
    while 1:
        c = ser.read(1)
        if c:
            rx_data.append(ord(c))
        if rx_data and not c:
            if not address or rx_data[0] == address:
                print_frame('RX', rx_data)
            rx_data = []


def send_relay_command(ser, address, relay, cmd, delay=0, verbose=False):
    """
        Send relay control
    :param ser: Serial
    :param address: Address
    :param relay: Relay number
    :param cmd: Command
    :param delay: Optional delay
    :param verbose: Print verbose messages
    :return: List response (int)
    """
    # Create binary control command
    tx_data = [
        address,                    # Slave address of the relay board 0..63
        FUNCTION_CONTROL_COMMAND,   # Read status is always 0x03
        0x00, relay,                # Relay 0x0001..0x0008
        cmd,                        # Command 0x01..0x06
        delay                       # Delay 0x00..0xFF
    ]
    # Append CRC to transmit frame
    tx_data += modbus_crc(tx_data)

    # Send command
    modbus_send(ser, tx_data, verbose)

    # Wait for response with timeout
    return modbus_receive(ser, RX_LEN_CONTROL_COMMAND, verbose)


def read_relay_status(ser, address, relay, verbose=False):
    """
        Read relay status
    :param ser: Serial
    :param address: Address
    :param relay: Relay number
    :param verbose: Print verbose messages
    :return:
        0: Relay off
        1: Relay on
        -1: An error occurred
    """
    # Create binary read status
    tx_data = [
        address,                # Slave address of the relay board 0..63
        FUNCTION_READ_STATUS,   # Read status is always 0x03
        0x00, relay,            # Relay 0x0001..0x0008
        0x00, 0x01              # Number of bytes is always 0x0001
    ]

    # Append CRC
    tx_data += modbus_crc(tx_data)

    # Send command and wait for response with timeout
    modbus_send(ser, tx_data, verbose)

    # Wait for response with timeout
    rx_data = modbus_receive(ser, RX_LEN_READ_STATUS, verbose)

    if rx_data and len(rx_data) > 2:
        # Check CRC
        data_no_crc = rx_data[:-2]
        crc = rx_data[-2:]
        if modbus_crc(data_no_crc) != crc:
            print('RX error: Incorrect CRC received')
        elif rx_data[0] != tx_data[0]:
            print('RX error: Incorrect address received')
        elif rx_data[1] != tx_data[1]:
            print('RX error: Incorrect function received')
        elif rx_data[2] != 2:
            print('RX error: Incorrect data length received')
        elif rx_data[3] != 0:
            print('RX error: Incorrect data high Byte received')
        elif rx_data[4] != 0 and rx_data[4] != 1:
            print('RX error: Incorrect data low Byte received')
        else:
            return rx_data[4]

    return -1


def check_relay_numbers(relays):
    """
        Check for valid relay numbers. Exit when errors found.
    :param relays: List relay numbers (int)
    :return: None
    """
    errors = False
    for relay in relays:
        if relay < 1 or relay > NUM_RELAYS:
            errors = True
            print('Incorrect relay number: {}'.format(relay))
    if errors:
        sys.exit(1)


def modbus_send_str(ser, tx_str, add_crc_to_frame=True):
    """
        Send raw ASCII hex string
    :param ser: Serial
    :param tx_str: Transmit string
    :param add_crc_to_frame:
        True: Append CRC to frame
        False: Do not append CRC
    :return:
        List receive Bytes
        None: Failure
    """
    try:
        # Replace characters, for example:
        #   ':010600010100D99A' -> '010600010100D99A'
        #   '0x01, 0x06, 0x00, 0x01, 0x01, 0x00, 0xD9, 0x9A' -> '01 06 00 01 01 00 D9 9A'
        for c in ['0x', ':', ',', ' ']:
            tx_str = tx_str.replace(c, '')

        # Insert space every 2 characters, for example:
        #   '010600010100D99A' -> '01 06 00 01 01 00 D9 9A'
        tx_str = ' '.join(a + b for a, b in zip(tx_str[::2], tx_str[1::2]))

        # Split data in ints, for example:
        #   [0x01, 0x06, 0x00, 0x01, 0x01, 0x00, 0xD9, 0x9A]
        tx_data = [int(i, 16) for i in tx_str.split(' ')]
    except ValueError:
        print('Incorrect send argument. Expecting --send formats like:')
        print('  ":010600010100"')
        print('  "01 06 00 01 01 00"')
        print('  "0x01, 0x06, 0x00, 0x01, 0x01, 0x00"')
        print('Note: CRC bytes can be omitted.')
        return

    # Add CRC only when not equal to last two Bytes of the transmit frame
    if add_crc_to_frame:
        tx_data += modbus_crc(tx_data)

    # Transmit and receive frame
    modbus_send(ser, tx_data, verbose=True)
    return modbus_receive(ser, 0, verbose=True)


def main():
    """
        Main function, including argument parser
    :return: None
    """

    # Argument parser
    _parser = argparse.ArgumentParser(description='8 Channel RS485 RTU relay board type R421A08')
    _parser.add_argument('SERIAL_PORT',
                         help='Serial port (such as COM1 or /dev/ttyUSB0)')
    _parser.add_argument('ADDRESS',
                         type=int,
                         help='Slave address [0..63]')

    _parser.add_argument('-v', '--verbose',
                         action='store_true',
                         help='Print verbose')
    _parser.add_argument('-i', '--listen',
                         action='store_true',
                         help='Listen on receive')
    _parser.add_argument('-r', '--relay',
                         nargs='*',
                         help='Relay numbers [1..8] or * for all relays')
    _parser.add_argument('-s', '--status',
                         action='store_true',
                         help='Read status')
    _parser.add_argument('-1', '--on',
                         action='store_true',
                         help='On')
    _parser.add_argument('-0', '--off',
                         action='store_true',
                         help='Off')
    _parser.add_argument('-t', '--toggle',
                         action='store_true',
                         help='Toggle')
    _parser.add_argument('-l', '--latch',
                         action='store_true',
                         help='Latch')
    _parser.add_argument('-m', '--momentary',
                         action='store_true',
                         help='Momentary')
    _parser.add_argument('-d', '--delay',
                         type=int,
                         help='Delay (0..255 seconds)')
    _parser.add_argument('--send',
                         type=str,
                         metavar='FRAME',
                         help='Transmit MODBUS frame in ASCII hex, such as ":010600010100" or '
                              '"01 06 00 01 01 00" or "0x01, 0x06, 0x00, 0x01, 0x01, 0x00". CRC is '
                              'automatically added to the end of the frame.')
    _parser.add_argument('-n', '--no-crc',
                         action='store_true',
                         help='Do not add CRC to --send frame')
    args = _parser.parse_args()

    # Get arguments
    serial_port = args.SERIAL_PORT
    address = args.ADDRESS
    relays = None
    if args.relay:
        if args.relay == ['*']:
            # Convert * to relay int numbers
            relays = [relay for relay in range(1, NUM_RELAYS + 1)]
        else:
            # Convert relay arguments to int
            relays = list(map(int, args.relay))
        check_relay_numbers(relays)
    delay = 0
    verbose = args.verbose

    # Create serial
    ser = serial.Serial()
    ser.port = serial_port
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.stopbits = 1
    ser.parity = serial.PARITY_NONE
    ser.timeout = 0.1

    # Open serial port
    try:
        ser.open()
    except serial.SerialException:
        print('Error: Cannot open serial port: ' + ser.port)
        sys.exit(1)

    cmd = None
    if args.listen:
        if address == 0:
            print('Listening for all incoming frames.')
        else:
            print('Listening for incoming frames from address {}.'.format(address))
        print('Press CTRL+C to abort.')
        modbus_listen(ser, address)
    else:
        if args.status:
            cmd = CMD_READ_STATUS
        elif args.on:
            cmd = CMD_ON
            print('Turn relay(s) {} on...'.format(relays))
        elif args.off:
            cmd = CMD_OFF
            print('Turn relay(s) {} off...'.format(relays))
        elif args.toggle:
            cmd = CMD_TOGGLE
            print('Toggle relay(s) {}...'.format(relays))
        elif args.latch:
            cmd = CMD_LATCH
            print('Latch relay(s) {}...'.format(relays))
        elif args.momentary:
            cmd = CMD_MOMENTARY
            print('Turn relay(s) {} on/off...'.format(relays))
        elif args.delay:
            cmd = CMD_DELAY
            delay = args.delay
            print('Turn relay(s) {} on/off with delay {} sec...'.format(relays, delay))
        elif args.send:
            add_crc_to_frame = True
            if args.no_crc:
                add_crc_to_frame = False
            retval = modbus_send_str(ser, args.send, add_crc_to_frame)
            if len(retval):
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print('Error: No command option specified')
            sys.exit(1)

    # Send command
    if cmd == CMD_READ_STATUS:
        for relay in list(relays):
            status = read_relay_status(ser,
                                       address=address,
                                       relay=relay,
                                       verbose=verbose)
            if status == 1:
                status_str = 'ON'
            elif status == 0:
                status_str = 'OFF'
            else:
                status_str = 'UNKNOWN'
            print('Relay {}: {}'.format(relay, status_str))
    else:
        for relay in list(relays):
            send_relay_command(ser,
                               address=address,
                               relay=relay,
                               cmd=cmd,
                               delay=delay,
                               verbose=verbose)


if __name__ == '__main__':
    main()
