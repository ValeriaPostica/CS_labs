import random
import unittest
from pathlib import Path

P_TABLE = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25,
]

def check_bits(value, size, name):
    value = value.replace(" ", "")
    if len(value) != size or any(bit not in "01" for bit in value):
        raise ValueError(f"{name} must contain exactly {size} bits.")
    return value

def permute(bits):
    return "".join(bits[position - 1] for position in P_TABLE)

def xor(left, right):
    return "".join("0" if a == b else "1" for a, b in zip(left, right))


def print_input_table(sbox_outputs, left_previous):
    print("\n1. Input values")
    print("+----------+--------+")
    print("| Value    | Bits   |")
    print("+----------+--------+")
    for index, value in enumerate(sbox_outputs, 1):
        print(f"| S{index}(B{index})  | {value} |")
    print(f"| L(i-1)   | {left_previous} |")
    print("+----------+--------+")


def print_s_concatenation(sbox_outputs, s):
    print("\n2. S-box concatenation")
    print("+----------+--------+")
    print("| Component| Value  |")
    print("+----------+--------+")
    for index, value in enumerate(sbox_outputs, 1):
        print(f"| S{index}(B{index})  | {value} |")
    print("+----------+--------+")
    print(f"S = {' || '.join(sbox_outputs)}")
    print(f"S = {s}")


def print_permutation_table(s):
    p_s = permute(s)
    print("\n3. DES P permutation")
    print("P table:")
    print(" ".join(f"{position:2}" for position in P_TABLE))
    print("Output position | Input position | Input bit")
    print("----------------+----------------+----------")
    for output_position, input_position in enumerate(P_TABLE, 1):
        print(
            f"{output_position:15} | {input_position:14} | "
            f"{s[input_position - 1]}"
        )
    print(f"P(S) = {p_s}")


def print_xor_table(left_previous, p_s, right_current):
    print("\n4. XOR calculation")
    print("Position | L(i-1) bit | P(S) bit | R(i) bit")
    print("---------+------------+----------+---------")
    for position, (left_bit, permuted_bit, result_bit) in enumerate(
        zip(left_previous, p_s, right_current), 1
    ):
        print(
            f"{position:8} | {left_bit:10} | {permuted_bit:8} | "
            f"{result_bit:8}"
        )
    print(f"L(i-1)       = {left_previous}")
    print(f"P(S)         = {p_s}")
    print(f"R(i)         = {right_current}")


def calculate_right_half(sbox_outputs, left_previous):
    if len(sbox_outputs) != 8:
        raise ValueError("Exactly 8 S-box outputs are required.")

    sbox_outputs = [
        check_bits(value, 4, f"S{i}(B{i})")
        for i, value in enumerate(sbox_outputs, 1)
    ]
    left_previous = check_bits(left_previous, 32, "L(i-1)")

    s = "".join(sbox_outputs)
    p_s = permute(s)
    right_current = xor(left_previous, p_s)
    return s, p_s, right_current


def read_manual_inputs():
    """Read the eight S-box outputs and the previous left half."""
    print("Enter the eight 4-bit S-box outputs.")
    sbox_outputs = [
        input(f"S{i}(B{i}) = ").strip()
        for i in range(1, 9)
    ]
    left_previous = input("L(i-1) = ").strip()
    return sbox_outputs, left_previous


def generate_inputs(rng=None):
    """Generate valid random inputs."""
    rng = rng or random.SystemRandom()
    sbox_outputs = [
        format(rng.getrandbits(4), "04b")
        for _ in range(8)
    ]
    left_previous = format(rng.getrandbits(32), "032b")
    return sbox_outputs, left_previous


def display_calculation(sbox_outputs, left_previous):
    """Validate inputs and display the complete DES calculation."""
    try:
        s, p_s, right_current = calculate_right_half(
            sbox_outputs, left_previous
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    normalized_left = left_previous.replace(" ", "")
    print_input_table(sbox_outputs, normalized_left)
    print_s_concatenation(sbox_outputs, s)
    print_permutation_table(s)
    print_xor_table(normalized_left, p_s, right_current)
    print(f"R(i) in hexadecimal = {int(right_current, 2):08X}")


def run_tests():
    loader = unittest.defaultTestLoader
    test_directory = Path(__file__).resolve().parent
    suite = loader.discover(start_dir=str(test_directory), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def main():
    print("DES task 2.10")
    print("\nChoose an option:")
    print("1. Enter the values manually")
    print("2. Generate random valid values")
    print("3. Run automated tests")
    choice = input("Option (1-3) = ").strip()

    if choice == "1":
        sbox_outputs, left_previous = read_manual_inputs()
        display_calculation(sbox_outputs, left_previous)
    elif choice == "2":
        sbox_outputs, left_previous = generate_inputs()
        print("\nGenerated input values:")
        for index, value in enumerate(sbox_outputs, 1):
            print(f"S{index}(B{index}) = {value}")
        print(f"L(i-1) = {left_previous}")
        display_calculation(sbox_outputs, left_previous)
    elif choice == "3":
        print("\nRunning automated tests...\n")
        if run_tests():
            print("\nAll automated tests passed.")
        else:
            print("\nSome automated tests failed.")
    else:
        print("Error: choose option 1, 2, or 3.")


if __name__ == "__main__":
    main()
