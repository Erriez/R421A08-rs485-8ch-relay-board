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
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import time

import relay_modbus


# Fixed board type string
BOARD_TYPE = 'R421A08'

# Fixed RS485 baudrate required for the R421A08 relay board
BAUDRATE = 9600

# Fixed number of relays on the R421A08 board
NUM_RELAYS = 8

# Fixed number of addresses, configurable with 6 DIP switches on the R421A08 relay board
NUM_ADDRESSES = 64

# Commands
CMD_ON = 0x01
CMD_OFF = 0x02
CMD_TOGGLE = 0x03
CMD_LATCH = 0x04
CMD_MOMENTARY = 0x05
CMD_DELAY = 0x06

# R421A08 supports MODBUS control command and read status only
FUNCTION_CONTROL_COMMAND = 0x06
FUNCTION_READ_STATUS = 0x03

# Fixed receive frame length
RX_LEN_CONTROL_COMMAND = 8
RX_LEN_READ_STATUS = 7


class ModbusException(Exception):
    pass


class R421A08(object):
    """ R421A08 relay board class """
    def __init__(self,
                 modbus_obj,
                 address=1,
                 board_name='Relay board {}'.format(BOARD_TYPE),
                 num_address=NUM_ADDRESSES,
                 num_relays=NUM_RELAYS,
                 verbose=False):
        """
            R421A08 relay board constructor
        :param modbus_obj:
        :param address:
        :param board_name:
        :param num_address:
        :param num_relays:
        :param verbose:
            False: Normal prints (Default)
            True: Print verbose messages
        """
        # Print additional prints
        self._verbose = verbose

        assert type(modbus_obj) == relay_modbus.Modbus
        self._modbus = modbus_obj

        # Store required board address (Configurable with DIP 6 switches)
        assert 0 <= int(address) < NUM_ADDRESSES
        self._address = int(address)

        # Store optional board name
        self._board_name = str(board_name)

        # Store default R421A08 board settings which may be overruled (Not recommended)
        self._num_addresses = int(num_address)
        self._num_relays = int(num_relays)

    # ----------------------------------------------------------------------------------------------
    # Relay board properties
    # ----------------------------------------------------------------------------------------------
    @property
    def board_type(self):
        return BOARD_TYPE

    @property
    def board_name(self):
        return self._board_name

    @board_name.setter
    def board_name(self, board_name):
        self._board_name = board_name

    @property
    def serial_port(self):
        return self._modbus.serial_port

    @property
    def baudrate(self):
        return self._modbus.baudrate

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        address = int(address)

        if address >= 0 and address < self._num_addresses:
            self._address = address

    @property
    def num_addresses(self):
        return self._num_addresses

    @property
    def num_relays(self):
        return self._num_relays

    # ----------------------------------------------------------------------------------------------
    # Relay board private functions
    # ----------------------------------------------------------------------------------------------
    def _send_relay_command(self, relay, cmd, delay=0):
        """
            Send relay control
        :param relay: Relay number
        :param cmd: Command
        :param delay: Optional delay
        :return: List response (int)
        """

        assert type(relay) == int
        assert type(cmd) == int
        assert type(delay) == int

        assert relay >= 0 and relay <= 255
        assert cmd >= 0 and cmd <= 255
        assert delay >= 0 and delay <= 255

        if not self._modbus.is_open():
            raise ModbusException('Error: Serial port not open')

        # Create binary control command
        tx_data = [
            self._address,              # Slave address of the relay board 0..63
            FUNCTION_CONTROL_COMMAND,   # Read status is always 0x03
            0x00, relay,                # Relay 0x0001..0x0008
            cmd,                        # Command 0x01..0x06
            delay                       # Delay 0x00..0xFF
        ]

        # Send command
        self._modbus.send(tx_data)

        # Wait for response with timeout
        rx_frame = self._modbus.receive(RX_LEN_CONTROL_COMMAND)

        # Check response from relay
        if not rx_frame or len(rx_frame) != RX_LEN_CONTROL_COMMAND:
            return False

        return True

    def _read_relay_status(self, relay):
        """
            Read relay status
        :param relay: Relay number
        :return:
            0: Relay off
            1: Relay on
            -1: An error occurred
        """

        assert type(relay) == int

        if not self._modbus.is_open():
            raise ModbusException('Error: Serial port not open')

        # Create binary read status
        tx_data = [
            self._address,          # Slave address of the relay board 0..63
            FUNCTION_READ_STATUS,   # Read status is always 0x03
            0x00, relay,            # Relay 0x0001..0x0008
            0x00, 0x01              # Number of bytes is always 0x0001
        ]

        # Send command and wait for response with timeout
        self._modbus.send(tx_data)

        # Wait for response with timeout
        rx_data = self._modbus.receive(RX_LEN_READ_STATUS)

        if rx_data and len(rx_data) > 2:
            # Check CRC
            data_no_crc = rx_data[:-2]
            crc = rx_data[-2:]
            if self._modbus.crc(data_no_crc) != crc:
                raise ModbusException('RX error: Incorrect CRC received')
            elif rx_data[0] != tx_data[0]:
                raise ModbusException('RX error: Incorrect address received')
            elif rx_data[1] != tx_data[1]:
                raise ModbusException('RX error: Incorrect function received')
            elif rx_data[2] != 2:
                raise ModbusException('RX error: Incorrect data length received')
            elif rx_data[3] != 0:
                raise ModbusException('RX error: Incorrect data high Byte received')
            elif rx_data[4] != 0 and rx_data[4] != 1:
                raise ModbusException('RX error: Incorrect data low Byte received')
            else:
                return rx_data[4]

        return -1

    # ----------------------------------------------------------------------------------------------
    # Public functions to read/write single relay
    # ----------------------------------------------------------------------------------------------
    def get_status(self, relay):
        return self._read_relay_status(relay)

    def print_status(self, relay, indent=False):
        line = ''
        if indent:
            line += '  '

        line += 'Relay {}: '.format(relay)

        status = self.get_status(relay)
        if status == 0:
            line += 'OFF'
        elif status == 1:
            line += 'ON'
        else:
            line += 'UNKNOWN'
            return False

        print(line)
        return True

    def relay_poll(self, relay, interval=1.0):
        status_old = -1
        while 1:
            status_new = self._read_relay_status(relay)

            if status_old != status_new:
                status_old = status_new

                if status_new == 0:
                    print('Relay {}: OFF'.format(relay))
                elif status_new == 1:
                    print('Relay {}: ON'.format(relay))
                else:
                    print('Relay {}: UNKNOWN'.format(relay))

            time.sleep(interval)
            if self._verbose:
                print('.')

    def on(self, relay):
        return self._send_relay_command(relay, CMD_ON)

    def off(self, relay):
        return self._send_relay_command(relay, CMD_OFF)

    def toggle(self, relay):
        return self._send_relay_command(relay, CMD_TOGGLE)

    def latch(self, relay):
        return self._send_relay_command(relay, CMD_LATCH)

    def momentary(self, relay):
        return self._send_relay_command(relay, CMD_MOMENTARY)

    def delay(self, relay, delay):
        return self._send_relay_command(relay, CMD_DELAY, delay=delay)

    # ----------------------------------------------------------------------------------------------
    # Public functions to read/write multiple relays
    # ----------------------------------------------------------------------------------------------
    def get_status_multi(self, relays):
        """
            Read relay status
        :param relays: List relays (int)
        :return: Dictionary with relay status [(number: status}, ...]
        """
        relay_status = {}

        for relay in relays:
            status = self._read_relay_status(relay)
            relay_status[relay] = status

        return relay_status

    def print_status_multi(self, relays, indent=False):
        """
            Print status multiple relays
        :param relays: List relays (int)
        :param indent: True: Add spaces at the beginning of the line
        :return: None
        """
        for relay in relays:
            if not self.print_status(relay, indent):
                return False
        return True

    # def poll_multi(self, relays, interval=1.0):
    #     print_stderr('TODO: Not implement yet')

    def on_multi(self, relays):
        for relay in relays:
            retval = self.on(relay)
            if not retval:
                return False
        return True

    def off_multi(self, relays):
        for relay in relays:
            retval = self.off(relay)
            if not retval:
                return False
        return True

    def toggle_multi(self, relays):
        for relay in relays:
            retval = self.toggle(relay)
            if not retval:
                return False
        return True

    def latch_multi(self, relays):
        for relay in relays:
            retval = self.latch(relay)
            if not retval:
                return False
        return True

    def momentary_multi(self, relays):
        for relay in relays:
            retval = self.momentary(relay)
            if not retval:
                return False
        return True

    def delay_multi(self, relays, delay):
        for relay in relays:
            retval = self.delay(relay, delay=delay)
            if not retval:
                return False
        return True

    # ----------------------------------------------------------------------------------------------
    # Public functions to read/write all relays
    # ----------------------------------------------------------------------------------------------
    def get_status_all(self):
        return self.get_status_multi(range(1, self._num_relays + 1))

    def print_status_all(self, indent=False):
        return self.print_status_multi(range(1, self._num_relays + 1), indent=indent)

    def on_all(self):
        return self.on_multi(range(1, self._num_relays + 1))

    def off_all(self):
        return self.off_multi(range(1, self._num_relays + 1))

    def toggle_all(self):
        return self.toggle_multi(range(1, self._num_relays + 1))

    def latch_all(self):
        return self.latch_multi(range(1, self._num_relays + 1))

    def momentary_all(self):
        return self.momentary_multi(range(1, self._num_relays + 1))

    def delay_all(self, delay):
        return self.delay_multi(range(1, self._num_relays + 1), delay=delay)
