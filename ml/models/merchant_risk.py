def compute_merchant_risk(df):
    merchant_counts = df['description'].str.lower().str.strip().value_counts()

    def risk_label(desc):
        count = merchant_counts.get(desc.lower().strip(), 0)
        if count == 1:
            return "New Merchant"
        elif count <= 3:
            return "Infrequent"
        else:
            return "Familiar"

    df['merchant_risk'] = df['description'].apply(risk_label)
    df['fraud_signal']  = df.apply(
        lambda r: "High Risk - New Merchant and Unusual Amount"
        if r['merchant_risk'] == 'New Merchant' and r['anomaly']
        else (
            "Caution - New Merchant"
            if r['merchant_risk'] == 'New Merchant'
            else ""
        ),
        axis=1
    )
    return df
