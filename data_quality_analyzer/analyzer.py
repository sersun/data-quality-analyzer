"""
Core functionality for the Data Quality Analyzer.
Provides comprehensive analysis of data quality issues in ML datasets.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Optional, Union
import warnings
warnings.filterwarnings('ignore')

class DataQualityAnalyzer:
    def __init__(self, file_path: Union[str, Path]):
        """Initialize the analyzer with a CSV file path."""
        self.df: pd.DataFrame = pd.read_csv(file_path)
        self.output_dir: Path = Path('quality_report_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
        self.output_dir.mkdir(exist_ok=True)
        
    def analyze(self) -> None:
        """Run all analyses and generate reports."""
        print("Starting data quality analysis...")
        
        # Create Excel writer with engine specification
        with pd.ExcelWriter(
            self.output_dir / 'data_quality_report.xlsx',
            engine='openpyxl'
        ) as writer:
            # Ensure at least one sheet is written
            self._basic_info(writer)
            self._missing_values_analysis(writer)
            self._duplicates_analysis(writer)
            self._data_distribution(writer)
            self._outliers_analysis(writer)
            self._correlation_analysis(writer)
            
        self._generate_visualizations()
        print(f"\nAnalysis complete! Reports saved in: {self.output_dir}")

    def _basic_info(self, writer: pd.ExcelWriter) -> None:
        """Generate basic dataset information."""
        try:
            # Data types and memory usage
            dtypes_info = []
            for col in self.df.columns:
                dtypes_info.append({
                    'Column': col,
                    'Data Type': str(self.df[col].dtype),
                    'Memory Usage (MB)': self.df[col].memory_usage(deep=True) / 1024 / 1024,
                    'Unique Values': self.df[col].nunique()
                })
            dtypes_df = pd.DataFrame(dtypes_info)
            
            # Basic statistics
            stats_df = self.df.describe(include='all').T
            
            dtypes_df.to_excel(writer, sheet_name='Data Types', index=False)
            stats_df.to_excel(writer, sheet_name='Basic Statistics', index=True)
            print("Basic info analysis completed")
        except Exception as e:
            print(f"Warning: Error in basic info analysis: {str(e)}")

    def _missing_values_analysis(self, writer: pd.ExcelWriter) -> None:
        """Analyze missing values."""
        try:
            missing = pd.DataFrame({
                'Missing Count': self.df.isnull().sum(),
                'Missing Percentage': (self.df.isnull().sum() / len(self.df) * 100).round(2)
            })
            missing.to_excel(writer, sheet_name='Missing Values', index=True)
            print("Missing values analysis completed")
        except Exception as e:
            print(f"Warning: Error in missing values analysis: {str(e)}")

    def _duplicates_analysis(self, writer: pd.ExcelWriter) -> None:
        """Analyze duplicate records."""
        try:
            duplicates_info = pd.DataFrame({
                'Total Duplicates': [self.df.duplicated().sum()],
                'Duplicate Percentage': [(self.df.duplicated().sum() / len(self.df) * 100).round(2)],
                'Total Unique Records': [len(self.df.drop_duplicates())]
            })
            duplicates_info.to_excel(writer, sheet_name='Duplicates', index=False)
            print("Duplicates analysis completed")
        except Exception as e:
            print(f"Warning: Error in duplicates analysis: {str(e)}")

    def _data_distribution(self, writer: pd.ExcelWriter) -> None:
        """Analyze data distribution for numerical columns."""
        try:
            numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            if len(numerical_cols) > 0:
                distribution_stats = pd.DataFrame({
                    'Skewness': self.df[numerical_cols].skew(),
                    'Kurtosis': self.df[numerical_cols].kurtosis(),
                    'Mean': self.df[numerical_cols].mean(),
                    'Median': self.df[numerical_cols].median(),
                    'Std': self.df[numerical_cols].std()
                })
                distribution_stats.to_excel(writer, sheet_name='Distribution Stats', index=True)
            print("Distribution analysis completed")
        except Exception as e:
            print(f"Warning: Error in distribution analysis: {str(e)}")

    def _outliers_analysis(self, writer: pd.ExcelWriter) -> None:
        """Detect outliers using IQR method."""
        try:
            numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            outliers_stats: Dict[str, Dict[str, float]] = {}
            
            for col in numerical_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
                outliers_stats[col] = {
                    'Outliers Count': float(outliers),
                    'Outliers Percentage': float((outliers / len(self.df) * 100).round(2))
                }
                
            outliers_df = pd.DataFrame.from_dict(outliers_stats, orient='index')
            outliers_df.to_excel(writer, sheet_name='Outliers', index=True)
            print("Outliers analysis completed")
        except Exception as e:
            print(f"Warning: Error in outliers analysis: {str(e)}")

    def _correlation_analysis(self, writer: pd.ExcelWriter) -> None:
        """Generate correlation matrix for numerical columns."""
        try:
            numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            if len(numerical_cols) > 0:
                corr_matrix = self.df[numerical_cols].corr()
                corr_matrix.to_excel(writer, sheet_name='Correlations', index=True)
            print("Correlation analysis completed")
        except Exception as e:
            print(f"Warning: Error in correlation analysis: {str(e)}")

    def _generate_visualizations(self) -> None:
        """Generate various plots."""
        try:
            plots_dir = self.output_dir / 'plots'
            plots_dir.mkdir(exist_ok=True)
            
            # Set default style parameters for better readability
            plt.rcParams.update({
                'figure.figsize': [10, 6],
                'axes.grid': True,
                'grid.alpha': 0.3,
                'axes.labelsize': 12,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10
            })
            
            # Missing values plot
            self._create_missing_values_plot(plots_dir)
            
            # Distribution and box plots for numerical columns
            self._create_numerical_plots(plots_dir)
            
            # Correlation heatmap
            self._create_correlation_heatmap(plots_dir)
            
            print("Visualizations generated")
        except Exception as e:
            print(f"Warning: Error in visualization generation: {str(e)}")

    def _create_missing_values_plot(self, plots_dir: Path) -> None:
        """Create missing values visualization."""
        plt.figure(figsize=(12, 6))
        missing_data = self.df.isnull().sum()
        sns.barplot(x=missing_data.index, y=missing_data.values)
        plt.xticks(rotation=45, ha='right')
        plt.title('Missing Values by Column')
        plt.tight_layout()
        plt.savefig(plots_dir / 'missing_values.png')
        plt.close()

    def _create_numerical_plots(self, plots_dir: Path) -> None:
        """Create distribution and box plots for numerical columns."""
        numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        for col in numerical_cols:
            # Distribution plot
            plt.figure(figsize=(10, 6))
            sns.histplot(data=self.df, x=col, kde=True)
            plt.title(f'Distribution of {col}')
            plt.tight_layout()
            plt.savefig(plots_dir / f'distribution_{col}.png')
            plt.close()

            # Box plot
            plt.figure(figsize=(8, 6))
            sns.boxplot(y=self.df[col])
            plt.title(f'Box Plot of {col}')
            plt.tight_layout()
            plt.savefig(plots_dir / f'boxplot_{col}.png')
            plt.close()

    def _create_correlation_heatmap(self, plots_dir: Path) -> None:
        """Create correlation heatmap for numerical columns."""
        numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        if len(numerical_cols) > 0:
            plt.figure(figsize=(12, 8))
            corr_matrix = self.df[numerical_cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plt.savefig(plots_dir / 'correlation_heatmap.png')
            plt.close()

def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python -m data_quality_analyzer <path_to_csv>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    analyzer = DataQualityAnalyzer(file_path)
    analyzer.analyze()

if __name__ == "__main__":
    main()
