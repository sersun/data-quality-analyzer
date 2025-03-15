import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_sample_data(n_rows: int = 1000) -> pd.DataFrame:
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate sample data
    data: Dict[str, Any] = {
        'customer_id': list(range(1, n_rows + 1)),
        'age': np.random.normal(35, 12, n_rows),
        'income': np.random.lognormal(10, 1, n_rows),
        'credit_score': np.random.normal(700, 100, n_rows),
        'account_balance': np.random.exponential(5000, n_rows),
        'num_transactions': np.random.poisson(30, n_rows),
        'years_customer': np.random.uniform(0, 20, n_rows)
    }

    # Add categorical features
    data['customer_type'] = np.random.choice(
        ['Regular', 'Premium', 'VIP', None], 
        n_rows, 
        p=[0.6, 0.3, 0.05, 0.05]
    )
    data['country'] = np.random.choice(
        ['USA', 'UK', 'Canada', 'Australia', None], 
        n_rows, 
        p=[0.4, 0.3, 0.2, 0.05, 0.05]
    )

    # Add dates
    base_date = datetime(2024, 1, 1)
    data['last_purchase'] = [
        base_date + timedelta(days=np.random.randint(-365, 0)) 
        for _ in range(n_rows)
    ]

    # Create DataFrame
    df = pd.DataFrame(data)

    # Introduce data quality issues
    # 1. Add missing values
    for col in ['age', 'income', 'credit_score', 'account_balance']:
        mask = np.random.choice([True, False], n_rows, p=[0.05, 0.95])
        df.loc[mask, col] = np.nan

    # 2. Add outliers
    df.loc[np.random.choice(n_rows, 10), 'income'] *= 100
    df.loc[np.random.choice(n_rows, 5), 'age'] += 100

    # 3. Add duplicates
    duplicate_indices = np.random.choice(n_rows, 20)
    df = pd.concat([df, df.iloc[duplicate_indices]], ignore_index=True)

    # 4. Add invalid values
    df.loc[np.random.choice(n_rows, 5), 'age'] = -1
    df.loc[np.random.choice(n_rows, 5), 'credit_score'] = -999

    return df

if __name__ == "__main__":
    df = generate_sample_data()
    df.to_csv('sample_customer_data.csv', index=False)
    print("Sample dataset created: sample_customer_data.csv")
