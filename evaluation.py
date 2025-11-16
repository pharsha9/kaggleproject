"""
Evaluation module for assessing agent performance and system quality.
Provides metrics and scoring for continuous improvement.
"""

import time
import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

from config import Config
from observability import observability


class AgentEvaluator:
    """
    Evaluates agent performance across multiple dimensions.
    Provides quantitative metrics for system quality assessment.
    """
    
    def __init__(self):
        """Initialize the evaluator."""
        self.evaluation_history = []
        self.metrics_path = Config.BASE_DIR / "evaluation_metrics.json"
        self.load_history()
    
    def load_history(self) -> None:
        """Load evaluation history from disk."""
        if self.metrics_path.exists():
            with open(self.metrics_path, 'r') as f:
                self.evaluation_history = json.load(f)
    
    def save_history(self) -> None:
        """Save evaluation history to disk."""
        with open(self.metrics_path, 'w') as f:
            json.dump(self.evaluation_history, f, indent=2)
    
    def evaluate_analysis_quality(self, results: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate the quality of an analysis run.
        
        Args:
            results: Analysis results dictionary
            
        Returns:
            Dictionary of quality scores (0-1 scale)
        """
        scores = {}
        
        # 1. Completeness Score
        # Check if all expected outputs are present
        expected_keys = ['insights', 'visualizations', 'report_path', 'data_summary']
        completeness = sum(1 for key in expected_keys if key in results and results[key]) / len(expected_keys)
        scores['completeness'] = completeness
        
        # 2. Insight Quality Score
        # Based on number and depth of insights
        insights = results.get('insights', [])
        insight_score = min(len(insights) / 5.0, 1.0)  # Target: 5+ insights
        avg_insight_length = sum(len(i) for i in insights) / len(insights) if insights else 0
        depth_score = min(avg_insight_length / 100.0, 1.0)  # Target: 100+ chars per insight
        scores['insight_quality'] = (insight_score + depth_score) / 2
        
        # 3. Visualization Coverage Score
        # Based on number of visualizations created
        viz_count = len(results.get('visualizations', []))
        scores['visualization_coverage'] = min(viz_count / 3.0, 1.0)  # Target: 3+ visualizations
        
        # 4. Data Coverage Score
        # Based on how much of the data was analyzed
        data_summary = results.get('data_summary', {})
        if data_summary:
            total_cols = data_summary.get('shape', {}).get('columns', 0)
            analyzed_cols = len(results.get('analysis_results', {}).get('correlation_analysis', {}).get('correlation_matrix', {}))
            scores['data_coverage'] = min(analyzed_cols / total_cols, 1.0) if total_cols > 0 else 0
        else:
            scores['data_coverage'] = 0
        
        # 5. Overall Quality Score
        scores['overall_quality'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def evaluate_performance(self, results: Dict[str, Any], 
                           execution_time: float) -> Dict[str, Any]:
        """
        Evaluate system performance metrics.
        
        Args:
            results: Analysis results
            execution_time: Total execution time in seconds
            
        Returns:
            Performance metrics dictionary
        """
        metrics = observability.get_metrics()
        
        performance = {
            'execution_time_seconds': execution_time,
            'agent_calls': metrics['agent_calls'],
            'tool_executions': metrics['tool_executions'],
            'avg_tool_time': metrics['avg_processing_time'],
            'error_rate': metrics['error_rate'],
            'errors': metrics['errors']
        }
        
        # Performance scores (0-1 scale, higher is better)
        performance['speed_score'] = max(0, 1 - (execution_time / 60.0))  # Target: < 60 seconds
        performance['efficiency_score'] = max(0, 1 - metrics['error_rate'])  # Target: 0% errors
        performance['reliability_score'] = 1.0 if results.get('success', False) else 0.0
        
        performance['overall_performance'] = (
            performance['speed_score'] +
            performance['efficiency_score'] +
            performance['reliability_score']
        ) / 3
        
        return performance
    
    def evaluate_memory_usage(self, session_id: str, memory_bank) -> Dict[str, Any]:
        """
        Evaluate memory system effectiveness.
        
        Args:
            session_id: Current session ID
            memory_bank: MemoryBank instance
            
        Returns:
            Memory usage metrics
        """
        session = memory_bank.load_session(session_id)
        
        if not session:
            return {'error': 'Session not found'}
        
        metrics = {
            'insights_stored': len(session.insights),
            'visualizations_stored': len(session.visualizations),
            'analysis_history_length': len(session.analysis_history),
            'global_insights_total': len(memory_bank.global_insights),
            'learned_patterns_count': sum(len(v) if isinstance(v, list) else 1 
                                         for v in memory_bank.learned_patterns.values())
        }
        
        # Memory effectiveness score
        metrics['memory_effectiveness'] = min(
            (metrics['insights_stored'] + 
             metrics['visualizations_stored'] + 
             metrics['analysis_history_length']) / 10.0,
            1.0
        )
        
        return metrics
    
    def comprehensive_evaluation(self, results: Dict[str, Any], 
                                execution_time: float,
                                session_id: str,
                                memory_bank) -> Dict[str, Any]:
        """
        Perform comprehensive evaluation of system performance.
        
        Args:
            results: Analysis results
            execution_time: Execution time in seconds
            session_id: Session identifier
            memory_bank: MemoryBank instance
            
        Returns:
            Complete evaluation report
        """
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'quality_scores': self.evaluate_analysis_quality(results),
            'performance_metrics': self.evaluate_performance(results, execution_time),
            'memory_metrics': self.evaluate_memory_usage(session_id, memory_bank)
        }
        
        # Calculate overall system score (0-100)
        quality_score = evaluation['quality_scores']['overall_quality']
        performance_score = evaluation['performance_metrics']['overall_performance']
        memory_score = evaluation['memory_metrics'].get('memory_effectiveness', 0)
        
        evaluation['overall_score'] = (quality_score * 0.5 + 
                                      performance_score * 0.3 + 
                                      memory_score * 0.2) * 100
        
        # Grade the system
        score = evaluation['overall_score']
        if score >= 90:
            evaluation['grade'] = 'A - Excellent'
        elif score >= 80:
            evaluation['grade'] = 'B - Good'
        elif score >= 70:
            evaluation['grade'] = 'C - Satisfactory'
        elif score >= 60:
            evaluation['grade'] = 'D - Needs Improvement'
        else:
            evaluation['grade'] = 'F - Poor'
        
        # Store evaluation
        self.evaluation_history.append(evaluation)
        self.save_history()
        
        return evaluation
    
    def get_improvement_recommendations(self, evaluation: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on evaluation results.
        
        Args:
            evaluation: Evaluation results
            
        Returns:
            List of improvement recommendations
        """
        recommendations = []
        
        quality = evaluation['quality_scores']
        performance = evaluation['performance_metrics']
        
        # Quality recommendations
        if quality['completeness'] < 0.8:
            recommendations.append(
                "Improve completeness: Ensure all analysis components are generated"
            )
        
        if quality['insight_quality'] < 0.7:
            recommendations.append(
                "Enhance insight quality: Generate more detailed and actionable insights"
            )
        
        if quality['visualization_coverage'] < 0.7:
            recommendations.append(
                "Increase visualization coverage: Create more diverse visualizations"
            )
        
        # Performance recommendations
        if performance['execution_time_seconds'] > 60:
            recommendations.append(
                f"Optimize execution time: Currently {performance['execution_time_seconds']:.1f}s, target < 60s"
            )
        
        if performance['error_rate'] > 0.1:
            recommendations.append(
                f"Reduce error rate: Currently {performance['error_rate']:.1%}, target < 10%"
            )
        
        # Memory recommendations
        memory = evaluation['memory_metrics']
        if memory.get('memory_effectiveness', 0) < 0.5:
            recommendations.append(
                "Improve memory utilization: Store more insights and patterns for context"
            )
        
        if not recommendations:
            recommendations.append("System is performing well! Continue monitoring.")
        
        return recommendations
    
    def generate_evaluation_report(self, evaluation: Dict[str, Any]) -> str:
        """
        Generate a formatted evaluation report.
        
        Args:
            evaluation: Evaluation results
            
        Returns:
            Formatted report string
        """
        recommendations = self.get_improvement_recommendations(evaluation)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    AGENT EVALUATION REPORT                           ║
╚══════════════════════════════════════════════════════════════════════╝

Session: {evaluation['session_id']}
Timestamp: {evaluation['timestamp']}

OVERALL SCORE: {evaluation['overall_score']:.1f}/100
GRADE: {evaluation['grade']}

───────────────────────────────────────────────────────────────────────
QUALITY METRICS
───────────────────────────────────────────────────────────────────────
Completeness:              {evaluation['quality_scores']['completeness']:.2%}
Insight Quality:           {evaluation['quality_scores']['insight_quality']:.2%}
Visualization Coverage:    {evaluation['quality_scores']['visualization_coverage']:.2%}
Data Coverage:             {evaluation['quality_scores']['data_coverage']:.2%}
Overall Quality:           {evaluation['quality_scores']['overall_quality']:.2%}

───────────────────────────────────────────────────────────────────────
PERFORMANCE METRICS
───────────────────────────────────────────────────────────────────────
Execution Time:            {evaluation['performance_metrics']['execution_time_seconds']:.2f}s
Agent Calls:               {evaluation['performance_metrics']['agent_calls']}
Tool Executions:           {evaluation['performance_metrics']['tool_executions']}
Average Tool Time:         {evaluation['performance_metrics']['avg_tool_time']:.3f}s
Error Rate:                {evaluation['performance_metrics']['error_rate']:.2%}
Overall Performance:       {evaluation['performance_metrics']['overall_performance']:.2%}

───────────────────────────────────────────────────────────────────────
MEMORY METRICS
───────────────────────────────────────────────────────────────────────
Insights Stored:           {evaluation['memory_metrics'].get('insights_stored', 0)}
Visualizations:            {evaluation['memory_metrics'].get('visualizations_stored', 0)}
Analysis History:          {evaluation['memory_metrics'].get('analysis_history_length', 0)}
Global Insights:           {evaluation['memory_metrics'].get('global_insights_total', 0)}
Memory Effectiveness:      {evaluation['memory_metrics'].get('memory_effectiveness', 0):.2%}

───────────────────────────────────────────────────────────────────────
RECOMMENDATIONS
───────────────────────────────────────────────────────────────────────
"""
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += "\n═══════════════════════════════════════════════════════════════════════\n"
        
        return report
    
    def get_historical_trends(self) -> Dict[str, Any]:
        """
        Analyze trends across evaluation history.
        
        Returns:
            Dictionary of trend analysis
        """
        if not self.evaluation_history:
            return {"message": "No evaluation history available"}
        
        # Calculate averages over time
        avg_quality = sum(e['quality_scores']['overall_quality'] 
                         for e in self.evaluation_history) / len(self.evaluation_history)
        
        avg_performance = sum(e['performance_metrics']['overall_performance'] 
                             for e in self.evaluation_history) / len(self.evaluation_history)
        
        avg_score = sum(e['overall_score'] 
                       for e in self.evaluation_history) / len(self.evaluation_history)
        
        # Trend direction
        if len(self.evaluation_history) >= 2:
            recent_score = self.evaluation_history[-1]['overall_score']
            older_score = self.evaluation_history[-2]['overall_score']
            trend = "improving" if recent_score > older_score else "declining" if recent_score < older_score else "stable"
        else:
            trend = "insufficient data"
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "average_quality_score": avg_quality,
            "average_performance_score": avg_performance,
            "average_overall_score": avg_score,
            "trend": trend,
            "best_score": max(e['overall_score'] for e in self.evaluation_history),
            "worst_score": min(e['overall_score'] for e in self.evaluation_history)
        }


def evaluate_analysis(results: Dict[str, Any], 
                     execution_time: float,
                     session_id: str,
                     memory_bank,
                     verbose: bool = True) -> Dict[str, Any]:
    """
    Convenience function to evaluate an analysis run.
    
    Args:
        results: Analysis results
        execution_time: Execution time
        session_id: Session ID
        memory_bank: MemoryBank instance
        verbose: Whether to print report
        
    Returns:
        Evaluation results
    """
    evaluator = AgentEvaluator()
    evaluation = evaluator.comprehensive_evaluation(
        results, execution_time, session_id, memory_bank
    )
    
    if verbose:
        report = evaluator.generate_evaluation_report(evaluation)
        print(report)
        
        # Show trends
        trends = evaluator.get_historical_trends()
        print("\n📈 Historical Trends:")
        print(f"   Total Evaluations: {trends['total_evaluations']}")
        print(f"   Average Score: {trends['average_overall_score']:.1f}/100")
        print(f"   Trend: {trends['trend']}")
        print(f"   Best Score: {trends['best_score']:.1f}")
        print(f"   Worst Score: {trends['worst_score']:.1f}\n")
    
    return evaluation

