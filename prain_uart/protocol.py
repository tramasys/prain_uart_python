from enum import Enum
from typing import Literal

FRAME_SIZE_BITS = 64
PAYLOAD_SIZE_BITS = 56
ADDR_SIZE_BITS = 2
CMD_SIZE_BITS = 4
PARAM_SIZE_BITS = 50
CRC_SIZE_BITS = 8

class Address(Enum):
    RASPBERRY_HAT = 0b00
    MOTION_CTRL = 0b01
    GRIP_CTRL = 0b11

class Command(Enum):
    MOVE = 0x0
    REVERSE = 0x1
    TURN = 0x2
    STOP = 0x3
    INFO = 0x4
    PING = 0x5
    PONG = 0x6
    ERROR = 0x7
    POLL = 0x8
    RESPONSE = 0x9
    CRANE = 0xA

class InfoFlag(Enum):
    BATTERY = 0x0
    TEMPERATURE = 0x1

class CraneFlag(Enum):
    UP = 0x0
    DOWN = 0x1

class PollId(Enum):
    DEGREE = 0x0
    DISTANCE = 0x1
    LINE_SENSOR = 0x2

class ErrorCode(Enum):
    INVALID_CRC = 0x0

AddrField = Literal[0, 1, 2, 3]  # 2 bits
CmdField = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # 4 bits
CrcField = int  # 8 bits (0-255)
ParamField = int  # 50 bits, but we'll mask it

class Frame:
    def __init__(self) -> None:
        self._field: int = 0

    @property
    def addr(self) -> int:
        return (self._field >> 0) & ((1 << ADDR_SIZE_BITS) - 1)

    @property
    def cmd(self) -> int:
        return (self._field >> ADDR_SIZE_BITS) & ((1 << CMD_SIZE_BITS) - 1)

    @property
    def parameter(self) -> int:
        return (self._field >> (ADDR_SIZE_BITS + CMD_SIZE_BITS)) & ((1 << PARAM_SIZE_BITS) - 1)

    @property
    def crc(self) -> int:
        return (self._field >> PAYLOAD_SIZE_BITS) & ((1 << CRC_SIZE_BITS) - 1)

    def set_addr(self, value: AddrField) -> None:
        if value > ((1 << ADDR_SIZE_BITS) - 1):
            raise ValueError(f"Address exceeds {ADDR_SIZE_BITS} bits")
        mask = ((1 << ADDR_SIZE_BITS) - 1) << 0
        self._field = (self._field & ~mask) | (value << 0)

    def set_cmd(self, value: CmdField) -> None:
        if value > ((1 << CMD_SIZE_BITS) - 1):
            raise ValueError(f"Command exceeds {CMD_SIZE_BITS} bits")
        mask = ((1 << CMD_SIZE_BITS) - 1) << ADDR_SIZE_BITS
        self._field = (self._field & ~mask) | (value << ADDR_SIZE_BITS)

    def set_parameter(self, value: ParamField) -> None:
        mask = ((1 << PARAM_SIZE_BITS) - 1) << (ADDR_SIZE_BITS + CMD_SIZE_BITS)
        self._field = (self._field & ~mask) | ((value & ((1 << PARAM_SIZE_BITS) - 1)) << (ADDR_SIZE_BITS + CMD_SIZE_BITS))

    def set_crc(self, value: CrcField) -> None:
        if value > ((1 << CRC_SIZE_BITS) - 1):
            raise ValueError(f"CRC exceeds {CRC_SIZE_BITS} bits")
        mask = ((1 << CRC_SIZE_BITS) - 1) << PAYLOAD_SIZE_BITS
        self._field = (self._field & ~mask) | (value << PAYLOAD_SIZE_BITS)

    def set_raw(self, value: int) -> None:
        if value > ((1 << FRAME_SIZE_BITS) - 1):
            raise ValueError(f"Raw value exceeds {FRAME_SIZE_BITS} bits")
        self._field = value

    @property
    def payload(self) -> int:
        return self._field & ((1 << PAYLOAD_SIZE_BITS) - 1)

    @property
    def raw(self) -> int:
        return self._field
