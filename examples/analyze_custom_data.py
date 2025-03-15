"""
Example script demonstrating how to use the Data Quality Analyzer with custom data.
This example shows how to:
1. Generate a custom dataset
2. Run the analysis
3. Access and interpret the results
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add parent directory to path to import data_quality_analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_quality_analyzer import DataQualityAnalyzer

def create_custom_dataset():
    """Create a custom dataset with various data quality issues."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Number of samples
    n_samples = 1000
    
    # Generate features
    data = {
        # Numerical features with different distributions
        'normal_dist': np.random.normal(100, 15, n_samples),
        'uniform_dist': np.random.uniform(0, 100, n_samples),
        'exponential_dist': np.random.exponential(10, n_samples),
        
        # Categorical features
        'category_balanced': np.random.choice(['A', 'B', 'C'], n_samples, p=[0.33, 0.33, 0.34]),
        'category_imbalanced': np.random.choice(['X', 'Y', 'Z'], n_samples, p=[0.8, 0.15, 0.05]),
        
        # DateTime feature
        'dates': pd.date_range(start='2024-01-01', periods=n_samples).values,
        
        # Target variable (binary classification)
        'target': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Introduce data quality issues
    
    # 1. Missing values
    for col in ['normal_dist', 'category_balanced']:
        mask = np.random.choice([True, False], n_samples, p=[0.1, 0.9])
        df.loc[mask, col] = np.nan
    
    # 2. Outliers
    df.loc[np.random.choice(n_samples, 10), 'normal_dist'] = 1000
    df.loc[np.random.choice(n_samples, 5), 'uniform_dist'] = 999
    
    # 3. Duplicates
    duplicate_indices = np.random.choice(n_samples, 50)
    df = pd.concat([df, df.iloc[duplicate_indices]], ignore_index=True)
    
    return df

def main():
    """Main function demonstrating the usage of Data Quality Analyzer."""
    # Create and save custom dataset
    print("Creating custom dataset...")
    df = create_custom_dataset()
    data_file = 'custom_data.csv'
    df.to_csv(data_file, index=False)
    print(f"Dataset saved to {data_file}")
    
    # Initialize and run analyzer
    print("\nRunning data quality analysis...")
    analyzer = DataQualityAnalyzer(data_file)
    analyzer.analyze()
    
    # Get the output directory
    output_dir = sorted(Path('.').glob('quality_report_*'))[-1]
    print(f"\nAnalysis complete! Reports saved in: {output_dir}")
    
    print("\nSummary of findings:")
    print("1. Check 'Data Types' sheet for feature information")
    print("2. Review 'Missing Values' sheet for data completeness")
    print("3. Examine 'Outliers' sheet for extreme values")
    print("4. Look at 'Correlations' sheet for feature relationships")
    print("5. View distribution plots in the 'plots' directory")

if __name__ == "__main__":
    main()
