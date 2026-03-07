def compute_health_score(df, anomalies_count, drift_alerts, burst_count):
    score = 100
    score -= anomalies_count * 5
    score -= len(drift_alerts) * 8
    score -= burst_count * 10
    total = df['amount'].sum()
    if total > 0:
        max_share = df.groupby('category')['amount'].sum().max() / total
        if max_share > 0.4:
            score -= 10
    if 'Income' in df['category'].values:
        score += 10
    return max(0, min(100, round(score)))
