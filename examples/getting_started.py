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
# This is a Python getting started example to control a single R421A08 relay board with a
# USB - RS485 dongle.
#
# Python 2.7 and Python 3.6 are supported.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import time
import sys

# Add system path to find relay_ Python packages
sys.path.append('.')
sys.path.append('..')

import relay_modbus
import relay_boards

# Required: Configure serial port, for example:
#   On Windows: 'COMx'
#   On Linux:   '/dev/ttyUSB0'
SERIAL_PORT = 'COM3'


def check(retval):
    if not retval:
        sys.exit(1)


if __name__ == '__main__':
    print('Getting started R421A08 relay board\n')

    # Create MODBUS object
    _modbus = relay_modbus.Modbus(serial_port=SERIAL_PORT)

    # Open serial port
    try:
        _modbus.open()
    except relay_modbus.SerialOpenException as err:
        print(err)
        sys.exit(1)

    # Create relay board object
    board = relay_boards.R421A08(_modbus, address=1)

    print('Status all relays:')
    check(board.print_status_all())
    time.sleep(1)

    print('Turn relay 1 on')
    check(board.on(1))
    time.sleep(1)

    print('Turn relay 1 off')
    check(board.off(1))
    time.sleep(1)

    print('Toggle relay 8')
    check(board.toggle(8))
    time.sleep(1)

    print('Latch relays 6 on, all other relays off')
    check(board.latch(6))
    time.sleep(1)

    print('Turn relay 4 on for 5 seconds, all other relays off')
    check(board.delay(4, delay=5))
    time.sleep(6)

    print('Turn relays 3, 7 and 8 on')
    check(board.toggle_multi([3, 7, 8]))
    time.sleep(1)

    print('Turn all relays on')
    check(board.on_all())
    time.sleep(1)

    print('Turn all relays off')
    check(board.off_all())
    time.sleep(1)
