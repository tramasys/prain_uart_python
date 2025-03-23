def calculate_crc8_atm(data: int, bit_length: int) -> int:
    """Calculate CRC-8-ATM (polynomial 0x07) over the given number of bits."""
    crc = 0
    for i in range(bit_length):
        # Process bit-by-bit (MSB first)
        bit = ((data >> (bit_length - 1 - i)) & 1) ^ ((crc >> 7) & 1)
        crc = ((crc << 1) & 0xFF)
        if bit:
            crc ^= 0x07 # CRC8-ATM polynomial: x^8 + x^2 + x + 1 (0x07)

    return crc
