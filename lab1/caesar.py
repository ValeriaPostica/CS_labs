ALPHABET = [
    'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'Î',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'Ș', 'T',
    'Ț', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
N = len(ALPHABET)


def clean_text(text):
    text = text.replace('Ş', 'Ș').replace('ş', 'ș')
    text = text.replace('Ţ', 'Ț').replace('ţ', 'ț')
    text = text.upper().replace(" ", "")
    
    for char in text:
        if char not in ALPHABET:
            print(f"Error: Character '{char}' is not allowed! Use only Romanian alphabet letters.")
            return None
    return text


def get_shift_key():
    while True:
        try:
            k = int(input("Enter numeric key k (1-30): "))
            if 1 <= k <= 30:
                return k
            print("The key must be an integer between 1 and 30!")
        except ValueError:
            print("Please enter a valid integer!")


def get_keyword():
    while True:
        keyword = input("Enter keyword (at least 7 letters): ")
        cleaned = clean_text(keyword)
        if cleaned and len(cleaned) >= 7:
            return cleaned
        elif cleaned:
            print("The keyword must be at least 7 characters long!")


def generate_permuted_alphabet(keyword):
    permuted = []
    
    for char in keyword:
        if char not in permuted:
            permuted.append(char)
            
    for char in ALPHABET:
        if char not in permuted:
            permuted.append(char)
            
    return permuted


def simple_caesar(text, k, operation):
    cleaned = clean_text(text)
    if not cleaned:
        return None
    
    result = []
    for char in cleaned:
        pos = ALPHABET.index(char)
        
        if operation == 'E':
            new_pos = (pos + k) % N
        else:
            new_pos = (pos - k) % N
            
        result.append(ALPHABET[new_pos])
        
    return "".join(result)


def permuted_caesar(text, k1, permuted_alphabet, operation):
    cleaned = clean_text(text)
    if not cleaned:
        return None
    
    result = []
    for char in cleaned:
        pos = permuted_alphabet.index(char)
        
        if operation == 'E':
            new_pos = (pos + k1) % N
        else:
            new_pos = (pos - k1) % N
            
        result.append(permuted_alphabet[new_pos])
        
    return "".join(result)


def main():
    print("Laboratory Work No. 1 - Caesar Cipher")
    print("1. Task 1.1: Simple Caesar Cipher")
    print("2. Task 1.2: Caesar Cipher with Permutation")
    
    choice = input("Select task (1 or 2): ").strip()
    if choice not in ['1', '2']:
        print("Invalid choice!")
        return

    operation = input("Select operation - (E)ncrypt or (D)ecrypt: ").strip().upper()
    if operation not in ['E', 'D']:
        print("Invalid operation!")
        return

    if choice == '1':
        k = get_shift_key()
        while True:
            text = input("Enter text: ")
            result = simple_caesar(text, k, operation)
            if result:
                print(f"\nResult: {result}")
                break

    elif choice == '2':
        k1 = get_shift_key()
        k2 = get_keyword()
        
        permuted_alphabet = generate_permuted_alphabet(k2)
        print("\nGenerated permuted alphabet:")
        print("".join(permuted_alphabet))
        print("-" * 40)

        while True:
            text = input("Enter text: ")
            result = permuted_caesar(text, k1, permuted_alphabet, operation)
            if result:
                print(f"\nResult: {result}")
                break


if __name__ == "__main__":
    main()