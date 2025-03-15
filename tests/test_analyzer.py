import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add parent directory to path to import data_quality_analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_quality_analyzer import DataQualityAnalyzer

class TestDataQualityAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a sample dataset for testing."""
        np.random.seed(42)
        n_rows = 100
        
        # Create sample data
        cls.data = pd.DataFrame({
            'id': range(n_rows),
            'value': np.random.normal(0, 1, n_rows),
            'category': np.random.choice(['A', 'B', 'C', None], n_rows),
            'constant': 1
        })
        
        # Save original data for duplicate testing
        cls.original_data = cls.data.copy()
        
        # Add some missing values
        cls.data.loc[0:4, 'value'] = np.nan
        
        # Save to CSV for missing values and outliers tests
        cls.data.to_csv('test_data.csv', index=False)
        
        # Initialize analyzer
        cls.analyzer = DataQualityAnalyzer('test_data.csv')

    def test_missing_values(self):
        """Test missing values analysis."""
        # Run analysis
        with pd.ExcelWriter('test_report.xlsx', engine='openpyxl') as writer:
            self.analyzer._missing_values_analysis(writer)
        
        # Read results with index_col=0 to properly set the index
        missing_df = pd.read_excel('test_report.xlsx', sheet_name='Missing Values', index_col=0)
        
        # Check results
        self.assertEqual(missing_df.loc['value', 'Missing Count'], 5)
        self.assertEqual(missing_df.loc['category', 'Missing Count'], 
                        len(self.data[self.data['category'].isna()]))

    def test_duplicates(self):
        """Test duplicates analysis."""
        # Create data with duplicates
        data_with_duplicates = pd.concat([self.original_data, self.original_data.iloc[0:5]], ignore_index=True)
        data_with_duplicates.to_csv('test_data.csv', index=False)
        
        # Create new analyzer instance with duplicated data
        analyzer = DataQualityAnalyzer('test_data.csv')
        
        # Run analysis
        with pd.ExcelWriter('test_report.xlsx', engine='openpyxl') as writer:
            analyzer._duplicates_analysis(writer)
        
        # Read results
        duplicates_df = pd.read_excel('test_report.xlsx', sheet_name='Duplicates')
        
        # Check results
        self.assertEqual(duplicates_df['Total Duplicates'].iloc[0], 5)

    def test_outliers(self):
        """Test outlier detection."""
        # Add some outliers to the data
        self.data.loc[0, 'value'] = 100  # Clear outlier
        self.data.to_csv('test_data.csv', index=False)
        
        # Create new analyzer instance with outlier data
        analyzer = DataQualityAnalyzer('test_data.csv')
        
        # Run analysis
        with pd.ExcelWriter('test_report.xlsx', engine='openpyxl') as writer:
            analyzer._outliers_analysis(writer)
        
        # Read results with index_col=0 to properly set the index
        outliers_df = pd.read_excel('test_report.xlsx', sheet_name='Outliers', index_col=0)
        
        # Check results
        self.assertGreater(outliers_df.loc['value', 'Outliers Count'], 0)

    @classmethod
    def tearDownClass(cls):
        """Clean up test files."""
        files_to_remove = ['test_data.csv', 'test_report.xlsx']
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()
