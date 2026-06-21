import csv
import time

# Define character sets for password generation
capitals = ['A', 'B', 'C', 'D', 'E']
lowercase=['a', 'b', 'c', 'd', 'e']
digits = ['1', '2', '3', '4', '5']
symbols = ['$', '&', '%']


def password_validation():
    """Get valid password length from user (minimum 4 characters)"""
    while True:
        user_input = input("Enter your password length: ")

        # Check if input is numeric
        if not user_input.isnumeric():
            print("Password must be a number.")
            continue

        password_length = int(user_input)
        
        # Ensure minimum length requirement
        if password_length < 4:
            print("Password must be at least 4 characters.")
            continue

        return password_length




def generate_passwords(current, length, writer, capitals_count=0, lowercase_count=0,
                       digits_count=0, symbols_count=0, valid_index=1):
    """
    Recursively generate all valid passwords that meet the criteria:
    - First character must be a letter
    - Must contain at least 1 capital, 1 lowercase, 1 digit, 1 symbol
    - Maximum 2 capitals and 2 symbols allowed
    """

    # Early pruning - check if remaining length can satisfy requirements
    remaining = length - len(current)
    needed_capitals = max(0, 1 - capitals_count)
    needed_lowercase = max(0, 1 - lowercase_count)
    needed_digits = max(0, 1 - digits_count)
    needed_symbols = max(0, 1 - symbols_count)
    total_needed = needed_capitals + needed_lowercase + needed_digits + needed_symbols
    
    # If we don't have enough space left to meet requirements, prune this branch
    if remaining < total_needed:
        return valid_index
    
    # Check if we can still meet max constraints
    if capitals_count > 2 or symbols_count > 2:
        return valid_index

    # Combine all possible characters
    chars = capitals + lowercase + digits + symbols

    # Base case: password has reached desired length
    if len(current) == length:
        # Check if all required categories are present
        if capitals_count == 0 or lowercase_count == 0 or digits_count == 0 or symbols_count == 0:
            return valid_index  # invalid password, skip

        # Write valid password to CSV with its index
        writer.writerow([f"{valid_index}:{''.join(current)}"])
        return valid_index + 1  # increment index for next password


    # Prioritize characters that satisfy missing requirements first
    # This helps find valid passwords faster
    
    # try characters from categories we still need
    needed_chars = []
    if needed_capitals > 0:
        needed_chars.extend(capitals)
    if needed_lowercase > 0:
        needed_chars.extend(lowercase)
    if needed_digits > 0:
        needed_chars.extend(digits)
    if needed_symbols > 0:
        needed_chars.extend(symbols)
    
    # Add remaining characters
    all_chars = needed_chars + [c for c in chars if c not in needed_chars]

    # Recursive case: try adding each possible character
    for c in all_chars: 
        # Rule: first character must be a letter
        if len(current) == 0 and c not in capitals + lowercase:
            continue  # skip invalid first character

        # Rule: no more than 2 capitals
        if c in capitals and capitals_count >= 2:
            continue  # skip if adding this capital exceeds limit

        # Rule: no more than 2 symbols
        if c in symbols and symbols_count >= 2:
            continue  # skip if adding this symbol exceeds limit




        # Update counts for next recursive call
        new_capitals = capitals_count + (1 if c in capitals else 0)  # CHANGED: More efficient
        new_lowercase = lowercase_count + (1 if c in lowercase else 0)
        new_digits = digits_count + (1 if c in digits else 0)
        new_symbols = symbols_count + (1 if c in symbols else 0)

        # Recursive call with new character added
        valid_index = generate_passwords(current + [c], length, writer,
                                         new_capitals, new_lowercase,
                                         new_digits, new_symbols,
                                         valid_index)


    return valid_index  # return updated index to caller




# --- MAIN EXECUTION ---
start_time = time.time()

# Open output file
with open("passwords.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Get password length from user
    length = password_validation() 
    
    # Need at least 4 characters (one from each category)
    if length < 4:
        print("Password must be at least 4 characters to include all categories.")
    else:
        # Generate all valid passwords
        total_passwords = generate_passwords([], length, writer) - 1
        print(f"Generated {total_passwords} valid passwords")

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")

