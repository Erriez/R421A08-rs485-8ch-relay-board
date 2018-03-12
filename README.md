# 8 Channel RS485 MODBUS RTU relay board type R421A08

This Python example can control up to 64 individual 8 channel relay boards from the command line by 
using a USB - RS485 dongle. It has been tested with board type R421A08 with Python 2 and 3 on 
Windows, but should work on Linux as well.

## Hardware

The following hardware is required for this project:

### R421A08 relay board

![R421A08 board](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/R421A08.png)

* Board power: 12V DC 
* Current board idle: ~11mA
* Current one relay: ~26mA
* Current all relays on: ~220mA

**WARNING: DO NOT USE THIS RELAY BOARD WITH 230V AC!**  
The distance between relay traces on the PCB are < 2mm without holes for isolation. This is dangerous when using it with high voltages. See the picture above.

### RS485 - USB dongle

This project requires a USB to RS485 dongle, for example:

![RS485 - USB dongle](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/RS485_USB_dongle.png)

* On Windows, open the ```Device Manager``` | ```Ports (COM & LPT)``` to find the ```USB-SERIAL CH340 (COMxx)``` serial port.
* On Linux, use the ```dmesg``` command  to find the serial port, such as ```/dev/ttyUSB0```.

## RS485 RTU MODBUS communication protocol

[MODBUS](https://en.wikipedia.org/wiki/Modbus) is an open binary serial communication protocol, mainly used for PLCs.

* Serial port at 9600 baud, 8 databits, 1 stop, no parity.
* This board supports MODBUS RTU protocol only.
* This board supports 64 addresses, configurable with 6 DIP switches. 
* This board does **not** support ASCII mode, but can be send with the Python```--send``` option.
* This board does **not** support AT commands.
* This board does **not** support broadcasts.
* All relays are off after power-on.

## Source
Support for Python 2 and 3 with PySerial module.

[Source R421A08.py](https://github.com/Erriez/R421A08-rs485-8ch-relay-board/blob/master/R421A08.py)

## Documentation
[MODBUS Application Protocol Specification v1.1.b](http://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b.pdf)

## Installation PySerial Windows
```bash
cd c:\Python36
python.exe -m pip install pyserial
```

## Installation PySerial Linux
```bash
$ sudo python3 -m pip install pyserial
```

## Usage
```
c:\Python36\python.exe R421A08.py -h
usage: R421A08.py [-h] [-v] [-i] [-a ADDRESS] [-r [RELAY [RELAY ...]]] [-s]
                  [-1] [-0] [-t] [-l] [-m] [-d DELAY] [--send FRAME] [-n]
                  SERIAL_PORT

Python script to control a 8 Channel RS485 MODBUS RTU relay board type
R421A08.

positional arguments:
  SERIAL_PORT           Serial port (such as COM1 or /dev/ttyUSB0)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print verbose
  -i, --listen          Listen on receive
  -a ADDRESS, --address ADDRESS
                        Address of the board [0..63] (Set DIP switches)
  -r [RELAY [RELAY ...]], --relay [RELAY [RELAY ...]]
                        Relay numbers [1..8] or * for all relays
  -s, --status          Read status
  -1, --on              On
  -0, --off             Off
  -t, --toggle          Toggle
  -l, --latch           Latch
  -m, --momentary       Momentary
  -d DELAY, --delay DELAY
                        Delay (0..255 seconds)
  --send FRAME          Transmit MODBUS frame in ASCII hex, such as
                        ":010600010100" or "01 06 00 01 01 00" or "0x01, 0x06,
                        0x00, 0x01, 0x01, 0x00". CRC is automatically added to
                        the end of the frame.
  -n, --no-crc          Do not add CRC to --send frame
```

### Board address 1, turn relay 1 on
Turn relay 1 on.  
Replace the relay number between 1 and 8.  
Abbreviation arguments are supported: replace ```--relay``` with ```-r```. 
```
python R421A08.py COM1 --address 1 --relay 1 --on
Turn relay(s) [1] on...
Done
```

### Board address 1, turn all relays on
```
python R421A08.py COM1 --address 1 --relay * --on
Turn relay(s) [1, 2, 3, 4, 5, 6, 7, 8] on...
Done
```

### Board address 1, turn relay 1 off
```
python R421A08.py COM1 --address 1 --relay 1 --off
Turn relay(s) [1] off...
Done
```

### Board address 1, toggle relay 1
Toggle relay: on -> off and off -> on.
```
python R421A08.py COM1 --address 1 --relay 1 --toggle
Toggle relay(s) [1]...
Done
```

### Board address 1, latch relay 1
Turn all relays off, except one.
```
python R421A08.py COM1 --address 1 --relay 1 --latch
Latch relay(s) [1]...
Done
```

### Board address 1, momentary relay 1
Turn relay on for 1 second, then turn it off.
```
python R421A08.py COM1 --address 1 --relay 1 --momentary
Turn relay(s) [1] on/off...
Done
```

### Board address 1, delay relay 1
Turn relay on for a specific delay in seconds, then turn it off.
```
python R421A08.py COM1 --address 1 --relay 1 --delay 3
Turn relay(s) [1] on/off with delay 3 sec...
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
Turn relay(s) [1, 2, 3, 4, 5, 6, 7, 8] on...
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
Turn relay(s) [1, 2, 3, 4, 5, 6, 7, 8] off...
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
Toggle relay(s) [1]...
TX 8:  01 06 00 01 03 00 D8 FA
RX 8:  01 06 00 01 03 00 D8 FA
Done

python R421A08.py COM1 --address 1 --relay 1 --latch -v
Latch relay(s) [1]...
TX 8:  01 06 00 01 04 00 DA CA
RX 8:  01 06 00 01 04 00 DA CA
Done

python R421A08.py COM1 --address 1 --relay 1 --momentary -v
Turn relay(s) [1] on/off...
TX 8:  01 06 00 01 05 00 DB 5A
RX 8:  01 06 00 01 05 00 DB 5A
Done

python R421A08.py COM1 --address 1 --relay 1 --delay 3 -v
Turn relay(s) [1] on/off with delay 3 sec...
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