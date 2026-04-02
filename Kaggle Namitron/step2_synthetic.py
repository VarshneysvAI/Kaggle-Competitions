import pandas as pd

def int_to_bin8(n): return format(n & 0xFF, '08b')

def generate_deterministic_math():
    print("Manufacturing Deterministic Math Traps...")
    dataset = []
    edge_cases = [0, 255, 170, 85, 15, 240, 128, 1] # The exact numbers that break models
    
    for key in range(1, 256):
        examples_text = "\n".join([f"{int_to_bin8(v)} -> {int_to_bin8(v ^ key)}" for v in edge_cases])
        target_val = (key + 42) % 256 if (key + 42) % 256 not in edge_cases else (key + 43) % 256
        correct_ans = target_val ^ key
        
        prompt = (
            "In Alice's Wonderland, a secret bit manipulation rule transforms 8-bit binary numbers. "
            "Here are some examples of input -> output:\n"
            f"{examples_text}\n"
            f"Now, determine the output for: {int_to_bin8(target_val)}"
        )
        
        # We enforce the <scratchpad> routing logic
        answer = (
            "<domain> bitwise_math </domain>\n"
            "<scratchpad>\n"
            "Testing XOR with constant. "
            f"{edge_cases[0]} ^ {edge_cases[0] ^ key} = {key}. "
            f"Target {target_val} ^ {key} = {correct_ans}.\n"
            "</scratchpad>\n"
            f"\\boxed{{{int_to_bin8(correct_ans)}}}"
        )
        dataset.append({"prompt": prompt, "answer": answer, "source": "synthetic_trap"})

    df = pd.DataFrame(dataset)
    df.to_csv("synthetic_math.csv", index=False)
    print(f"[SUCCESS] Created {len(df)} perfect synthetic traps.")

if __name__ == "__main__":
    generate_deterministic_math()