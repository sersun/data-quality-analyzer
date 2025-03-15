# Data Quality Analyzer for ML Projects
![data-quality-analyzer_img](https://github.com/user-attachments/assets/a7df0334-2081-439e-bb2c-a152f0e71c69)


A comprehensive Python tool for analyzing data quality in datasets intended for machine learning projects. This tool generates detailed reports about various aspects of data quality, helping data scientists and ML engineers identify potential issues before model development.

## Features

### 1. Data Overview
- Basic dataset information
- Memory usage analysis
- Data types summary
- Unique values count

### 2. Missing Values Analysis
- Count and percentage of missing values per column
- Visual representation of missing data distribution
- Identification of columns with high missing rates

### 3. Duplicate Records Detection
- Total number of duplicate records
- Percentage of duplicates in the dataset
- Count of unique records

### 4. Distribution Analysis
- Statistical measures (mean, median, std)
- Skewness and kurtosis calculations
- Distribution visualizations for numerical columns
- Box plots for outlier detection

### 5. Outlier Detection
- IQR (Interquartile Range) method
- Count and percentage of outliers per column
- Visual representation through box plots

### 6. Correlation Analysis
- Correlation matrix for numerical columns
- Heatmap visualization
- Identification of highly correlated features

## Installation

### Method 1: Install from Source
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install in development mode:
```bash
pip install -e .
```

### Method 2: Install from PyPI (coming soon)
```bash
pip install data-quality-analyzer
```

## Usage

### Command Line Usage
After installation, you can use the tool in two ways:

1. As a command-line tool:
```bash
data-quality-analyzer path_to_your_data.csv
```

2. As a Python module:
```bash
python -m data_quality_analyzer path_to_your_data.csv
```

### Python API Usage
You can also use the tool programmatically in your Python code:

```python
from data_quality_analyzer import DataQualityAnalyzer

# Initialize analyzer with your data
analyzer = DataQualityAnalyzer('path_to_your_data.csv')

# Run analysis
analyzer.analyze()
```

### Example Usage
The project includes example scripts in the `examples/` directory:

1. Basic example with custom data:
```bash
python examples/analyze_custom_data.py
```
This example demonstrates:
- Creating a custom dataset with various distributions
- Introducing common data quality issues
- Running the analysis
- Interpreting the results

### Sample Data Generation
For testing purposes, use:
```bash
python generate_sample_data.py
```
This creates `sample_customer_data.csv` with various data quality issues.

### Output Structure
The tool generates a new directory named `quality_report_YYYYMMDD_HHMMSS` containing:

1. Excel Report (`data_quality_report.xlsx`) with sheets:
   - Data Types
   - Basic Statistics
   - Missing Values
   - Duplicates
   - Distribution Stats
   - Outliers
   - Correlations

2. Visualizations (in `plots/` directory):
   - `missing_values.png`: Bar chart of missing values
   - `distribution_{column}.png`: Distribution plots for each numerical column
   - `boxplot_{column}.png`: Box plots for outlier detection
   - `correlation_heatmap.png`: Correlation matrix heatmap

## Technical Details

### Requirements
- Python 3.9+
- Dependencies:
  - pandas ~= 1.5.3
  - numpy ~= 1.24.3
  - matplotlib ~= 3.7.1
  - seaborn ~= 0.12.2
  - scikit-learn ~= 1.0.2
  - openpyxl ~= 3.1.2

### Data Limitations
- Designed for datasets with up to 30 columns
- Handles both numerical and categorical data
- Supports CSV file format

## Analysis Methods

### Missing Values
- Calculates both count and percentage of missing values
- Provides visual representation for easy identification
- Helps in deciding imputation strategies

### Outlier Detection
Uses the IQR method:
1. Calculates Q1 (25th percentile) and Q3 (75th percentile)
2. Computes IQR = Q3 - Q1
3. Identifies outliers as values outside: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]

### Distribution Analysis
- Generates histograms with KDE for numerical columns
- Calculates skewness and kurtosis
- Provides box plots for visual distribution analysis

### Correlation Analysis
- Generates correlation matrix for numerical columns
- Visualizes correlations through heatmap
- Helps identify potential feature interactions

## Testing

The project includes a comprehensive test suite in the `tests/` directory:

```bash
python -m unittest discover tests
```

The tests cover:
- Missing values detection
- Duplicate records analysis
- Outlier identification
- Basic functionality and edge cases

## Best Practices

1. Data Preparation:
   - Ensure CSV file is properly formatted
   - Check for encoding issues
   - Verify column names are unique

2. Resource Management:
   - For large datasets, ensure sufficient memory
   - Consider running analysis on a sample first

3. Report Interpretation:
   - Review all sheets in the Excel report
   - Pay special attention to outliers and missing values
   - Consider correlations when feature engineering

## Error Handling

The tool includes comprehensive error handling:
- Graceful handling of missing or invalid files
- Informative error messages
- Continued execution even if one analysis fails

## Project Structure

```
data-quality-analyzer/
├── data_quality_analyzer/    # Main package directory
│   ├── __init__.py          # Package initialization
│   └── analyzer.py          # Core functionality
├── examples/                # Example usage scripts
│   ├── __init__.py
│   └── analyze_custom_data.py
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_analyzer.py
├── setup.py                # Package setup file
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
└── .gitignore            # Git ignore rules
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
