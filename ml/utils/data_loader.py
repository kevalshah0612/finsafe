import pandas as pd
from datasets import load_dataset


def load_training_data():
    print("Loading real transaction data from Hugging Face...")
    try:
        dataset = load_dataset(
            "mitulshah/transaction-categorization",
            split="train[:5000]",
            trust_remote_code=True
        )
        df = dataset.to_pandas()
        print(f"Columns found: {list(df.columns)}")
        df.columns = df.columns.str.strip().str.lower()

        desc_col = next((c for c in df.columns if 'desc' in c or 'transaction' in c or 'name' in c), None)
        cat_col  = next((c for c in df.columns if 'cat' in c or 'label' in c or 'type' in c), None)

        if not desc_col or not cat_col:
            raise ValueError(f"Could not detect columns. Available: {list(df.columns)}")

        df = df.rename(columns={desc_col: 'description', cat_col: 'category'})
        df = df[['description', 'category']].dropna()
        df['description'] = df['description'].astype(str).str.lower().str.strip()

        print(f"Loaded {len(df)} real transactions across {df['category'].nunique()} categories")
        print(f"Categories: {list(df['category'].unique())}")
        return df

    except Exception as e:
        print(f"Hugging Face load failed: {e}")
        print("Falling back to built-in training data...")
        return _fallback()


def _fallback():
    templates = {
        "Food":          ["mcdonalds","starbucks","uber eats","dominos","chipotle",
                          "grubhub","doordash","subway","burger king","pizza hut"],
        "Transport":     ["uber","lyft","shell gas","delta airlines","amtrak",
                          "parking","bp fuel","enterprise car","toll payment","metro card"],
        "Subscriptions": ["netflix","spotify","amazon prime","apple icloud","hulu",
                          "disney plus","adobe creative","microsoft 365","youtube premium","hbo max"],
        "Shopping":      ["walmart","target","amazon purchase","ebay","best buy",
                          "costco","home depot","zara","ikea","etsy"],
        "Healthcare":    ["cvs pharmacy","walgreens","hospital bill","urgent care",
                          "dental clinic","gym membership","planet fitness","health insurance"],
        "Housing":       ["rent payment","mortgage","electric bill","gas utility",
                          "water utility","internet service","comcast","verizon"],
        "Transfer":      ["venmo","zelle payment","paypal","cashapp",
                          "bank transfer","atm withdrawal","wire transfer","western union"],
        "Income":        ["paycheck deposit","freelance payment","tax refund",
                          "salary deposit","bonus payment","dividend","cashback reward"]
    }
    rows = []
    for cat, keywords in templates.items():
        for kw in keywords:
            for variant in [kw, f"{kw} purchase", f"online {kw}", f"{kw} - debit", f"pmt {kw}"]:
                rows.append({"description": variant, "category": cat})
    df = pd.DataFrame(rows)
    print(f"Fallback loaded: {len(df)} rows across {df['category'].nunique()} categories")
    return df
