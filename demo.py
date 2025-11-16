"""
Demo script showcasing the BI Intelligence Agent System capabilities.
This script demonstrates all key features required for the capstone project.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import Config
from agents import CoordinatorAgent
from memory import MemoryBank
from observability import observability


def demo_comprehensive_analysis():
    """
    Demonstrate comprehensive data analysis with the multi-agent system.
    
    This demonstrates:
    - Multi-agent coordination (Coordinator, DataAnalyst, Visualizer, ReportGenerator)
    - Parallel agent execution (analysis + visualization)
    - Sequential agent execution (report generation after analysis)
    - Custom tools for data analysis and visualization
    """
    print("\n" + "="*80)
    print("DEMO 1: Comprehensive Business Intelligence Analysis")
    print("="*80 + "\n")
    
    # Initialize system
    print("🔧 Initializing multi-agent system...")
    memory_bank = MemoryBank()
    coordinator = CoordinatorAgent(memory_bank)
    
    # Sample data file
    data_file = Config.DATA_DIR / "examples" / "sales_data.csv"
    
    if not data_file.exists():
        print(f"❌ Sample data not found at {data_file}")
        return
    
    print(f"📊 Analyzing: {data_file}")
    print("\n🤖 Active Agents:")
    print("   • Coordinator Agent - Orchestrates the workflow")
    print("   • Data Analyst Agent - Statistical analysis")
    print("   • Visualization Agent - Creates visualizations")
    print("   • Report Generator Agent - Synthesizes findings\n")
    
    # Run analysis
    print("🚀 Starting analysis pipeline...\n")
    results = coordinator.analyze_file(str(data_file))
    
    if results["success"]:
        print("\n✅ Analysis Complete!\n")
        print(f"📁 Session ID: {results['session_id']}")
        print(f"\n📊 Data Summary:")
        summary = results["data_summary"]
        print(f"   • Rows: {summary['shape']['rows']}")
        print(f"   • Columns: {summary['shape']['columns']}")
        print(f"   • Memory: {summary['memory_usage']}")
        
        print(f"\n💡 Key Insights ({len(results['insights'])}):")
        for i, insight in enumerate(results['insights'][:5], 1):
            print(f"   {i}. {insight[:100]}...")
        
        print(f"\n📈 Visualizations: {len(results['visualizations'])} created")
        for viz in results['visualizations']:
            print(f"   • {Path(viz).name}")
        
        print(f"\n📄 Report: {results['report_path']}")
        
        # Show performance metrics
        print("\n📊 Performance Metrics:")
        metrics = observability.get_metrics()
        print(f"   • Agent Calls: {metrics['agent_calls']}")
        print(f"   • Tool Executions: {metrics['tool_executions']}")
        print(f"   • Avg Processing Time: {metrics['avg_processing_time']:.2f}s")
        print(f"   • Error Rate: {metrics['error_rate']:.2%}")
    else:
        print(f"❌ Analysis failed: {results['error']}")


def demo_time_series_analysis():
    """
    Demonstrate time series analysis capabilities.
    
    This demonstrates:
    - Specialized analysis workflows
    - Time series visualization
    - Trend detection and forecasting insights
    """
    print("\n" + "="*80)
    print("DEMO 2: Time Series Analysis")
    print("="*80 + "\n")
    
    # Initialize system
    memory_bank = MemoryBank()
    coordinator = CoordinatorAgent(memory_bank)
    
    # Sample data file
    data_file = Config.DATA_DIR / "examples" / "sales_data.csv"
    
    if not data_file.exists():
        print(f"❌ Sample data not found at {data_file}")
        return
    
    print(f"📈 Analyzing time series: Revenue over Time")
    print("\n🚀 Starting time series analysis...\n")
    
    # Run time series analysis
    results = coordinator.analyze_time_series(
        str(data_file),
        date_column="Date",
        value_column="Revenue"
    )
    
    if results["success"]:
        print("✅ Time Series Analysis Complete!\n")
        
        trend = results["trend_results"]
        print(f"📊 Trend Analysis:")
        print(f"   • Direction: {trend['trend_direction']}")
        print(f"   • Growth Rate: {trend.get('growth_rate', 'N/A'):.2f}%")
        print(f"   • R-squared: {trend['r_squared']:.4f}")
        print(f"   • Mean: ${trend['mean']:,.2f}")
        
        print(f"\n💡 AI Insights:")
        print(f"   {trend['ai_insights'][:200]}...")
        
        print(f"\n📄 Report: {results['report_path']}")
    else:
        print(f"❌ Analysis failed: {results['error']}")


def demo_memory_and_sessions():
    """
    Demonstrate memory bank and session management.
    
    This demonstrates:
    - Session persistence
    - Memory across multiple analyses
    - Context retrieval for improved insights
    """
    print("\n" + "="*80)
    print("DEMO 3: Memory Bank & Session Management")
    print("="*80 + "\n")
    
    memory_bank = MemoryBank()
    
    print("📚 Memory Bank Features:")
    print("   • Persistent session storage")
    print("   • Global insights accumulation")
    print("   • Pattern learning across analyses")
    print("   • Context-aware recommendations\n")
    
    # List previous sessions
    sessions = memory_bank.list_sessions()
    print(f"📋 Found {len(sessions)} session(s) in memory:\n")
    
    for session in sessions[:5]:  # Show last 5
        print(f"   Session: {session['session_id']}")
        print(f"   Created: {session['created_at']}")
        print(f"   Dataset: {session['dataset']}")
        print("   " + "-"*60)
    
    # Show global insights
    print(f"\n💡 Global Insights Learned: {len(memory_bank.global_insights)}")
    for i, insight in enumerate(memory_bank.global_insights[-3:], 1):
        print(f"   {i}. {insight[:80]}...")


def demo_observability():
    """
    Demonstrate observability features.
    
    This demonstrates:
    - Structured logging
    - Performance tracking
    - Error monitoring
    - Metrics collection
    """
    print("\n" + "="*80)
    print("DEMO 4: Observability & Monitoring")
    print("="*80 + "\n")
    
    print("📊 Observability Features:")
    print("   • Structured JSON logging")
    print("   • Agent call tracing")
    print("   • Tool execution timing")
    print("   • Error tracking")
    print("   • Performance metrics\n")
    
    # Get current metrics
    metrics = observability.get_metrics()
    
    print("📈 Current Session Metrics:")
    print(f"   • Agent Calls: {metrics['agent_calls']}")
    print(f"   • Tool Executions: {metrics['tool_executions']}")
    print(f"   • Total Processing Time: {metrics['total_processing_time']:.2f}s")
    print(f"   • Average Processing Time: {metrics['avg_processing_time']:.2f}s")
    print(f"   • Errors: {metrics['errors']}")
    print(f"   • Error Rate: {metrics['error_rate']:.2%}")


def main():
    """Run all demos."""
    print("\n" + "="*80)
    print("🎯 BI INTELLIGENCE AGENT SYSTEM - FEATURE DEMONSTRATION")
    print("="*80)
    print("\nThis demo showcases all required capstone features:")
    print("✓ Multi-agent system (Coordinator, Analyst, Visualizer, Reporter)")
    print("✓ Parallel & Sequential agent execution")
    print("✓ Custom tools (Data ingestion, Statistics, Visualization, Reports)")
    print("✓ Sessions & Memory (State management, Memory Bank)")
    print("✓ Observability (Logging, Tracing, Metrics)")
    print("✓ Google Gemini integration")
    
    try:
        # Check configuration
        Config.validate()
        
        # Run demos
        demo_comprehensive_analysis()
        demo_time_series_analysis()
        demo_memory_and_sessions()
        demo_observability()
        
        print("\n" + "="*80)
        print("✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*80 + "\n")
        
        print("📚 Next Steps:")
        print("   1. Open the generated HTML reports in your browser")
        print("   2. Review the visualizations in the outputs/ directory")
        print("   3. Check the memory/ directory for session data")
        print("   4. Try analyzing your own data files!\n")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n📝 Setup Instructions:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey")
        print("   3. Run the demo again\n")
    except Exception as e:
        print(f"\n❌ Demo Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

