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
# This is a Python example to control a single R421A08 relay board with a USB - RS485 dongle.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import sys
import time

# Add system path to find relay_ Python packages
sys.path.append('.')
sys.path.append('..')

import relay_modbus
import relay_boards


# Required: Configure serial port, for example:
#   On Windows: 'COMx'
#   On Linux:   '/dev/ttyUSB0'
SERIAL_PORT = 'COM3'

# Optional: Configure board address with 6 DIP switches on the relay board
# Default address: 1
address = 1

# Optional: Give the relay board a name
board_name = 'Relay board kitchen'


def print_relay_board_info(board):
    print('Relay board:')
    print('  Name:      {}'.format(board.board_name))
    print('  Type:      {}'.format(board.board_type))
    print('  Port:      {}'.format(board.serial_port))
    print('  Baudrate:  {}'.format(board.baudrate))
    print('  Addresses: {}'.format(board.num_addresses))
    print('  Relays:    {}'.format(board.num_relays))
    print('  Address:   {} (Configure DIP switches)'.format(board.address))
    print()


def relay_control(board):
    print('Turn relay 1 on')
    board.on(1)
    time.sleep(1)

    print('Turn relay 2 on')
    board.on(2)
    time.sleep(1)

    print('Turn all relays off')
    board.off_all()
    time.sleep(1)

    print('Turn relays 3, 7 and 8 on')
    board.toggle_multi([3, 7, 8])
    time.sleep(1)

    print('Status all relays:')
    board.print_status_all()

    print('Latch relays 6 on, all other relays off')
    board.latch(6)
    time.sleep(1)

    print('Turn relay 4 on for 5 seconds, all other relays off')
    board.delay(4, delay=5)


def main():
    print('Single R421A08 relay board example\n')

    # Create relay_modbus object
    _modbus = relay_modbus.Modbus(serial_port=SERIAL_PORT, verbose=False)

    # Open serial port
    try:
        _modbus.open()
    except relay_modbus.SerialOpenException as err:
        print(err)
        sys.exit(1)

    # Create relay board object
    board = relay_boards.R421A08(_modbus,
                                 address=address,
                                 board_name=board_name,
                                 verbose=False)

    # Print board info
    print_relay_board_info(board)

    # Control some relays
    relay_control(board)

    print('Done')


if __name__ == '__main__':
    main()
