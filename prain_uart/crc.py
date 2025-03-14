def calculate_crc8_atm(data: int, bits: int) -> int:
    """Calculate CRC-8-ATM (polynomial 0x07) over the given number of bits."""
    crc = 0x00
    poly = 0x07

    mask = (1 << bits) - 1
    data &= mask

    for i in range(bits - 1, -1, -1):
        bit = (data >> i) & 1
        # XOR the MSB of crc with the input bit
        crc ^= (bit << 7)
        # Shift left and XOR with polynomial if MSB was 1
        for _ in range(8):
            msb = crc & 0x80  # Check MSB
            crc = (crc << 1) & 0xFF  # Shift left, mask to 8 bits
            if msb:
                crc ^= poly

    return crc
