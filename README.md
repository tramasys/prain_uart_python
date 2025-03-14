# prain_uart_python

A python library providing an encoder and decoder for our 64-bit UART protocol used in the PREN project.

## Features
- **Typed API**: Uses Python's `typing` module for strong type hints (e.g., `Literal`, `Union`, `NamedTuple`).
- **Frame Structure**: 2-bit address, 4-bit command, 50-bit parameters, 8-bit CRC (total 64 bits).
- **Commands**: Supports `MOVE`, `REVERSE`, `TURN`, `STOP`, `INFO`, `PING`, `PONG`, `ERROR`, `POLL`, `RESPONSE`, and `CRANE`.
- **CRC-8-ATM**: Implements CRC-8 checksum calculation for data integrity.
- **Tested**: Comprehensive unit tests ensure compatibility with the C++ version.

## Installation
Requires Python 3.10 or higher.

1. **Clone the Repository**:
```bash
git clone <repository-url>
cd prain_uart_python
pip install .
pip install mypy
```

## Usage
The library provides encode_* functions to create frames and a Decoder class to parse them. Below are examples:

### Encoding a frame

```python
from prain_uart import encode_response, Address, PollId, Decoder
frame = encode_response(Address.MOTION_CTRL, PollId.DISTANCE, 420)
raw_frame = frame.raw
print(f"Raw frame: {hex(raw_frame)}")
```

### Decoding a frame
```python
decoder = Decoder(raw_frame)
print(f"Address: {decoder.address}")
print(f"Command: {decoder.command}")
print(f"CRC valid: {decoder.verify_crc()}")

params = decoder.get_params()
if isinstance(params, ResponseParams):
    print(f"Poll ID: {params.poll_id}, Data: {params.data}")
```

## Testing
```bash
python -m unittest tests/test_prain_uart.py
mypy tests/test_prain_uart.py
```
