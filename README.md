# 8 Channel RS485 MODBUS RTU relay board type R421A08

This Python project can control up to 64 individual 8 channel R421A08 relay boards from the command line and GUI. It uses a universal USB - RS485 dongle.

### Project features:

* Python packages for easy application integration.
* Simple command line interface, useful for scripting.
* Python packages tested with Python 2.7 and 3.6.
* wxPython GUI tested with Python 3.5 only (Windows 10 and Ubuntu 16.04)
* Unit tests with coverage.



## Hardware

The following hardware is required for this project:

* One or more R421A08 relay boards.
* RS485 - USB dongle.
* Optional: A second RS485 - USB dongle to monitor MODBUS frames.

### R421A08 relay board

![R421A08 board](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/R421A08.png)

* RS485 (binary) interface.
* 8 x 12V Relays: 10A 125VAC / 10A 28VDC.
* 8 status LED's.
* 6 DIP switches for 64 board addresses.
* Board power: 12V DC.
* Current board idle: ~11mA.
* Current one relay: ~26mA.
* Current all relays on: ~220mA.
* Length: 90mm, width: 60mm, height: 20mm.

**WARNING: DO NOT USE THIS RELAY BOARD WITH 230V AC!**  
The distance between relay traces on the PCB are < 2mm without holes for isolation. This is dangerous when using it with high voltages. See the picture above.

### RS485 - USB dongle

This project requires a RS485 - USB dongle which is widely available, for example:

![RS485 - USB dongle](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/RS485_USB_dongle.png)

* On Windows, open the ```Device Manager``` | ```Ports (COM & LPT)``` to find the ```USB-SERIAL CH340 (COMxx)``` serial port.
* On Linux, use the ```dmesg``` command  to find the serial port, such as ```/dev/ttyUSB0```.


## Software

### Screenshot R421A08 relay GUI

![Screenshot R421A08 Relay Control GUI](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/screenshot_R421A08_relay_control_gui.png)

### Screenshot MODBUS GUI

![Screenshot MODBUS GUI](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/screenshot_modbus_gui.png)

### Screenshot commandline

![Screenshot MODBUS GUI](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/screenshot_commandline.png)

### Screenshot relay toggle example

![Screenshot MODBUS GUI](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/screenshot_wxPython_relay_toggle_gui.png)

## Installation 

Installation PySerial Windows:

```bash
python.exe -m pip install pyserial
python -m pip install -U --force-reinstall pip
```

Installation PySerial Linux:
```bash
# For Python2:
$ sudo python -m pip install pyserial

# For Python3:
$ sudo apt-get install python3-pip
$ sudo pip3 install pyserial
```



## Usage ```relay_boards``` package

[getting_started.py](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/examples/getting_started.py)

```python
import time
import relay_boards

def check(retval):
    if not retval:
        exit(1)

if __name__ == '__main__':
    print('Getting started R421A08 relay board\n')

    # Create relay board object
    board = relay_boards.R421A08(serial_port='COM3', address=1)

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
```



## Usage command line

```shell
set PATH=%PATH%;C:\Python36
set PYTHONPATH=%PYTHONPATH%;.
echo %PYTHONPATH%

.\relay_cmdline.py
examples\getting_started.py
```



The relay board can be controlled from the command line:

```
usage: relay_cmdline.py [-h]
                        <SERIAL_PORT> <ADDRESS>
                        {status,on,off,toggle,latch,momentary,delay} ...

Python script to control a 8 Channel RS485 MODBUS RTU relay board type
R421A08.

positional arguments:
  <SERIAL_PORT>         Serial port (such as COM1 or /dev/ttyUSB0)
  <ADDRESS>             Address of the board [0..63] (Set DIP switches)
  {status,on,off,toggle,latch,momentary,delay}
                        Relay command
    status              Read status
    on                  On
    off                 Off
    toggle              Toggle
    latch               Latch
    momentary           Momentary
    delay               Delay

optional arguments:
  -h, --help            show this help message and exit
```

### Board address 1, turn relay 1 on
Turn relay 1 on.  
Replace the relay number between 1 and 8.  
Abbreviation arguments are supported: replace ```--relay``` with ```-r```. 
```
python R421A08.py COM1 --address 1 --relay 1 --on
Turn relay 1 on...
Done
```

### Board address 1, turn all relays on
```
python R421A08.py COM1 --address 1 --relay * --on
Turn relays 1, 2, 3, 4, 5, 6, 7, 8 on...
Done
```

### Board address 1, turn relay 1 off
```
python R421A08.py COM1 --address 1 --relay 1 --off
Turn relay 1 off...
Done
```

### Board address 1, toggle relay 1
Toggle relay: on -> off and off -> on.
```
python R421A08.py COM1 --address 1 --relay 1 --toggle
Toggle relay 1...
Done
```

### Board address 1, latch relay 1
Turn all relays off, except one.
```
python R421A08.py COM1 --address 1 --relay 1 --latch
Latch relay 1...
Done
```

### Board address 1, momentary relay 1
Turn relay on for 1 second, then turn it off.
```
python R421A08.py COM1 --address 1 --relay 1 --momentary
Turn relay 1 on/off with 1 sec delay...
Done
```

### Board address 1, delay relay 1
Turn relay on for a specific delay in seconds, then turn it off.
```
python R421A08.py COM1 --address 1 --relay 1 --delay 3
Turn relay 1 on/off with 3 sec delay...
Done
```

### Board address 1, read status relay 1
Read status of one relay.
```
python R421A08.py COM1 --address 1 --relay 1 --status
Relay 1: OFF
Done
```

### Board address 1, read status all relay's
Read status of all relays.
```
python R421A08.py COM1 --address 1 --relay * --status
Relay 1: ON
Relay 2: OFF
Relay 3: ON
Relay 4: ON
Relay 5: ON
Relay 6: ON
Relay 7: ON
Relay 8: OFF
Done
```

### Listen: Print frames from all addresses
For debug purposes, print all receiving frames.
```
python  R421A08.py COM1 --address 0 --listen
Listening for all incoming frames.
Press CTRL+C to abort.
RX 16:  02 06 00 02 01 00 29 9A 01 06 00 02 01 00 29 9A
RX 16:  01 06 00 01 01 00 D9 9A 01 06 00 01 01 00 D9 9A
RX 16:  01 06 00 01 02 00 D9 6A 01 06 00 01 02 00 D9 6A
RX 16:  01 06 00 01 03 00 D8 FA 01 06 00 01 03 00 D8 FA
...
```

### Listen: Print frames from address 2 only
For debug purposes, print receiving frames from one address.
```
python  R421A08.py COM1 --address 2 --listen
Listening for incoming frames from address 2.
Press CTRL+C to abort.
RX 16:  02 06 00 01 01 00 D9 A9 02 06 00 01 01 00 D9 A9
RX 16:  02 06 00 01 02 00 D9 59 02 06 00 01 02 00 D9 59
...
```

### Send MODBUS raw ASCII hex command

Send frame with adding CRC:

```
python R421A08.py COM1 --address 1 --send ":010600010100"
TX 8:  01 06 00 01 02 00 D9 9A
RX 8:  01 06 00 01 02 00 D9 9A
Done

python R421A08.py COM1 --address 1 --send "01 06 00 01 01 00"
TX 8:  01 06 00 01 01 00 D9 9A
RX 8:  01 06 00 01 01 00 D9 9A
Done

python R421A08.py COM1 1 --send "0x01, 0x06, 0x00, 0x01, 0x01, 0x00"
TX 8:  01 06 00 01 01 00 D9 9A
RX 8:  01 06 00 01 01 00 D9 9A
Done
```

Send frame without adding CRC:

```
python R421A08.py COM1 --address 1 --send ":010600010100D99A" --no-crc
TX 8:  01 06 00 01 02 00 D9 9A
RX 8:  01 06 00 01 02 00 D9 9A
Done

python R421A08.py COM1 --address 1 --send "01 06 00 01 01 00 D9 9A" --no-crc
TX 8:  01 06 00 01 01 00 D9 9A
RX 8:  01 06 00 01 01 00 D9 9A
Done

python R421A08.py COM1 --address 1 --send "0x01, 0x06, 0x00, 0x01, 0x01, 0x00, 0xD9, 0x9A" --no-crc
TX 8:  01 06 00 01 01 00 D9 9A
RX 8:  01 06 00 01 01 00 D9 9A
Done
```

### Verbose

For debug purposes, print transmit and receive frames in HEX.
```
python R421A08.py COM1 --address 1 --relay * --on -v
Turn relays 1, 2, 3, 4, 5, 6, 7, 8 on...
TX 8:  01 06 00 01 01 00 D9 9A
RX 8:  01 06 00 01 01 00 D9 9A
TX 8:  01 06 00 02 01 00 29 9A
RX 8:  01 06 00 02 01 00 29 9A
TX 8:  01 06 00 03 01 00 78 5A
RX 8:  01 06 00 03 01 00 78 5A
TX 8:  01 06 00 04 01 00 C9 9B
RX 8:  01 06 00 04 01 00 C9 9B
TX 8:  01 06 00 05 01 00 98 5B
RX 8:  01 06 00 05 01 00 98 5B
TX 8:  01 06 00 06 01 00 68 5B
RX 8:  01 06 00 06 01 00 68 5B
TX 8:  01 06 00 07 01 00 39 9B
RX 8:  01 06 00 07 01 00 39 9B
TX 8:  01 06 00 08 01 00 09 98
RX 8:  01 06 00 08 01 00 09 98
Done

python R421A08.py COM1 --address 1 --relay * --off -v
Turn relays 1, 2, 3, 4, 5, 6, 7, 8 off...
TX 8:  01 06 00 01 02 00 D9 6A
RX 8:  01 06 00 01 02 00 D9 6A
TX 8:  01 06 00 02 02 00 29 6A
RX 8:  01 06 00 02 02 00 29 6A
TX 8:  01 06 00 03 02 00 78 AA
RX 8:  01 06 00 03 02 00 78 AA
TX 8:  01 06 00 04 02 00 C9 6B
RX 8:  01 06 00 04 02 00 C9 6B
TX 8:  01 06 00 05 02 00 98 AB
RX 8:  01 06 00 05 02 00 98 AB
TX 8:  01 06 00 06 02 00 68 AB
RX 8:  01 06 00 06 02 00 68 AB
TX 8:  01 06 00 07 02 00 39 6B
RX 8:  01 06 00 07 02 00 39 6B
TX 8:  01 06 00 08 02 00 09 68
RX 8:  01 06 00 08 02 00 09 68
Done

python R421A08.py COM1 --address 1 --relay 1 --toggle -v
Toggle relay 1...
TX 8:  01 06 00 01 03 00 D8 FA
RX 8:  01 06 00 01 03 00 D8 FA
Done

python R421A08.py COM1 --address 1 --relay 1 --latch -v
Latch relay 1...
TX 8:  01 06 00 01 04 00 DA CA
RX 8:  01 06 00 01 04 00 DA CA
Done

python R421A08.py COM1 --address 1 --relay 1 --momentary -v
Turn relay 1 on/off with 1 sec delay...
TX 8:  01 06 00 01 05 00 DB 5A
RX 8:  01 06 00 01 05 00 DB 5A
Done

python R421A08.py COM1 --address 1 --relay 1 --delay 3 -v
Turn relay 1 on/off with 3 sec delay...
TX 8:  01 06 00 01 06 03 9B AB
RX 8:  01 06 00 01 06 03 9B AB
Done

python R421A08.py COM1 --address 1 --relay * --status -v
TX 8:  01 03 00 01 00 01 D5 CA
RX 7:  01 03 02 00 01 79 84
Relay 1: ON
TX 8:  01 03 00 02 00 01 25 CA
RX 7:  01 03 02 00 01 79 84
Relay 2: ON
TX 8:  01 03 00 03 00 01 74 0A
RX 7:  01 03 02 00 01 79 84
Relay 3: ON
TX 8:  01 03 00 04 00 01 C5 CB
RX 7:  01 03 02 00 01 79 84
Relay 4: ON
TX 8:  01 03 00 05 00 01 94 0B
RX 7:  01 03 02 00 01 79 84
Relay 5: ON
TX 8:  01 03 00 06 00 01 64 0B
RX 7:  01 03 02 00 01 79 84
Relay 6: ON
TX 8:  01 03 00 07 00 01 35 CB
RX 7:  01 03 02 00 01 79 84
Relay 7: ON
TX 8:  01 03 00 08 00 01 05 C8
RX 7:  01 03 02 00 00 B8 44
Relay 8: OFF
Done
```

## Documentation

[MODBUS Application Protocol Specification v1.1.b](http://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b.pdf)

The following Python packages are available in this project:

- R421A08 relay board Python package:
  - Read state relay(s).
  - Turn relay(s) on.
  - Turn relay(s) off.
  - Toggle relay(s).
  - Latch relay (One relay on, rest off).
  - Momentary (Turn relay on for one second).
  - Delay (Turn relay on for 1..255 seconds).
  - Single or multiple relay boards.
- Serial MODBUS Python package:
  - MODBUS monitor frames on the RS485 bus
  - Send raw ASCII MODBUS frames

### RS485 RTU MODBUS communication protocol

[MODBUS](https://en.wikipedia.org/wiki/Modbus) is an open binary serial communication protocol, mainly used for PLCs.

- Serial port at 9600 baud, 8 databits, 1 stop, no parity.
- This board supports MODBUS RTU protocol only.
- This board supports 64 addresses, configurable with 6 DIP switches. 
- This board does **not** support ASCII mode, but can be send with the Python```--send``` option.
- This board does **not** support AT commands.
- This board does **not** support broadcasts.
- All relays are off after power-on.

## Unit tests

```bash
python -m unittest tests.test_relay_board
```
