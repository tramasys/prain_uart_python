from typing import overload
from .protocol import PAYLOAD_SIZE_BITS, Frame, Address, Command, InfoFlag, CraneFlag, PollId, ErrorCode
from .decoder import MoveParams, ReverseParams, TurnParams, InfoParams, ErrorParams, PingParams, PongParams, PollParams, ResponseParams, CraneParams, EmptyParams
from .crc import calculate_crc8_atm

def encode(addr: Address, cmd: Command, params: MoveParams | ReverseParams | TurnParams | InfoParams | EmptyParams | ErrorParams | PingParams | PongParams | PollParams | ResponseParams | CraneParams) -> Frame:
    f = Frame()
    f.set_addr(addr.value)
    f.set_cmd(cmd.value)

    if isinstance(params, EmptyParams):
        f.set_parameter(0)
    elif isinstance(params, ResponseParams):
        f.set_parameter((params.data << 8) | params.poll_id)
    elif isinstance(params, MoveParams):
        f.set_parameter(params.distance)
    elif isinstance(params, ReverseParams):
        f.set_parameter(params.distance)
    elif isinstance(params, TurnParams):
        f.set_parameter(params.angle & 0xFFFF)  # Mask to 16 bits
    elif isinstance(params, InfoParams):
        f.set_parameter(params.flag)
    elif isinstance(params, ErrorParams):
        f.set_parameter(params.error_code)
    elif isinstance(params, PingParams):
        f.set_parameter(params.id)
    elif isinstance(params, PongParams):
        f.set_parameter(params.id)
    elif isinstance(params, PollParams):
        f.set_parameter(params.poll_id)
    elif isinstance(params, CraneParams):
        f.set_parameter(params.flag)

    f.set_crc(calculate_crc8_atm(f.payload, PAYLOAD_SIZE_BITS))
    return f

@overload
def encode_move(addr: Address, distance: int) -> Frame: ...
@overload
def encode_reverse(addr: Address, distance: int) -> Frame: ...
@overload
def encode_turn(addr: Address, angle: int) -> Frame: ...
@overload
def encode_stop(addr: Address) -> Frame: ...
@overload
def encode_info(addr: Address, flags: int) -> Frame: ...
@overload
def encode_info(addr: Address, flag: InfoFlag) -> Frame: ...
@overload
def encode_ping(addr: Address, id: int) -> Frame: ...
@overload
def encode_pong(addr: Address, id: int) -> Frame: ...
@overload
def encode_error(addr: Address, error_code: int) -> Frame: ...
@overload
def encode_error(addr: Address, code: ErrorCode) -> Frame: ...
@overload
def encode_poll(addr: Address, poll_id: int) -> Frame: ...
@overload
def encode_poll(addr: Address, id: PollId) -> Frame: ...
@overload
def encode_response(addr: Address, poll_id: int, data: int) -> Frame: ...
@overload
def encode_response(addr: Address, id: PollId, data: int) -> Frame: ...
@overload
def encode_crane(addr: Address, flag: int) -> Frame: ...
@overload
def encode_crane(addr: Address, flag: CraneFlag) -> Frame: ...

def encode_move(addr: Address, distance: int) -> Frame:
    return encode(addr, Command.MOVE, MoveParams(distance))

def encode_reverse(addr: Address, distance: int) -> Frame:
    return encode(addr, Command.REVERSE, ReverseParams(distance))

def encode_turn(addr: Address, angle: int) -> Frame:
    return encode(addr, Command.TURN, TurnParams(angle))

def encode_stop(addr: Address) -> Frame:
    return encode(addr, Command.STOP, EmptyParams())

def encode_info(addr: Address, flags: int | InfoFlag) -> Frame:
    flag = flags if isinstance(flags, int) else flags.value
    return encode(addr, Command.INFO, InfoParams(flag))

def encode_ping(addr: Address, id: int) -> Frame:
    return encode(addr, Command.PING, PingParams(id))

def encode_pong(addr: Address, id: int) -> Frame:
    return encode(addr, Command.PONG, PongParams(id))

def encode_error(addr: Address, error_code: int | ErrorCode) -> Frame:
    code = error_code if isinstance(error_code, int) else error_code.value
    return encode(addr, Command.ERROR, ErrorParams(code))

def encode_poll(addr: Address, poll_id: int | PollId) -> Frame:
    pid = poll_id if isinstance(poll_id, int) else poll_id.value
    return encode(addr, Command.POLL, PollParams(pid))

def encode_response(addr: Address, poll_id: int | PollId, data: int) -> Frame:
    pid = poll_id if isinstance(poll_id, int) else poll_id.value
    return encode(addr, Command.RESPONSE, ResponseParams(pid, data))

def encode_crane(addr: Address, flag: int | CraneFlag) -> Frame:
    f = flag if isinstance(flag, int) else flag.value
    return encode(addr, Command.CRANE, CraneParams(f))
