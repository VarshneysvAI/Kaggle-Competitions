import os
# Force the Hugging Face library to use the mirror endpoint to bypass DNS/ISP blocks
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import pandas as pd
from datasets import load_dataset

def fetch_reasoning_core():
    print("Connecting to Hugging Face Mirror... Bypassing network blocks.")
    try:
        # Download a highly curated math dataset
        dataset = load_dataset("AI-MO/NuminaMath-CoT", split="train")
        
        print("Dataset downloaded. Extracting 5,000 perfect reasoning traces...")
        # Shuffle and grab 5,000 rows
        dataset = dataset.shuffle(seed=42).select(range(5000))
        
        extracted_data = []
        for row in dataset:
            # Format it exactly how we want Nemotron to learn
            prompt = row['problem']
            # We inject the <domain> tag to train the model to route itself
            answer = (
                "<domain> general_reasoning </domain>\n"
                "<scratchpad>\n"
                f"{row['solution']}\n" 
                "</scratchpad>"
            )
            extracted_data.append({"prompt": prompt, "answer": answer, "source": "numina_core"})
            
        df = pd.DataFrame(extracted_data)
        df.to_csv("numina_reasoning.csv", index=False)
        print(f"\n[SUCCESS] Extracted {len(df)} general reasoning puzzles to numina_reasoning.csv.")
        
    except Exception as e:
        print(f"\n[CRITICAL ERROR] The mirror is also blocked by your network.")
        print(f"Error details: {e}")
        print("\nWe will need to use the manual offline bypass instead.")

if __name__ == "__main__":
    fetch_reasoning_core()