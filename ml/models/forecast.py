import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_spending(df):
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['week'] = df['date'].dt.isocalendar().week.astype(int)
        weekly     = df.groupby('week')['amount'].sum().reset_index()
        weekly.columns = ['week', 'total']

        if len(weekly) < 3:
            avg = weekly['total'].mean() if len(weekly) > 0 else 100
            return [{"week": f"Week +{i+1}", "forecast": round(avg, 2)} for i in range(4)]

        model = LinearRegression()
        model.fit(weekly['week'].values.reshape(-1, 1), weekly['total'].values)
        last_week = int(weekly['week'].max())

        return [
            {"week": f"Week +{i}", "forecast": round(max(model.predict([[last_week + i]])[0], 0), 2)}
            for i in range(1, 5)
        ]
    except Exception:
        return [{"week": f"Week +{i}", "forecast": 0.0} for i in range(1, 5)]
