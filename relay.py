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
# This is a Python example to control the relay board with a USB - RS485 dongle.
# Python 2.7 and Python 3.6 are supported.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import argparse
import sys

import serial
import relay_modbus
import relay_boards
from relay_boards.R421A08 import NUM_RELAYS as R421A08_NUM_RELAYS
from relay_boards.R421A08 import NUM_ADDRESSES as R421A08_NUM_ADDRESSES
from print_stderr import print_stderr


def get_relay_numbers(relays):
    """
        Check for valid relay numbers. Exit when errors found.
    :param relays: Relays
    :return: List relays (int)
    """
    relay_numbers = []

    if relays:
        if relays == ['*']:
            # Convert * to relay int numbers
            relay_numbers = [relay for relay in range(1, R421A08_NUM_RELAYS + 1)]
        else:
            # Convert relay arguments to int
            relay_numbers = list(map(int, relays))

        # Check relay numbers
        for relay_number in relay_numbers:
            if relay_number < 1 or relay_number > R421A08_NUM_RELAYS:
                raise ValueError('Incorrect relay number: {}'.format(relay_number))

    return relay_numbers


def print_relay_command(relays, cmd):
    """
        Print relay command
    :param relays: List relays (int)
    :param cmd: Relay command
    :return: None
    """

    if relays:
        if relays[0] == '*':
            print('All relays {}...'.format(cmd))
        else:
            if len(relays) > 1:
                relay_str = 'Relays'
            else:
                relay_str = 'Relay'

            relay_numbers_str = ', '.join(str(relay) for relay in relays)

            print('{} {} {}...'.format(relay_str, relay_numbers_str, cmd))


def relay_cmd_status(args, **kwargs):
    """
        Send status command to relay and read response from relay board
    :param args: Commandline arguments
    :return: None
    """
    _relay_board = kwargs['relay_boards']

    # Convert relay argument to list relay numbers (int)
    relays = get_relay_numbers(args.relays)

    # Print status one or more relays
    if relays and len(relays) == 1:
        print('Status relay:')
        _relay_board.print_status(relays[0])
    elif relays and len(relays) > 1:
        print('Status relays:')
        _relay_board.print_status_multi(relays, indent=True)


def relay_cmd_on(args, **kwargs):
    _relay_board = kwargs['relay_boards']

    # Print relay command
    print_relay_command(args.relays, 'on')

    # Convert relay argument to list relay numbers (int)
    relays = get_relay_numbers(args.relays)

    # Turn one or more relays on
    try:
        if relays and len(relays) == 1:
            _relay_board.on(relays[0])
        elif relays and len(relays) > 1:
            _relay_board.on_multi(relays)
    except relay_modbus.TransferException as err:
        print_stderr(err)


def relay_cmd_off(args, **kwargs):
    _relay_board = kwargs['relay_boards']

    print_relay_command(args.relays, 'off')
    relays = get_relay_numbers(args.relays)

    try:
        if relays and len(relays) == 1:
            _relay_board.off(relays[0])
        elif relays and len(relays) > 1:
            _relay_board.off_multi(relays)
    except relay_modbus.TransferException as err:
        print_stderr(err)


def relay_cmd_toggle(args, **kwargs):
    _relay_board = kwargs['relay_boards']

    print_relay_command(args.relays, 'toggle')
    relays = get_relay_numbers(args.relays)

    try:
        if relays and len(relays) == 1:
            _relay_board.toggle(relays[0])
        elif relays and len(relays) > 1:
            _relay_board.toggle_multi(relays)
    except relay_modbus.TransferException as err:
        print_stderr(err)


def relay_cmd_latch(args, **kwargs):
    _relay_board = kwargs['relay_boards']

    print_relay_command(args.relays, 'latch')
    relays = get_relay_numbers(args.relays)

    try:
        if relays and len(relays) == 1:
            _relay_board.latch(relays[0])
        elif relays and len(relays) > 1:
            _relay_board.latch_multi(relays)
    except relay_modbus.TransferException as err:
        print_stderr(err)


def relay_cmd_momentary(args, **kwargs):
    _relay_board = kwargs['relay_boards']

    print_relay_command(args.relays, 'momentary')
    relays = get_relay_numbers(args.relays)

    try:
        if relays and len(relays) == 1:
            _relay_board.momentary(relays[0])
        elif relays and len(relays) > 1:
            _relay_board.momentary_multi(relays)
    except relay_modbus.TransferException as err:
        print_stderr(err)


def relay_cmd_delay(args, **kwargs):
    _relay_board = kwargs['relay_boards']
    print_relay_command(args.relays, 'delay')
    relays = get_relay_numbers(args.relays)

    try:
        if relays and len(relays) == 1:
            _relay_board.delay(relays[0], delay=args.delay)
        elif relays and len(relays) > 1:
            _relay_board.delay_multi(relays, delay=args.delay)
    except relay_modbus.TransferException as err:
        print_stderr(err)


def arg_check_relay(relay):
    """
        Check relay type argument
    :param relay: One relay
    :return: Relay argument
    """
    errors = False

    if relay == '*':
        pass
    else:
        try:
            relay = int(relay)
            if relay < 1 or relay > R421A08_NUM_RELAYS:
                errors = True
        except ValueError:
            errors = True

    if errors:
        raise argparse.ArgumentTypeError(
            "Valid relay numbers: 1..{}".format(R421A08_NUM_RELAYS))

    return relay


def arg_check_address(address):
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

    if address >= R421A08_NUM_ADDRESSES:
        errors = True

    if errors:
        raise argparse.ArgumentTypeError(
            "Valid addresses: 0..{}".format(R421A08_NUM_ADDRESSES - 1))

    return address


def arg_check_delay(delay):
    """
        Check delay argument
    :param delay: Delay must be int and 1..255
    :return: delay when valid
    """
    errors = False

    try:
        delay = int(delay)
    except ValueError:
        errors = True

    if delay < 1 or delay > 255:
        errors = True

    if errors:
        raise argparse.ArgumentTypeError("Valid delays: 1..N seconds")

    return delay


def argument_parser(args):
    """
        Argument parser
    :param args: Commandline arguments
    :return: None
    """

    # ----------------------------------------------
    # Description and help strings
    description = \
        'Python script to control a 8 Channel RS485 MODBUS RTU relay board type R421A08.'

    help_serial_port = \
        'Serial port (such as COM1 or /dev/ttyUSB0)'

    help_address = \
        'Address of the board [0..{}] (Set DIP switches)'.format(R421A08_NUM_ADDRESSES - 1)

    help_relays = \
        'Relay numbers [1..{}] or * for all relays'.format(R421A08_NUM_RELAYS)

    # ----------------------------------------------------------------------------------------------
    # Create argument parser
    _parser = argparse.ArgumentParser(description=description)

    # Serial port argument is always required
    _parser.add_argument('serial_port', metavar='<SERIAL_PORT>', type=str, help=help_serial_port)

    # Address argument is always required
    _parser.add_argument('address', metavar='<ADDRESS>', type=arg_check_address, help=help_address)

    # ----------------------------------------------------------------------------------------------
    # Create sub command arguments
    _subparsers = _parser.add_subparsers(help='Relay command')

    # Create status argument
    _parser_status = _subparsers.add_parser('status', help='Read status')
    _parser_status.add_argument('relays', metavar='<RELAYS>', nargs='*', default=['*'],
                                type=arg_check_relay, help=help_relays)
    _parser_status.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_status.set_defaults(func=relay_cmd_status)

    # Create poll argument
    # _parser_poll = _subparsers.add_parser('poll', help='Poll status')
    # _parser_poll.add_argument('relays', metavar='<RELAYS>', nargs='*', default=['*'],
    #                           type=arg_check_relay, help=help_relays)
    # _parser_poll.add_argument('-i', '--interval', type=int, help='Poll interval in seconds')
    # _parser_poll.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    # _parser_poll.set_defaults(func=relay_cmd_poll)

    # Create on argument
    _parser_on = _subparsers.add_parser('on', help='On')
    _parser_on.add_argument('relays', metavar='<RELAYS>', nargs='*', type=arg_check_relay,
                            help=help_relays)
    _parser_on.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_on.set_defaults(func=relay_cmd_on)

    # Create off argument
    _parser_off = _subparsers.add_parser('off', help='Off')
    _parser_off.add_argument('relays', metavar='<RELAYS>', nargs='*', type=arg_check_relay,
                             help=help_relays)
    _parser_off.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_off.set_defaults(func=relay_cmd_off)

    # Create toggle argument
    _parser_toggle = _subparsers.add_parser('toggle', help='Toggle')
    _parser_toggle.add_argument('relays', metavar='<RELAYS>', nargs='*', type=arg_check_relay,
                                help=help_relays)
    _parser_toggle.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_toggle.set_defaults(func=relay_cmd_toggle)

    # Create latch argument
    _parser_latch = _subparsers.add_parser('latch', help='Latch')
    _parser_latch.add_argument('relays', metavar='<RELAYS>', nargs='*', type=arg_check_relay,
                               help=help_relays)
    _parser_latch.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_latch.set_defaults(func=relay_cmd_latch)

    # Create momentary argument
    _parser_latch = _subparsers.add_parser('momentary', help='Momentary')
    _parser_latch.add_argument('relays', metavar='<RELAYS>', nargs='*', type=arg_check_relay,
                               help=help_relays)
    _parser_latch.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_latch.set_defaults(func=relay_cmd_momentary)

    # Create delay argument
    _parser_moment = _subparsers.add_parser('delay', help='Delay')
    _parser_moment.add_argument('relays', metavar='<RELAYS>', nargs='*', type=arg_check_relay,
                                help=help_relays)
    _parser_moment.add_argument('-d', '--delay', type=arg_check_delay, default=2,
                                help='Delay (1..255 seconds) Default: 2 seconds')
    _parser_moment.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    _parser_moment.set_defaults(func=relay_cmd_delay)

    # ----------------------------------------------------------------------------------------------
    # Parse arguments
    _args = None
    try:
        _args = _parser.parse_args(args)

        # Check required arguments
        for argument in ['serial_port', 'address', 'relays', 'verbose']:
            if argument not in _args:
                raise AttributeError()
    except AttributeError:
        _parser.print_help()
        sys.exit(0)

    # Create relay_modbus object
    _modbus = relay_modbus.Modbus(_args.serial_port, verbose=_args.verbose)
    try:
        _modbus.open()
    except serial.SerialException:
        print_stderr('Error: Cannot open serial port: ' + args.serial_port)
        sys.exit(1)

    # Create relay board object
    _relay_board = relay_boards.R421A08(_modbus,
                                        address=_args.address,
                                        verbose=_args.verbose)

    _args.func(_args, relay_boards=_relay_board)


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
