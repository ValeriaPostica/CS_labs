import unittest
from unittest.mock import patch
from io import StringIO
import random
from des_round import calculate_right_half, generate_inputs, main

class TestDesRound(unittest.TestCase):
    def test_task_2_10(self):
        s, p_s, right = calculate_right_half(
            ("0000", "0001", "0010", "0011",
             "0100", "0101", "0110", "0111"),
            "00010010001101000101011001111000",
        )

        self.assertEqual(s, "00000001001000110100010101100111")
        self.assertEqual(p_s, "10000000010101100110110000101100")
        self.assertEqual(right, "10010010011000100011101001010100")
        self.assertEqual(int(right, 2), 0x92623A54)

    def test_zero_s(self):
        s, p_s, right = calculate_right_half(("0000",) * 8, "1" * 32)
        self.assertEqual(p_s, "0" * 32)
        self.assertEqual(right, "1" * 32)

    def test_main_displays_complete_trace(self):
        inputs = [
            "1",
            "0000", "0001", "0010", "0011",
            "0100", "0101", "0110", "0111",
            "00010010001101000101011001111000",
        ]
        with patch("builtins.input", side_effect=inputs), patch(
            "sys.stdout", new_callable=StringIO
        ) as output:
            main()

        text = output.getvalue()
        self.assertIn("1. Input values", text)
        self.assertIn("2. S-box concatenation", text)
        self.assertIn("3. DES P permutation", text)
        self.assertIn("4. XOR calculation", text)
        self.assertIn("Output position | Input position | Input bit", text)
        self.assertIn("Position | L(i-1) bit | P(S) bit | R(i) bit", text)
        self.assertIn("R(i) in hexadecimal = 92623A54", text)

    def test_generate_inputs_returns_valid_values(self):
        sbox_outputs, left_previous = generate_inputs(random.Random(10))

        self.assertEqual(len(sbox_outputs), 8)
        self.assertTrue(all(len(value) == 4 for value in sbox_outputs))
        self.assertTrue(all(set(value) <= {"0", "1"} for value in sbox_outputs))
        self.assertEqual(len(left_previous), 32)
        self.assertTrue(set(left_previous) <= {"0", "1"})

    def test_main_runs_generated_calculation(self):
        with patch("builtins.input", return_value="2"), patch(
            "des_round.generate_inputs",
            return_value=(
                ("0000", "0001", "0010", "0011",
                 "0100", "0101", "0110", "0111"),
                "00010010001101000101011001111000",
            ),
        ), patch("sys.stdout", new_callable=StringIO) as output:
            main()

        text = output.getvalue()
        self.assertIn("Generated input values:", text)
        self.assertIn("R(i) in hexadecimal = 92623A54", text)


if __name__ == "__main__":
    unittest.main()
