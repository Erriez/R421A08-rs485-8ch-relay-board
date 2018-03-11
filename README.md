# 8 Channel RS485 MODBUS RTU relay board type R421A08

This is a Python example to control the relay board with a USB - RS485 dongle.
Python 2 and 3 are supported.

## Hardware

This following hardware is required for this project:

### R421A08 relay board:

![R421A08 board](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/R421A08.png)

* Board power: 12V DC 
* Current board idle: ~11mA
* Current one relay: ~26mA
* Current all relays on: ~220mA

### RS485 - USB dongle:

This project requires a USB to RS485 dongle, for example:

![RS485 - USB dongle](https://raw.githubusercontent.com/Erriez/R421A08-rs485-8ch-relay-board/master/images/RS485_USB_dongle.png)

## RS485 RTU MODBUS communication protocol

This is an open binary communication protocol. This relay board does **not** support ASCII mode.

* Serial port at 9600 baud, 8 databits, 1 stop, no parity.
* The board supports MODBUS RTU protocol only.
* The board supports 64 addresses, configurable with 6 DIP switches. 
* The board does not support ACII mode.
* The board does not broadcasts.
* All relays are off after power-on.

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
usage: R421A08.py [-h] [-v] [-i] [-r [RELAY [RELAY ...]]] [-s] [-1] [-0] [-t]
                  [-l] [-m] [-d DELAY]
                  SERIAL_PORT ADDRESS

8 Channel RS485 RTU relay board type R421A08

positional arguments:
  SERIAL_PORT           Serial port (such as COM1)
  ADDRESS               Slave address [0..63]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Print verbose
  -i, --listen          Listen on receive
  -r [RELAY [RELAY ...]], --relay [RELAY [RELAY ...]]
                        Relay numbers [1..8] or * for all relays
  -s, --status          Read status
  -1, --on              On
  -0, --off             Off
  -t, --toggle          Toggle
  -l, --latch           Latch
  -m, --moment          Momentary
  -d DELAY, --delay DELAY
                        Delay (0..255 seconds)
```

### Board address 1, turn relay 1 on
Turn relay 1 on.  
Replace the relay number between 1 and 8.  
Abbreviation arguments are supported: replace ```--relay``` with ```-r```. 
```
python R421A08.py COM3 1 --relay 1 --on
```

### Board address 1, turn all relays on
```
python R421A08.py COM3 1 --relay * --on
```

### Board address 1, turn relay 1 off
```
python R421A08.py COM3 1 --relay 1 --off
```

### Board address 1, toggle relay 1
Toggle relay: on -> off and off -> on.
```
python R421A08.py COM3 1 --relay 1 --toggle
```

### Board address 1, latch relay 1
Turn all relays off, except one.
```
python R421A08.py COM3 1 --relay 1 --latch
```

### Board address 1, momentary relay 1
Turn relay on for 1 second, then turn it off.
```
python R421A08.py COM3 1 --relay 1 --momentary
```

### Board address 1, delay relay 1
Turn relay on for a specific delay in seconds, then turn it off.
```
python R421A08.py COM3 1 --relay 1 --delay 3
```

### Board address 1, read status relay 1
Read status of one relay.
```
python R421A08.py COM3 1 --relay 1 --status
Relay 1: OFF
```

### Board address 1, read status all relay's
Read status of all relays.
```
python R421A08.py COM3 1 --relay * --status
Relay 1: ON
Relay 2: OFF
Relay 3: ON
Relay 4: ON
Relay 5: ON
Relay 6: ON
Relay 7: ON
Relay 8: OFF
```

### Listen: Print frames from all addresses
For debug purposes, print all receiving frames.
```
python  R421A08.py COM3 0 --listen
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
python  R421A08.py COM3 2 --listen
Listening for incoming frames from address 2.
Press CTRL+C to abort.
RX 16:  02 06 00 01 01 00 D9 A9 02 06 00 01 01 00 D9 A9
RX 16:  02 06 00 01 02 00 D9 59 02 06 00 01 02 00 D9 59
...
```

### Verbose
For debug purposes, print transmit and receive frames in HEX.
```
python R421A08.py COM3 1 --relay * --on -v
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

python R421A08.py COM3 1 --relay * --off -v
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

python R421A08.py COM3 1 --relay 1 --toggle -v
Toggle relay(s) [1]...
TX 8:  01 06 00 01 03 00 D8 FA
RX 8:  01 06 00 01 03 00 D8 FA

python R421A08.py COM3 1 --relay 1 --latch -v
Latch relay(s) [1]...
TX 8:  01 06 00 01 04 00 DA CA
RX 8:  01 06 00 01 04 00 DA CA

python R421A08.py COM3 1 --relay 1 --momentary -v
Turn relay(s) [1] on/off...
TX 8:  01 06 00 01 05 00 DB 5A
RX 8:  01 06 00 01 05 00 DB 5A

python R421A08.py COM3 1 --relay 1 --delay 3 -v
Turn relay(s) [1] on/off with delay 3 sec...
TX 8:  01 06 00 01 06 03 9B AB
RX 8:  01 06 00 01 06 03 9B AB

python R421A08.py COM3 1 --relay * --status -v
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
```