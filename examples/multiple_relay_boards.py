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
# This is a Python example to control multiple R421A08 relay boards with a USB - RS485 dongle.
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


def print_relay_board_info(board):
    print('Relay board "{}" #{}:'.format(board.board_name, board.address))
    print('  Name:      {}'.format(board.board_name))
    print('  Type:      {}'.format(board.board_type))
    print('  Port:      {}'.format(board.serial_port))
    print('  Baudrate:  {}'.format(board.baudrate))
    print('  Addresses: {}'.format(board.num_addresses))
    print('  Relays:    {}'.format(board.num_relays))
    print('  Address:   {} (Configure DIP switches)'.format(board.address))
    print()


def main():
    print('Multiple R421A08 relay boards example\n')

    # ----------------------------------------------------------------------------------------------
    # Create relay_modbus object
    _modbus = relay_modbus.Modbus(serial_port=SERIAL_PORT, verbose=False)

    # Open serial port
    try:
        _modbus.open()
    except relay_modbus.SerialOpenException as err:
        print(err)
        sys.exit(1)

    # ----------------------------------------------------------------------------------------------
    # Create relay board object with on address 1
    relays_kitchen = relay_boards.R421A08(_modbus,
                                          address=1,
                                          board_name='Kitchen')

    # Create second relay board object on address 2
    relays_living_room = relay_boards.R421A08(_modbus,
                                              address=1,
                                              board_name='Living room')

    # ----------------------------------------------------------------------------------------------
    # Print board info
    print_relay_board_info(relays_kitchen)
    print_relay_board_info(relays_living_room)

    # ----------------------------------------------------------------------------------------------
    # Control relays kitchen
    print('Relay board #{} relay 1 on'.format(relays_kitchen.address))
    relays_kitchen.on(1)
    print('Relay board #{} relays 2, 3 and 7 on'.format(relays_kitchen.address))
    relays_kitchen.on_multi([2, 3, 7])
    print('Relay board #{} status:'.format(relays_kitchen.address))
    relays_kitchen.print_status_all()
    time.sleep(2)

    # ----------------------------------------------------------------------------------------------
    # Control relays living room
    print('Relay board #{} toggle relay 8'.format(relays_living_room.address))
    relays_living_room.toggle(8)
    print('Relay board #{} status:'.format(relays_kitchen.address))
    relays_living_room.print_status_all()
    time.sleep(2)

    # ----------------------------------------------------------------------------------------------
    # Control relays kitchen and living room
    print('Relay board #{} all off'.format(relays_kitchen.address))
    relays_kitchen.off_all()
    print('Relay board #{} all off'.format(relays_living_room.address))
    relays_living_room.off_all()

    print('Done')


if __name__ == '__main__':
    main()
