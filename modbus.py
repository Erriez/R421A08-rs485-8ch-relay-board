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

##
# 8 Channel RS485 RTU relay board type R421A08.
#
# This is a Python commandline example to monitor and send MODBUS commands by using a USB - RS485
# dongle.
#
# Python 2.7 and Python 3.6 are supported.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import argparse
import sys

from print_stderr import print_stderr
import relay_modbus


# Typical MODBUS baudrates are 9600 or 19200
DEFAULT_BAUDRATE = 9600

# Maximum number of monitor address counting from 0
NUM_ADDRESSES = 64


def modbus_cmd_monitor(args):
    """
        MODBUS monitor command: Print receiving frames on the serial console.
    :param args: Commandline arguments
    :return: None
    """

    # Create MODBUS object
    _modbus = relay_modbus.Modbus(args.serial_port, baud_rate=args.baudrate)
    _modbus.open()

    # Start monitoring
    _modbus.monitor_start(args.address)


def modbus_cmd_send(args):
    """
        MODBUS send command
    :param args: Commandline arguments
    :return: None
    """

    # Create MODBUS object
    _modbus = relay_modbus.Modbus(args.serial_port, baud_rate=args.baudrate, verbose=True)
    try:
        _modbus.open()
    except relay_modbus.SerialOpenException:
        print_stderr('Error: Cannot open serial port: ' + args.serial_port)
        sys.exit(1)

    tx_data = None
    try:
        tx_str = args.frame

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
        sys.exit(1)

    # Send and receive MODBUS frame
    _modbus.transfer(tx_data, not args.no_append_crc, rx_length=0)


def check_address_type(address):
    """
        Check address type argument
    :param address: Address
    :return: Address argument
    """
    errors = False

    try:
        address = int(address)
    except ValueError:
        errors = True

    if address >= NUM_ADDRESSES:
        errors = True

    if errors:
        raise argparse.ArgumentTypeError(
            "Valid addresses: 0..{}".format(NUM_ADDRESSES - 1))

    return address


def argument_parser(args):
    """
        Argument parse
    :param args: Commandline arguments
    :return: Return value of _parser.parse_args()
    """

    # ----------------------------------------------
    # Description and help strings
    description = \
        'Python script to monitor/send RS485 MODBUS commands v{}.'.format(relay_modbus.VERSION)

    # ----------------------------------------------
    help_serial_port = \
        'Serial port (such as COM1 or /dev/ttyUSB0)'
    help_baudrate = \
        'Serial baudrate (Default: {})'.format(DEFAULT_BAUDRATE)

    # ----------------------------------------------
    help_monitor = \
        'Monitor and print receiving frames'
    help_monitor_address = \
        'Address of the board [0..{}] (Set DIP switches)'. format(NUM_ADDRESSES - 1)

    # ----------------------------------------------
    help_send = \
        'Send MODBUS frame'
    help_send_frame = \
        'ASCII frame, for example: ":010600010100" or "01 06 00 01 01 00" or ' \
        '"0x01, 0x06, 0x00, 0x01, 0x01, 0x00". CRC is automatically added to the end of the ' \
        'frame, or can be omitted with the--no-append-crc option.'
    help_send_no_crc_append = \
        'Do not append CRC at the end of <FRAME>'

    # ----------------------------------------------------------------------------------------------
    # Create argument parser
    _parser = argparse.ArgumentParser(description=description)

    # Serial port argument is always required
    _parser.add_argument('serial_port',
                         metavar='<SERIAL_PORT>',
                         type=str,
                         help=help_serial_port)

    # Serial port baudrate is optional
    _parser.add_argument('-b', '--baudrate',
                         metavar='<BAUDRATE>',
                         type=int,
                         default=DEFAULT_BAUDRATE,
                         help=help_baudrate)

    # ----------------------------------------------------------------------------------------------
    # Create sub command arguments
    _subparsers = _parser.add_subparsers(help='MODBUS command')

    # ----------------------------------------------------------------------------------------------
    # MODBUS monitor command
    _parser_monitor = _subparsers.add_parser('monitor', help=help_monitor)

    _parser_monitor.add_argument('-a', '--address',
                                 metavar='<ADDRESS>',
                                 default='0',
                                 type=check_address_type,
                                 help=help_monitor_address)

    _parser_monitor.set_defaults(func=modbus_cmd_monitor)

    # ----------------------------------------------------------------------------------------------
    # Send raw MODBUS command
    _parser_send = _subparsers.add_parser('send', help=help_send)

    _parser_send.add_argument('frame', metavar='<FRAME>', type=str, help=help_send_frame)

    _parser_send.add_argument('-n', '--no-append-crc',
                              action='store_true',
                              default=False,
                              help=help_send_no_crc_append)

    _parser_send.set_defaults(func=modbus_cmd_send)

    # ----------------------------------------------------------------------------------------------
    # Parse arguments
    _args = _parser.parse_args(args)

    try:
        _args.func(_args)
    except AttributeError:
        _parser.print_help(sys.stderr)
        sys.exit(1)


def main():
    """
        Main function, including argument parser
    :return: None
    """

    # Argument parser
    argument_parser(sys.argv[1:])

    print('Done')


if __name__ == '__main__':
    main()
