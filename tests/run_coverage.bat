@echo off
rem
rem Installation coverage: python.exe -m pip install coverage
rem

setlocal

rem Configure Python environment
call python36env\Scripts\activate.bat

rem Serial port relay board for normal control
set RELAY_SERIAL_PORT=COM3

rem Second serial port for MODBUS monitor
set RELAY_SERIAL_PORT_MONITOR=COM4

rem Configure relay board DIP switches
set RELAY_ADDRESS=1

python -m coverage erase
python -m coverage run -a -m examples.getting_started
python -m coverage run -a -m examples.single_relay_board
python -m coverage run -a -m examples.multiple_relay_boards
python -m coverage run -a -m unittest discover -s . -v
python -m coverage report --include=examples/*,relay_modbus/*,relay_boards/*
python -m coverage html --include=examples/*,relay_modbus/*,relay_boards/*
start htmlcov\index.html
