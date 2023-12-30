import random
import os
import itertools
import time


# Function to calculate check digit using Modulo-11 algorithm
def calculate_modulo_11_check_digit(digits):
    if len(digits) != 12 or not digits.isdigit():
        return "Invalid input. Please enter 12 numeric digits."

    weights = [2, 3, 4, 5, 6, 7] * 2
    total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
    remainder = total % 11
    check_digit = 11 - remainder
    if check_digit == 10:
        return "X"
    elif check_digit == 11:
        return "0"
    else:
        return str(check_digit)

# Function to calculate check digit for ISBN-13
def calculate_isbn_13_check_digit(digits):
    if len(digits) != 12 or not digits.isdigit():
        return "Invalid input. Please enter 12 numeric digits."

    weights = [1, 3] * 6
    total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
    check_digit = 10 - (total % 10)
    if check_digit == 10:
        return "0"
    else:
        return str(check_digit)

# Menu for the user to choose the type of check digit algorithm
def mainDC():
    print("\nCheck Digit Creator")
    print("1. Modulo-11")
    print("2. ISBN-13")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        input_digits = input("\nEnter 12 digits: ")
        print("Check Digit:", calculate_modulo_11_check_digit(input_digits))
    elif choice == '2':
        input_digits = input("\nEnter 12 digits: ")
        print("Check Digit:", calculate_isbn_13_check_digit(input_digits))
    else:
        print("\nInvalid choice")

# Function to generate a random 256-bit key with numbers and letters
def generate_key():
    import os
    import random
    import string
    key_characters = string.ascii_letters + string.digits  # Letters and numbers
    key = ''.join(random.choice(key_characters) for _ in range(43))  # 43 characters for 256 bits
    return key

# Function to encrypt the message using the key
def encrypt(message, key):
    import base64
    key_as_bytes = key.encode()  # Convert key to bytes
    encrypted = bytearray()
    for i in range(len(message)):
        encrypted.append(message[i] ^ key_as_bytes[i % len(key_as_bytes)])
    encrypted_bytes = bytes(encrypted)
    encoded_message = base64.b64encode(encrypted_bytes).decode('utf-8')  # Encode the encrypted message using Base64
    return encoded_message

# Function to store the key securely
def store_key(key):
    print("Key securely stored.")

# Function to decrypt the encrypted message
def decrypt(encrypted_message, key):
    import base64
    key_as_bytes = key.encode()
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted = bytearray()
    for i in range(len(encrypted_bytes)):
        decrypted.append(encrypted_bytes[i] ^ key_as_bytes[i % len(key_as_bytes)])
    decrypted_message = bytes(decrypted).decode('utf-8')
    return decrypted_message



# Function to generate a random MAC address
def generate_mac_address():
    mac = [ 0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Function to generate a MAC address with a specific vendor
def generate_specific_mac_address(vendor):
    mac = [ int(vendor[i:i+2], 16) for i in range(0, len(vendor), 2) ]
    mac += [ random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Function to generate a random IPv4 address
def generate_ipv4_address():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Function to generate a random IPv6 address
def generate_ipv6_address():
    return ':'.join('{:04x}'.format(random.randint(0, 0xffff)) for _ in range(8))

# Function to generate passwords and write them to a file
def estimate_file_size(allowed_chars, min_length, max_length):
    # Calculate the number of possible passwords
    total_passwords = sum(len(allowed_chars) ** length for length in range(min_length, max_length + 1))

    # Estimate the file size
    average_password_length = (min_length + max_length) / 2  # Assuming an average length
    average_character_size = 1  # Assuming each character takes 1 byte
    estimated_file_size_bytes = total_passwords * average_password_length * average_character_size
    if allowed_chars == "0123456789":
        estimated_file_size_kb = estimated_file_size_bytes / 1024                       # Convert to kilobytes, as its small
        return estimated_file_size_kb
    else:
        estimated_file_size_tb = estimated_file_size_bytes / 9094947017729.282          # Convert to TB, as its large, scarely large
        return estimated_file_size_tb

    
def generate_passwords(allowed_chars, min_length, max_length):
    file_path = os.path.join(os.path.expanduser("~"), "Desktop", "BruteForce.txt")  # File path for the desktop

    # Estimate the file size
    estimated_file_size_kb = estimate_file_size(allowed_chars, min_length, max_length)
    estimated_file_size_tb = estimate_file_size(allowed_chars, min_length, max_length)
    if allowed_chars == "0123456789":
        print(f"Estimated file size: {estimated_file_size_kb:.2f} KB")
    else:
        print(f"Estimated file size: {estimated_file_size_tb:.2f} TB")
        
    # Check if the user wants to proceed
    confirm = input("Do you want to proceed with generating the password list? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return

    print("\nLoading...")
    with open(file_path, 'w') as file:
        for length in range(min_length, max_length + 1):
            for password_tuple in itertools.product(allowed_chars, repeat=length):
                password = ''.join(password_tuple)
                file.write(password + '\n')

    print(f"\nPassword list generated and saved to {file_path}")
    print("Completed Your Brute Force Text File")

# Menu for the user to choose the type of address or password generation
def main():
    print("Menu:")
    print("1. Address Generator")
    print("2. Password Generator")
    print("3. Check Digit Generator")
    print("4. C: Scan")
    print("99. Exit")
    choice = input("Enter your choice (1, 2, 3, 4, or 99): ")
    


    if choice == '1':
        print("\nAddress Generator")
        print("1. MAC Address")
        print("2. IP Address")
        address_choice = input("Enter your choice (1 or 2): ")
        if address_choice == '1':
            print("\nMAC Address Options:")
            print("1. Random vendor")
            print("2. Specific vendor")
            mac_choice = input("Enter your choice (1 or 2): ")
            if mac_choice == '1':
                print("\nGenerated MAC Address:", generate_mac_address())
            elif mac_choice == '2':
                vendor = input("\nEnter the specific vendor OUI (e.g., 001122): ") # Will need a error checking method
                print("\nGenerated MAC Address:", generate_specific_mac_address(vendor))
            else:
                print("\nInvalid MAC choice")
        elif address_choice == '2':
            print("\nIP Address Options:")
            print("1. Generate IPv4 address")
            print("2. Generate IPv6 address")
            ip_choice = input("Enter your choice (1 or 2): ")
            if ip_choice == '1':
                print("\nGenerated IPv4 Address:", generate_ipv4_address())
            elif ip_choice == '2':
                print("\nGenerated IPv6 Address:", generate_ipv6_address())
            else:
                print("\nInvalid IP choice")
        else:
            print("\nInvalid choice")
            
    elif choice == '2':
        print("\nWarning: This is a very resource-intensive operation and may create a large text file if option STRING is chosen!")
        print("Please read the warnings carefully before proceeding.")
        print("Notepad and Notepad++ have a limit which is 512MB and ~2GB respectively, So using a software like EmEditor (Not sponsored) allows upto 16TB")
        allowed_chars_choice = input("\nEnter 'N' for numerical only or 'S' for string (alphabets) only: ")
        if allowed_chars_choice.upper() == 'N':
            allowed_chars = '0123456789'
        elif allowed_chars_choice.upper() == 'S':
            allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=01234567890<,>.?/:;{[}]|~`'
        else:
            print("Invalid choice. Please enter 'N' or 'S'.")
            return

        min_length = int(input("Enter the minimum length for the passwords: "))
        max_length = int(input("Enter the maximum length for the passwords: "))
        generate_passwords(allowed_chars, min_length, max_length)
        
        
    elif choice == '3':
        if __name__ == "__main__":
            mainDC()
    elif choice == '4':
        
        # Warning
        print("\nThis is a new addition so it may be buggy, It also does not have ANY menu integrated in here, usually it takes")
        print("20 seconds so bear with it or press Ctrl+C")
        
        # Define the path to the C: drive
        c_drive_path = "C:\\"

        # Prompt the user to enter the name of the text file with input validation
        while True:
            file_name = input("\nEnter the name of the text file, including .txt: ")
            if file_name.endswith(".txt"):
                break
            else:
                print("\nInvalid file name. Please include the .txt extension.")

        # Estimate the file size
        num_folders = sum([len(dirs) for _, dirs, _ in os.walk(c_drive_path)])
        num_files = sum([len(files) for _, _, files in os.walk(c_drive_path)])
        file_size = (num_folders * 20 + num_files * 30) / (1024 * 1024)  # Convert to megabytes
        file_size_rounded = round(file_size, 2)  # Round to two decimal places

        # Warn about the potential size and duration
        print("")
        print(f"Warning: The estimated file size is {file_size_rounded} megabytes. This may take some time to generate. Press Ctrl+C to Cancel")
        print("Loading...")

        # Estimate the time it might take
        start_time_estimate = time.time()

        # Write the folders and subfolders to the text file
        with open(file_name, "w", encoding="utf-8") as file:
            for root, dirs, files in os.walk(c_drive_path):
                file.write(root + "\n")
                for dir in dirs:
                    file.write(os.path.join(root, dir) + "\n")

        end_time_estimate = time.time()
        duration_estimate = end_time_estimate - start_time_estimate
        print("")
        print(f"This took: {duration_estimate:.2f} seconds.")
        print("\nOpening File...")
        # Open the text file for viewing
        os.startfile(file_name)
        print("Opened!")
        print("Completed Task, Found bugs? Report them")
    else:
        print("\nInvalid choice")

print(r"_________                               __                   ___ ___                __            ")
print(r"\_   ___ \  ____   _____ ______  __ ___/  |_  ___________   /   |   \_____    ____ |  | __  ______")
print(r"/    \  \/ /  _ \ /     \\____ \|  |  \   __\/ __ \_  __ \ /    ~    \__  \ _/ ___\|  |/ / /  ___/")
print(r"\     \___(  <_> )  Y Y  \  |_> >  |  /|  | \  ___/|  | \/ \    Y    // __ \\  \___|    <  \___ \ ")
print(r" \______  /\____/|__|_|  /   __/|____/ |__|  \___  >__|     \___|_  /(____  /\___  >__|_ \/____  >")
print(r"        \/             \/|__|                    \/               \/      \/     \/     \/     \/ ")
print("\nVersion 1.1.0")

while True:
    if __name__ == "__main__":
        print("")
        main()