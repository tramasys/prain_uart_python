from typing import Union, NamedTuple
from .protocol import PAYLOAD_SIZE_BITS, Frame, Command, Address
from .crc import calculate_crc8_atm

# Parameter types as NamedTuples for immutability and type hints
class MoveParams(NamedTuple):
    distance: int  # uint16_t equivalent (0-65535)

class ReverseParams(NamedTuple):
    distance: int

class TurnParams(NamedTuple):
    angle: int  # int16_t equivalent (-32768 to 32767)

class InfoParams(NamedTuple):
    flag: int  # uint8_t

class ErrorParams(NamedTuple):
    error_code: int  # uint16_t

class PingParams(NamedTuple):
    id: int  # uint8_t

class PongParams(NamedTuple):
    id: int

class PollParams(NamedTuple):
    poll_id: int  # uint8_t

class ResponseParams(NamedTuple):
    poll_id: int
    data: int  # uint16_t

class EmptyParams(NamedTuple):
    pass

Params = Union[
    MoveParams, ReverseParams, TurnParams, InfoParams, EmptyParams,
    ErrorParams, PingParams, PongParams, PollParams, ResponseParams
]

class Decoder:
    def __init__(self, frame: Frame | int) -> None:
        self._frame = Frame()
        if isinstance(frame, int):
            self._frame.set_raw(frame)
        else:
            self._frame = frame

    @property
    def address(self) -> Address:
        return Address(self._frame.addr)

    @property
    def command(self) -> Command:
        return Command(self._frame.cmd)

    @property
    def raw_parameters(self) -> int:
        return self._frame.parameter

    @property
    def crc(self) -> int:
        return self._frame.crc

    def verify_crc(self) -> bool:
        return calculate_crc8_atm(self._frame.payload, PAYLOAD_SIZE_BITS) == self._frame.crc

    def get_params(self) -> Params:
        param = self._frame.parameter
        match self.command:
            case Command.MOVE:
                return MoveParams(distance=param & 0xFFFF)
            case Command.REVERSE:
                return ReverseParams(distance=param & 0xFFFF)
            case Command.TURN:
                # Handle int16_t sign extension
                value = param & 0xFFFF
                return TurnParams(angle=value if value < 0x8000 else value - 0x10000)
            case Command.STOP:
                return EmptyParams()
            case Command.INFO:
                return InfoParams(flag=param & 0xFF)
            case Command.PING:
                return PingParams(id=param & 0xFF)
            case Command.PONG:
                return PongParams(id=param & 0xFF)
            case Command.ERROR:
                return ErrorParams(error_code=param & 0xFFFF)
            case Command.POLL:
                return PollParams(poll_id=param & 0xFF)
            case Command.RESPONSE:
                return ResponseParams(poll_id=param & 0xFF, data=(param >> 8) & 0xFFFF)
            case Command.GRIP:
                return EmptyParams()
            case Command.RELEASE:
                return EmptyParams()
            case _:
                raise ValueError(f"Unknown command: {self.command}")
