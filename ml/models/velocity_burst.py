import pandas as pd


def detect_velocity_burst(df):
    df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('date_parsed').copy()

    df['rolling_3day'] = (
        df.set_index('date_parsed')['amount']
        .rolling('3D')
        .sum()
        .values
    )

    avg_3day = df['rolling_3day'].mean()
    std_3day = df['rolling_3day'].std() if df['rolling_3day'].std() > 0 else 1

    df['velocity_burst']     = df['rolling_3day'] > (avg_3day + 2 * std_3day)
    df['velocity_burst_msg'] = df.apply(
        lambda r: (
            f"Spent ${r['rolling_3day']:.0f} in 3 days - "
            f"{round(r['rolling_3day'] / avg_3day, 1)}x your normal 3-day window"
        ) if r['velocity_burst'] else '',
        axis=1
    )
    return df
