"""
Multi-agent system for Business Intelligence Analysis.
Implements coordinator, data analyst, and report generator agents using Google Gemini.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime
import pandas as pd

from google import genai
from google.genai import types

from config import Config
from tools import (
    DataIngestionTool, 
    StatisticalAnalysisTool, 
    VisualizationTool,
    ReportGenerationTool
)
from memory import MemoryBank, InMemorySessionService, AnalysisSession
from observability import observability


class BIAgent:
    """Base class for Business Intelligence agents."""
    
    def __init__(self, name: str, role: str, model_name: str = None):
        """
        Initialize a BI agent.
        
        Args:
            name: Agent name
            role: Agent role description
            model_name: Gemini model to use
        """
        self.name = name
        self.role = role
        self.model_name = model_name or Config.DEFAULT_MODEL
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=Config.GOOGLE_API_KEY)
        
        # Observability
        self.observability = observability
    
    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a response using Gemini.
        
        Args:
            prompt: User prompt
            context: Additional context for the prompt
            
        Returns:
            Generated response text
        """
        # Log agent call
        self.observability.log_agent_call(
            agent_name=self.name,
            task=prompt[:100],
            model=self.model_name
        )
        
        # Build system instruction
        system_instruction = f"""You are {self.name}, a specialized AI agent for business intelligence.
Your role: {self.role}

You provide clear, actionable insights based on data analysis. Be specific, use numbers, 
and explain your reasoning. When analyzing data, consider:
- Trends and patterns
- Outliers and anomalies
- Correlations and relationships
- Business implications

{f'Context: {context}' if context else ''}
"""
        
        try:
            # Generate response
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=Config.TEMPERATURE,
                )
            )
            
            return response.text
        
        except Exception as e:
            self.observability.log_error(
                error_type="generation_error",
                message=str(e),
                agent=self.name
            )
            return f"Error generating response: {str(e)}"


class DataAnalystAgent(BIAgent):
    """
    Agent specialized in data analysis and statistical insights.
    Performs deep analysis of datasets and identifies patterns.
    """
    
    def __init__(self):
        """Initialize the Data Analyst agent."""
        super().__init__(
            name="Data Analyst Agent",
            role="Expert in statistical analysis, pattern recognition, and data quality assessment"
        )
        self.stats_tool = StatisticalAnalysisTool()
    
    def analyze_dataset(self, df: pd.DataFrame, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a dataset.
        
        Args:
            df: DataFrame to analyze
            data_summary: Summary of the dataset
            
        Returns:
            Dictionary containing analysis results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "correlation_analysis": {},
            "outlier_analysis": {},
            "ai_insights": ""
        }
        
        # Perform correlation analysis
        results["correlation_analysis"] = self.stats_tool.calculate_correlations(df)
        
        # Detect outliers in numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        outliers_found = []
        for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
            outlier_info = self.stats_tool.detect_outliers(df, col)
            if outlier_info.get("outlier_percentage", 0) > 5:  # Only report if > 5% outliers
                outliers_found.append(outlier_info)
        results["outlier_analysis"] = outliers_found
        
        # Generate AI insights
        analysis_prompt = f"""Analyze this dataset and provide key insights:

Dataset Summary:
- Rows: {data_summary['shape']['rows']}
- Columns: {data_summary['shape']['columns']}
- Column names: {', '.join(data_summary['columns'])}

Correlation Analysis:
Strong correlations found: {len(results['correlation_analysis'].get('strong_correlations', []))}
{results['correlation_analysis'].get('strong_correlations', [])}

Outliers Detected:
{outliers_found}

Provide 3-5 key insights about this data, including:
1. Overall data quality and completeness
2. Notable patterns or correlations
3. Potential data issues or anomalies
4. Recommendations for further analysis
"""
        
        results["ai_insights"] = self.generate_response(analysis_prompt)
        
        return results
    
    def analyze_time_series(self, df: pd.DataFrame, date_column: str, 
                           value_column: str) -> Dict[str, Any]:
        """
        Analyze time series data.
        
        Args:
            df: DataFrame with time series data
            date_column: Name of date column
            value_column: Name of value column
            
        Returns:
            Time series analysis results
        """
        trend_results = self.stats_tool.trend_analysis(df, date_column, value_column)
        
        # Generate AI insights on trends
        trend_prompt = f"""Analyze this time series trend:

Metric: {value_column}
Trend Direction: {trend_results.get('trend_direction', 'unknown')}
Growth Rate: {trend_results.get('growth_rate', 'N/A')}%
R-squared: {trend_results.get('r_squared', 'N/A')}

Statistics:
- Mean: {trend_results.get('mean', 'N/A')}
- Std Dev: {trend_results.get('std', 'N/A')}
- Min: {trend_results.get('min', 'N/A')}
- Max: {trend_results.get('max', 'N/A')}

Provide insights on:
1. Strength and reliability of the trend
2. Business implications
3. Potential forecasting considerations
"""
        
        trend_results["ai_insights"] = self.generate_response(trend_prompt)
        
        return trend_results


class VisualizationAgent(BIAgent):
    """
    Agent specialized in data visualization and visual insights.
    Creates meaningful visualizations and explains them.
    """
    
    def __init__(self):
        """Initialize the Visualization agent."""
        super().__init__(
            name="Visualization Agent",
            role="Expert in data visualization and visual storytelling"
        )
        self.viz_tool = VisualizationTool()
    
    def create_visualizations(self, df: pd.DataFrame, 
                            analysis_results: Dict[str, Any]) -> List[str]:
        """
        Create appropriate visualizations for the dataset.
        
        Args:
            df: DataFrame to visualize
            analysis_results: Results from data analysis
            
        Returns:
            List of paths to created visualizations
        """
        visualizations = []
        
        try:
            # Create correlation heatmap if we have numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 1:
                viz_path = self.viz_tool.create_correlation_heatmap(df)
                visualizations.append(viz_path)
                self.observability.logger.info("created_visualization", type="correlation_heatmap", path=viz_path)
            
            # Create distribution plots for key numeric columns
            for col in numeric_cols[:3]:  # First 3 numeric columns
                viz_path = self.viz_tool.create_distribution_plot(df, col)
                visualizations.append(viz_path)
                self.observability.logger.info("created_visualization", type="distribution", column=col, path=viz_path)
        
        except Exception as e:
            self.observability.log_error("visualization_error", str(e))
        
        return visualizations
    
    def create_time_series_viz(self, df: pd.DataFrame, date_column: str, 
                               value_column: str) -> Optional[str]:
        """
        Create time series visualization.
        
        Args:
            df: DataFrame with time series data
            date_column: Date column name
            value_column: Value column name
            
        Returns:
            Path to visualization or None
        """
        try:
            viz_path = self.viz_tool.create_time_series_plot(df, date_column, value_column)
            self.observability.logger.info("created_visualization", type="time_series", path=viz_path)
            return viz_path
        except Exception as e:
            self.observability.log_error("visualization_error", str(e))
            return None


class ReportGeneratorAgent(BIAgent):
    """
    Agent specialized in generating comprehensive analysis reports.
    Synthesizes findings from other agents into actionable reports.
    """
    
    def __init__(self):
        """Initialize the Report Generator agent."""
        super().__init__(
            name="Report Generator Agent",
            role="Expert in synthesizing analysis results into clear, actionable business reports"
        )
        self.report_tool = ReportGenerationTool()
    
    def generate_insights(self, data_summary: Dict[str, Any], 
                         analysis_results: Dict[str, Any],
                         session_context: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Generate key insights from analysis results.
        
        Args:
            data_summary: Dataset summary
            analysis_results: Analysis results
            session_context: Context from previous sessions
            
        Returns:
            List of key insights
        """
        insights_prompt = f"""Based on the following analysis, generate 5-7 key business insights 
that would be valuable to stakeholders:

Dataset: {data_summary['shape']['rows']} rows, {data_summary['shape']['columns']} columns

Analysis Summary:
{analysis_results.get('ai_insights', 'No AI insights available')}

{f"Previous Context: {session_context}" if session_context else ""}

Provide insights that are:
1. Actionable - suggest what to do
2. Specific - include numbers and details
3. Business-focused - explain the impact
4. Clear - easy to understand

Format each insight as a complete sentence starting with a bullet point."""
        
        response = self.generate_response(insights_prompt)
        
        # Parse insights from response
        insights = [line.strip().lstrip('•-*').strip() 
                   for line in response.split('\n') 
                   if line.strip() and not line.strip().startswith('#')]
        
        return insights[:7]  # Limit to 7 insights
    
    def generate_report(self, data_summary: Dict[str, Any],
                       analysis_results: Dict[str, Any],
                       visualizations: List[str],
                       insights: List[str]) -> str:
        """
        Generate a comprehensive HTML report.
        
        Args:
            data_summary: Dataset summary
            analysis_results: Analysis results
            visualizations: List of visualization paths
            insights: List of insights
            
        Returns:
            Path to generated report
        """
        report_path = self.report_tool.generate_html_report(
            data_summary=data_summary,
            analysis_results=analysis_results,
            visualizations=visualizations,
            insights=insights
        )
        
        self.observability.logger.info("report_generated", path=report_path)
        
        return report_path


class CoordinatorAgent(BIAgent):
    """
    Coordinator agent that orchestrates the multi-agent workflow.
    Manages parallel and sequential agent execution.
    """
    
    def __init__(self, memory_bank: MemoryBank):
        """
        Initialize the Coordinator agent.
        
        Args:
            memory_bank: Memory bank for session management
        """
        super().__init__(
            name="Coordinator Agent",
            role="Orchestrates the BI analysis workflow and coordinates specialist agents"
        )
        
        # Initialize specialist agents
        self.data_analyst = DataAnalystAgent()
        self.visualizer = VisualizationAgent()
        self.report_generator = ReportGeneratorAgent()
        
        # Initialize tools
        self.ingestion_tool = DataIngestionTool()
        
        # Session management
        self.memory_bank = memory_bank
        self.session_service = InMemorySessionService(memory_bank)
    
    def analyze_file(self, file_path: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Coordinate a comprehensive analysis of a data file.
        
        Args:
            file_path: Path to the data file
            analysis_type: Type of analysis to perform
            
        Returns:
            Dictionary with analysis results and report path
        """
        # Start new session
        session = self.session_service.start_session()
        
        try:
            # Step 1: Data Ingestion
            self.observability.logger.info("analysis_started", file=file_path, session=session.session_id)
            df = self.ingestion_tool.load_data(file_path)
            data_summary = self.ingestion_tool.get_data_summary(df)
            
            # Update session with dataset info
            session.dataset_info = {
                "file_path": file_path,
                "columns": data_summary["columns"],
                **data_summary["shape"]
            }
            
            # Get relevant context from memory
            context = self.memory_bank.get_relevant_context(data_summary["columns"])
            
            # Step 2: Parallel execution of analysis and visualization
            # (Simulated parallel execution - in production, use asyncio or threading)
            self.observability.logger.info("parallel_analysis_started", agents=["DataAnalyst", "Visualizer"])
            
            # Data analysis
            analysis_results = self.data_analyst.analyze_dataset(df, data_summary)
            self.memory_bank.add_analysis_result(session, "statistical_analysis", analysis_results)
            
            # Visualization (can run in parallel with analysis)
            visualizations = self.visualizer.create_visualizations(df, analysis_results)
            for viz in visualizations:
                self.memory_bank.add_visualization(session, viz)
            
            # Step 3: Sequential execution - generate insights and report
            # (Must wait for analysis and visualization to complete)
            self.observability.logger.info("sequential_report_generation_started")
            
            insights = self.report_generator.generate_insights(
                data_summary, 
                analysis_results,
                context
            )
            
            # Store insights in memory
            for insight in insights:
                self.memory_bank.add_insight(session, insight, is_global=True)
            
            # Generate final report
            report_path = self.report_generator.generate_report(
                data_summary=data_summary,
                analysis_results=analysis_results,
                visualizations=visualizations,
                insights=insights
            )
            
            # Persist session
            self.session_service.persist_session(session.session_id)
            
            # Log metrics
            self.observability.log_metrics_summary()
            
            return {
                "success": True,
                "session_id": session.session_id,
                "report_path": report_path,
                "visualizations": visualizations,
                "insights": insights,
                "data_summary": data_summary,
                "analysis_results": analysis_results
            }
        
        except Exception as e:
            self.observability.log_error("analysis_failed", str(e), session=session.session_id)
            return {
                "success": False,
                "error": str(e),
                "session_id": session.session_id
            }
    
    def analyze_time_series(self, file_path: str, date_column: str, 
                           value_column: str) -> Dict[str, Any]:
        """
        Coordinate time series analysis.
        
        Args:
            file_path: Path to the data file
            date_column: Name of date column
            value_column: Name of value column
            
        Returns:
            Analysis results
        """
        session = self.session_service.start_session()
        
        try:
            # Load data
            df = self.ingestion_tool.load_data(file_path)
            data_summary = self.ingestion_tool.get_data_summary(df)
            
            # Time series analysis
            trend_results = self.data_analyst.analyze_time_series(df, date_column, value_column)
            self.memory_bank.add_analysis_result(session, "time_series", trend_results)
            
            # Create visualization
            viz_path = self.visualizer.create_time_series_viz(df, date_column, value_column)
            if viz_path:
                self.memory_bank.add_visualization(session, viz_path)
            
            # Generate insights
            insights = self.report_generator.generate_insights(data_summary, trend_results)
            for insight in insights:
                self.memory_bank.add_insight(session, insight)
            
            # Generate report
            report_path = self.report_generator.generate_report(
                data_summary=data_summary,
                analysis_results=trend_results,
                visualizations=[viz_path] if viz_path else [],
                insights=insights
            )
            
            self.session_service.persist_session(session.session_id)
            
            return {
                "success": True,
                "session_id": session.session_id,
                "report_path": report_path,
                "trend_results": trend_results,
                "insights": insights
            }
        
        except Exception as e:
            self.observability.log_error("time_series_analysis_failed", str(e))
            return {
                "success": False,
                "error": str(e)
            }

