import unittest
from prain_uart import *
from prain_uart.crc import calculate_crc8_atm
from prain_uart.protocol import PAYLOAD_SIZE_BITS

class TestPrainUart(unittest.TestCase):
    def test_move_round_trip(self):
        f = encode_move(Address.RASPBERRY_HAT, 1234)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.RASPBERRY_HAT)
        self.assertEqual(dec.command, Command.MOVE)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, MoveParams)
        self.assertEqual(params.distance, 1234)

    def test_reverse_round_trip(self):
        f = encode_reverse(Address.MOTION_CTRL, 5678)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.MOTION_CTRL)
        self.assertEqual(dec.command, Command.REVERSE)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, ReverseParams)
        self.assertEqual(params.distance, 5678)

    def test_turn_round_trip(self):
        f = encode_turn(Address.GRIP_CTRL, -420)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.GRIP_CTRL)
        self.assertEqual(dec.command, Command.TURN)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, TurnParams)
        self.assertEqual(params.angle, -420)

    def test_stop_round_trip(self):
        f = encode_stop(Address.GRIP_CTRL)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.GRIP_CTRL)
        self.assertEqual(dec.command, Command.STOP)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, EmptyParams)

    def test_info_round_trip(self):
        f = encode_info(Address.RASPBERRY_HAT, InfoFlag.BATTERY)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.RASPBERRY_HAT)
        self.assertEqual(dec.command, Command.INFO)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, InfoParams)
        self.assertEqual(params.flag, InfoFlag.BATTERY.value)

    def test_ping_round_trip(self):
        f = encode_ping(Address.MOTION_CTRL, 42)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.MOTION_CTRL)
        self.assertEqual(dec.command, Command.PING)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, PingParams)
        self.assertEqual(params.id, 42)

    def test_pong_round_trip(self):
        f = encode_pong(Address.RASPBERRY_HAT, 42)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.RASPBERRY_HAT)
        self.assertEqual(dec.command, Command.PONG)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, PongParams)
        self.assertEqual(params.id, 42)

    def test_error_round_trip(self):
        f = encode_error(Address.GRIP_CTRL, 0x1234)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.GRIP_CTRL)
        self.assertEqual(dec.command, Command.ERROR)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, ErrorParams)
        self.assertEqual(params.error_code, 0x1234)

    def test_poll_round_trip(self):
        f = encode_poll(Address.MOTION_CTRL, PollId.DEGREE)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.MOTION_CTRL)
        self.assertEqual(dec.command, Command.POLL)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, PollParams)
        self.assertEqual(params.poll_id, PollId.DEGREE.value)

    def test_response_round_trip(self):
        f = encode_response(Address.MOTION_CTRL, PollId.DISTANCE, 420)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.MOTION_CTRL)
        self.assertEqual(dec.command, Command.RESPONSE)
        self.assertTrue(dec.verify_crc())
        params = dec.get_params()
        self.assertIsInstance(params, ResponseParams)
        self.assertEqual(params.poll_id, PollId.DISTANCE.value)
        self.assertEqual(params.data, 420)

    def test_crane_round_trip(self):
        f = encode_crane(Address.RASPBERRY_HAT, CraneFlag.UP)
        dec = Decoder(f.raw)
        self.assertEqual(dec.address, Address.RASPBERRY_HAT)
        self.assertEqual(dec.command, Command.CRANE)
        self.assertTrue(dec.verify_crc())
        self.assertEqual(dec.raw_parameters, CraneFlag.UP.value)
        params = dec.get_params()
        self.assertIsInstance(params, CraneParams)
        self.assertEqual(params.flag, CraneFlag.UP.value)

    def test_valid_crc(self):
        f = encode_ping(Address.MOTION_CTRL, 42)
        dec = Decoder(f.raw)
        self.assertTrue(dec.verify_crc())

    def test_invalid_crc(self):
        f = encode_ping(Address.MOTION_CTRL, 42)
        raw = f.raw ^ (0xFF << 56)  # Flip CRC bits
        dec = Decoder(raw)
        self.assertFalse(dec.verify_crc())

    def test_unknown_command_throws(self):
        f = Frame()
        f.set_addr(Address.RASPBERRY_HAT.value)
        f.set_cmd(0xF)  # Invalid command (15)
        f.set_parameter(0)
        f.set_crc(calculate_crc8_atm(f.payload, PAYLOAD_SIZE_BITS))
        dec = Decoder(f.raw)
        with self.assertRaises(ValueError):
            dec.get_params()

if __name__ == "__main__":
    unittest.main()
