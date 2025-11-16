"""
Main entry point for the BI Intelligence Agent System.
Provides CLI interface for running business intelligence analysis.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from config import Config
from agents import CoordinatorAgent
from memory import MemoryBank
from observability import observability


def print_banner():
    """Print welcome banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     📊 BI INTELLIGENCE AGENT SYSTEM 📊                   ║
    ║                                                          ║
    ║     Multi-Agent Business Intelligence Analyzer           ║
    ║     Powered by Google Gemini                            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_results(results: dict):
    """
    Print analysis results in a formatted way.
    
    Args:
        results: Results dictionary from analysis
    """
    if results["success"]:
        print("\n✅ Analysis Complete!")
        print(f"📁 Session ID: {results['session_id']}")
        print(f"\n📊 Data Summary:")
        summary = results.get("data_summary", {})
        print(f"   • Rows: {summary.get('shape', {}).get('rows', 'N/A')}")
        print(f"   • Columns: {summary.get('shape', {}).get('columns', 'N/A')}")
        
        print(f"\n💡 Key Insights ({len(results.get('insights', []))}):")
        for i, insight in enumerate(results.get("insights", [])[:5], 1):
            print(f"   {i}. {insight}")
        
        print(f"\n📈 Visualizations Created: {len(results.get('visualizations', []))}")
        for viz in results.get("visualizations", []):
            print(f"   • {Path(viz).name}")
        
        print(f"\n📄 Report Generated:")
        print(f"   {results['report_path']}")
        
        print("\n" + "="*60)
        print("Open the HTML report in your browser to view the full analysis!")
        print("="*60 + "\n")
    else:
        print(f"\n❌ Analysis Failed: {results.get('error', 'Unknown error')}")


def analyze_command(args):
    """
    Execute the analyze command.
    
    Args:
        args: Parsed command line arguments
    """
    print(f"\n🔍 Analyzing file: {args.file}")
    print("⚙️  Initializing agents...")
    
    # Initialize system
    memory_bank = MemoryBank()
    coordinator = CoordinatorAgent(memory_bank)
    
    print("🚀 Starting analysis...")
    
    # Run analysis
    if args.type == "timeseries":
        if not args.date_column or not args.value_column:
            print("❌ Error: Time series analysis requires --date-column and --value-column")
            sys.exit(1)
        
        results = coordinator.analyze_time_series(
            args.file, 
            args.date_column, 
            args.value_column
        )
    else:
        results = coordinator.analyze_file(args.file, args.type)
    
    # Print results
    print_results(results)
    
    # Show metrics if verbose
    if args.verbose:
        print("\n📊 Performance Metrics:")
        metrics = observability.get_metrics()
        for key, value in metrics.items():
            print(f"   • {key}: {value}")


def list_sessions_command(args):
    """
    Execute the list-sessions command.
    
    Args:
        args: Parsed command line arguments
    """
    memory_bank = MemoryBank()
    sessions = memory_bank.list_sessions()
    
    print(f"\n📋 Found {len(sessions)} session(s):\n")
    
    for session in sessions[:10]:  # Show last 10 sessions
        print(f"  Session: {session['session_id']}")
        print(f"  Created: {session['created_at']}")
        print(f"  Dataset: {session['dataset']}")
        print("  " + "-"*50)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="BI Intelligence Agent System - Multi-Agent Business Intelligence Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a CSV file
  python main.py analyze data/sales.csv

  # Analyze with time series
  python main.py analyze data/sales.csv --type timeseries --date-column Date --value-column Revenue

  # List previous sessions
  python main.py list-sessions

For more information, see README.md
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a data file")
    analyze_parser.add_argument("file", type=str, help="Path to data file (CSV, JSON, Excel)")
    analyze_parser.add_argument(
        "--type", 
        type=str, 
        choices=["comprehensive", "timeseries"], 
        default="comprehensive",
        help="Type of analysis to perform"
    )
    analyze_parser.add_argument(
        "--date-column", 
        type=str, 
        help="Date column name (required for timeseries)"
    )
    analyze_parser.add_argument(
        "--value-column", 
        type=str, 
        help="Value column name (required for timeseries)"
    )
    analyze_parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Show detailed metrics"
    )
    
    # List sessions command
    list_parser = subparsers.add_parser("list-sessions", help="List previous analysis sessions")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check if API key is configured
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n📝 Setup Instructions:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey")
        print("   3. Run the command again")
        sys.exit(1)
    
    # Execute command
    if args.command == "analyze":
        analyze_command(args)
    elif args.command == "list-sessions":
        list_sessions_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

