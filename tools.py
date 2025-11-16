"""
Custom tools for data analysis and visualization in the BI Intelligence Agent System.
These tools provide capabilities for data ingestion, statistical analysis, and report generation.
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from config import Config
from observability import trace_execution, observability


class DataIngestionTool:
    """Tool for ingesting data from various file formats."""
    
    def __init__(self):
        """Initialize the data ingestion tool."""
        self.supported_formats = ['.csv', '.json', '.xlsx', '.xls']
        self.observability = observability
    
    @trace_execution
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from a file into a pandas DataFrame.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            DataFrame containing the loaded data
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix not in self.supported_formats:
            raise ValueError(
                f"Unsupported format {path.suffix}. "
                f"Supported formats: {self.supported_formats}"
            )
        
        # Load based on file extension
        if path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif path.suffix == '.json':
            df = pd.read_json(file_path)
        elif path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        
        observability.logger.info(
            "data_loaded",
            file_path=file_path,
            rows=len(df),
            columns=len(df.columns)
        )
        
        return df
    
    @trace_execution
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the dataset.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary containing summary statistics
        """
        # Convert missing values to dict with int conversion
        missing_values = {}
        for col, val in df.isnull().sum().items():
            missing_values[col] = int(val)
        
        summary = {
            "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": missing_values,
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
        
        return summary


class StatisticalAnalysisTool:
    """Tool for performing statistical analysis on datasets."""
    
    def __init__(self):
        """Initialize the statistical analysis tool."""
        self.observability = observability
    
    @trace_execution
    def calculate_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate correlation matrix for numeric columns.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with correlation matrix and strong correlations
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {"error": "No numeric columns found for correlation analysis"}
        
        corr_matrix = numeric_df.corr()
        
        # Find strong correlations (|r| > 0.7, excluding diagonal)
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_corr.append({
                        "variable_1": corr_matrix.columns[i],
                        "variable_2": corr_matrix.columns[j],
                        "correlation": float(corr_value)
                    })
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_corr
        }
    
    @trace_execution
    def detect_outliers(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Detect outliers in a numeric column using IQR method.
        
        Args:
            df: DataFrame containing the data
            column: Name of the column to analyze
            
        Returns:
            Dictionary with outlier information
        """
        if column not in df.columns:
            return {"error": f"Column '{column}' not found"}
        
        if not np.issubdtype(df[column].dtype, np.number):
            return {"error": f"Column '{column}' is not numeric"}
        
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        return {
            "column": column,
            "total_values": int(len(df)),
            "outlier_count": int(len(outliers)),
            "outlier_percentage": float(len(outliers) / len(df) * 100),
            "bounds": {
                "lower": float(lower_bound),
                "upper": float(upper_bound)
            },
            "quartiles": {
                "Q1": float(Q1),
                "Q2": float(df[column].median()),
                "Q3": float(Q3),
                "IQR": float(IQR)
            }
        }
    
    @trace_execution
    def trend_analysis(self, df: pd.DataFrame, date_column: str, value_column: str) -> Dict[str, Any]:
        """
        Perform trend analysis on time series data.
        
        Args:
            df: DataFrame containing the data
            date_column: Name of the date/time column
            value_column: Name of the value column to analyze
            
        Returns:
            Dictionary with trend analysis results
        """
        try:
            # Ensure date column is datetime
            df_copy = df.copy()
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            df_copy = df_copy.sort_values(date_column)
            
            # Calculate basic trend statistics
            values = df_copy[value_column].values
            x = np.arange(len(values))
            
            # Linear regression for trend
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Calculate moving averages
            ma_7 = df_copy[value_column].rolling(window=min(7, len(df_copy))).mean()
            ma_30 = df_copy[value_column].rolling(window=min(30, len(df_copy))).mean()
            
            trend_direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "flat"
            
            return {
                "trend_direction": trend_direction,
                "slope": float(slope),
                "r_squared": float(r_value ** 2),
                "p_value": float(p_value),
                "mean": float(df_copy[value_column].mean()),
                "std": float(df_copy[value_column].std()),
                "min": float(df_copy[value_column].min()),
                "max": float(df_copy[value_column].max()),
                "growth_rate": float((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else None
            }
        except Exception as e:
            return {"error": str(e)}


class VisualizationTool:
    """Tool for creating data visualizations."""
    
    def __init__(self):
        """Initialize the visualization tool."""
        self.observability = observability
        Config.OUTPUT_DIR.mkdir(exist_ok=True)
    
    @trace_execution
    def create_correlation_heatmap(self, df: pd.DataFrame, output_path: Optional[str] = None) -> str:
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            df: DataFrame to visualize
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            raise ValueError("No numeric columns found for correlation heatmap")
        
        # Create correlation matrix
        corr = numeric_df.corr()
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, 
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save figure
        if output_path is None:
            output_path = Config.OUTPUT_DIR / f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        else:
            output_path = Path(output_path)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    @trace_execution
    def create_distribution_plot(self, df: pd.DataFrame, column: str, output_path: Optional[str] = None) -> str:
        """
        Create a distribution plot for a numeric column.
        
        Args:
            df: DataFrame containing the data
            column: Column name to visualize
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram with KDE
        axes[0].hist(df[column].dropna(), bins=30, edgecolor='black', alpha=0.7)
        axes[0].set_xlabel(column, fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)
        axes[0].set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
        axes[0].grid(alpha=0.3)
        
        # Box plot
        axes[1].boxplot(df[column].dropna())
        axes[1].set_ylabel(column, fontsize=12)
        axes[1].set_title(f'Box Plot of {column}', fontsize=14, fontweight='bold')
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        
        # Save figure
        if output_path is None:
            output_path = Config.OUTPUT_DIR / f"distribution_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        else:
            output_path = Path(output_path)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    @trace_execution
    def create_time_series_plot(self, df: pd.DataFrame, date_column: str, 
                                value_column: str, output_path: Optional[str] = None) -> str:
        """
        Create a time series visualization.
        
        Args:
            df: DataFrame containing the data
            date_column: Name of the date column
            value_column: Name of the value column
            output_path: Path to save the visualization
            
        Returns:
            Path to the saved visualization
        """
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        df_copy = df_copy.sort_values(date_column)
        
        plt.figure(figsize=(14, 7))
        plt.plot(df_copy[date_column], df_copy[value_column], linewidth=2, marker='o', markersize=4)
        plt.xlabel(date_column, fontsize=12)
        plt.ylabel(value_column, fontsize=12)
        plt.title(f'{value_column} Over Time', fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save figure
        if output_path is None:
            output_path = Config.OUTPUT_DIR / f"timeseries_{value_column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        else:
            output_path = Path(output_path)
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)


class ReportGenerationTool:
    """Tool for generating comprehensive analysis reports."""
    
    def __init__(self):
        """Initialize the report generation tool."""
        self.observability = observability
        Config.REPORTS_DIR.mkdir(exist_ok=True)
    
    @trace_execution
    def generate_html_report(self, 
                            data_summary: Dict[str, Any],
                            analysis_results: Dict[str, Any],
                            visualizations: List[str],
                            insights: List[str],
                            output_path: Optional[str] = None) -> str:
        """
        Generate an HTML report with analysis results.
        
        Args:
            data_summary: Dictionary containing data summary
            analysis_results: Dictionary containing analysis results
            visualizations: List of paths to visualization images
            insights: List of key insights
            output_path: Path to save the report
            
        Returns:
            Path to the saved report
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Business Intelligence Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                }}
                .section {{
                    background: white;
                    padding: 25px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .section h2 {{
                    color: #667eea;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }}
                .insight {{
                    background: #f0f4ff;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #667eea;
                    border-radius: 4px;
                }}
                .metric {{
                    display: inline-block;
                    background: #e8f4f8;
                    padding: 10px 20px;
                    margin: 5px;
                    border-radius: 5px;
                }}
                .visualization {{
                    max-width: 100%;
                    height: auto;
                    margin: 15px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #667eea;
                    color: white;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Business Intelligence Analysis Report</h1>
                <p>Generated: {timestamp}</p>
            </div>
            
            <div class="section">
                <h2>📈 Data Summary</h2>
                <div class="metric"><strong>Rows:</strong> {data_summary.get('shape', {}).get('rows', 'N/A')}</div>
                <div class="metric"><strong>Columns:</strong> {data_summary.get('shape', {}).get('columns', 'N/A')}</div>
                <div class="metric"><strong>Memory:</strong> {data_summary.get('memory_usage', 'N/A')}</div>
            </div>
            
            <div class="section">
                <h2>💡 Key Insights</h2>
                {"".join([f'<div class="insight">• {insight}</div>' for insight in insights])}
            </div>
            
            <div class="section">
                <h2>📊 Visualizations</h2>
                {"".join([f'<img src="{viz}" class="visualization" alt="Visualization">' for viz in visualizations])}
            </div>
            
            <div class="section">
                <h2>🔍 Detailed Analysis</h2>
                <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto;">
{json.dumps(analysis_results, indent=2)}
                </pre>
            </div>
            
            <div class="footer">
                <p>Generated by BI Intelligence Agent System | Powered by Google Gemini</p>
            </div>
        </body>
        </html>
        """
        
        # Save report
        if output_path is None:
            output_path = Config.REPORTS_DIR / f"bi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        else:
            output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)

