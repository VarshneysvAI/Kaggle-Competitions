import pandas as pd
import os

def execute_grand_merger():
    print("Initiating Grand Dataset Merger...")
    
    # 1. Verify all 4 files exist
    files_needed = ["clean_train.csv", "synthetic_math.csv", "numina_reasoning.csv", "synthetic_crypto.csv"]
    for f in files_needed:
        if not os.path.exists(f):
            print(f"[CRITICAL ERROR] Missing {f}. Cannot merge.")
            return

    # 2. Load Datasets
    print("Loading all 4 data pillars...")
    df_kaggle = pd.read_csv("clean_train.csv")
    df_kaggle['source'] = 'kaggle_clean'
    
    df_synth_math = pd.read_csv("synthetic_math.csv")
    df_numina = pd.read_csv("numina_reasoning.csv")
    df_synth_crypto = pd.read_csv("synthetic_crypto.csv")
    
    # 3. Standardize Columns 
    if 'Question' in df_kaggle.columns:
        df_kaggle = df_kaggle.rename(columns={'Question': 'prompt', 'Answer': 'answer'})
        
    df_kaggle = df_kaggle[['prompt', 'answer', 'source']]
    df_synth_math = df_synth_math[['prompt', 'answer', 'source']]
    df_numina = df_numina[['prompt', 'answer', 'source']]
    df_synth_crypto = df_synth_crypto[['prompt', 'answer', 'source']]
    
    # 4. The Fusion
    print("Fusing datasets...")
    master_df = pd.concat([df_kaggle, df_synth_math, df_numina, df_synth_crypto], ignore_index=True)
    
    # 5. The Shuffle (Seed 42)
    print("Shuffling context windows to prevent catastrophic forgetting...")
    master_df = master_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # 6. Export to JSONL format
    output_filename = "nemotron_master_training.jsonl"
    master_df.to_json(output_filename, orient="records", lines=True)
    
    print("\n==========================================")
    print("        MASTER PIPELINE COMPLETE          ")
    print("==========================================")
    print(f"Total High-Fidelity Training Rows: {len(master_df)}")
    print("\nDataset Breakdown:")
    print(master_df['source'].value_counts())
    print(f"\n[READY FOR KAGGLE] -> {output_filename} is ready for deployment.")

if __name__ == "__main__":
    execute_grand_merger()