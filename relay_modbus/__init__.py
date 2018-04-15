from . modbus import Modbus, get_frame_str
from . modbus import FRAME_DELAY
from . modbus import SerialOpenException, TransferException
from . serial_ports import get_serial_ports

__version__ = '0.0.2'
VERSION = __version__
