import pandas as pd
import re
import os

def audit_nemotron_bit_row(prompt: str, answer: str) -> bool:
    """
    Reverse-engineers the hidden bitwise rule from the examples.
    If the examples are hallucinatory or the math is broken, returns False.
    """
    # 1. Extract the 8 examples and the final question
    examples = re.findall(r'([01]{8})\s*->\s*([01]{8})', str(prompt))
    q_match = re.search(r'output for:\s*([01]{8})', str(prompt))
    
    if not examples or not q_match:
        return True # Not a bitwise puzzle, keep it for other tests
        
    q_val = int(q_match.group(1), 2)
    ans_str = str(answer).strip()
    
    try:
        # Find the last binary string in the answer
        a_val = int(re.findall(r'[01]{8}', ans_str)[-1], 2)
    except IndexError:
        return False
        
    # 2. Try to deduce the secret rule mathematically
    # Rule 1: NOT (Invert all bits)
    if all( (~int(ex[0], 2) & 0xFF) == int(ex[1], 2) for ex in examples ):
        return (~q_val & 0xFF) == a_val
        
    # Rule 2: REVERSE (Reverse the string)
    if all( int(ex[0][::-1], 2) == int(ex[1], 2) for ex in examples ):
        return int(q_match.group(1)[::-1], 2) == a_val
        
    # Rule 3: XOR, AND, OR with a Constant (Brute-force 0-255)
    for k in range(256):
        if all( (int(ex[0], 2) ^ k) == int(ex[1], 2) for ex in examples ):
            return (q_val ^ k) == a_val
        if all( (int(ex[0], 2) & k) == int(ex[1], 2) for ex in examples ):
            return (q_val & k) == a_val
        if all( (int(ex[0], 2) | k) == int(ex[1], 2) for ex in examples ):
            return (q_val | k) == a_val

    # Rule 4: Bit Shifts
    if all( ((int(ex[0], 2) << 1) & 0xFF) == int(ex[1], 2) for ex in examples ):
        return ((q_val << 1) & 0xFF) == a_val
    if all( (int(ex[0], 2) >> 1) == int(ex[1], 2) for ex in examples ):
        return (q_val >> 1) == a_val

    # If NO rule mathematically fits all 8 examples perfectly, the data is poisoned.
    return False

def run_local_audit():
    file_path = "train.csv"
    
    if not os.path.exists(file_path):
        print(f"[ERROR] {file_path} not found.")
        return

    print("Loading local dataset...")
    df = pd.read_csv(file_path)
    
    initial_count = len(df)
    
    # Isolate bit manipulation rows for tracking
    bit_rows = df[df['prompt'].str.contains('secret bit manipulation rule', na=False, case=False)]
    print(f"Total Bit Manipulation puzzles found: {len(bit_rows)}")
    
    print("\nExecuting aggressive deterministic math verification...")
    # Explicitly use column names
    df['is_valid'] = df.apply(lambda row: audit_nemotron_bit_row(row['prompt'], row['answer']), axis=1)
    
    clean_df = df[df['is_valid'] == True].copy()
    clean_df = clean_df.drop(columns=['is_valid'])
    
    final_count = len(clean_df)
    dropped = initial_count - final_count
    
    print("\n--- AUDIT RESULTS ---")
    print(f"Total rows scanned: {initial_count}")
    print(f"Poisoned rows dropped: {dropped}")
    print(f"Clean rows remaining: {final_count}")
    
    clean_df.to_csv("clean_train.csv", index=False)
    print("\n[SUCCESS] Saved verified dataset as 'clean_train.csv'")

if __name__ == "__main__":
    run_local_audit()