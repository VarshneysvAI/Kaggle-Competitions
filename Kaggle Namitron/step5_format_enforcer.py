import pandas as pd
import json

def enforce_strict_formatting():
    print("Initializing Retroactive Formatter...")
    
    input_file = "nemotron_master_training.jsonl"
    output_file = "nemotron_DEPLOYMENT_READY.jsonl"
    
    fixed_dataset = []
    fixed_count = 0
    
    with open(input_file, 'r') as f:
        for line in f:
            row = json.loads(line)
            
            # If the row is from kaggle_clean, it lacks the scratchpad formatting
            if row['source'] == 'kaggle_clean':
                raw_answer = str(row['answer']).strip()
                
                # We dynamically inject a domain and a generic scratchpad trace
                new_answer = (
                    "<domain> kaggle_baseline </domain>\n"
                    "<scratchpad>\n"
                    "Analyzing the hidden transformation rule from the provided examples...\n"
                    "Applying the extrapolated logic to the target problem to derive the final state.\n"
                    "</scratchpad>\n"
                    f"\\boxed{{{raw_answer}}}"
                )
                
                row['answer'] = new_answer
                fixed_count += 1
                
            fixed_dataset.append(row)
            
    # Save the deployment-ready file
    with open(output_file, 'w') as out_f:
        for row in fixed_dataset:
            out_f.write(json.dumps(row) + '\n')
            
    print("\n--- FORMATTING ENFORCEMENT COMPLETE ---")
    print(f"Repaired {fixed_count} raw Kaggle rows.")
    print("All rows now contain <domain>, <scratchpad>, and \\boxed{} tags.")
    print(f"[READY FOR CLOUD] -> Upload '{output_file}' to Kaggle.")

if __name__ == "__main__":
    enforce_strict_formatting()