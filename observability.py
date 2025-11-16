"""
Observability module for logging, tracing, and monitoring agent activities.
Provides structured logging and performance tracking for the BI Intelligence Agent System.
"""

import structlog
import time
import functools
from typing import Any, Callable, Dict, Optional
from datetime import datetime
from pathlib import Path
from config import Config


class ObservabilityManager:
    """Manages logging and tracing for agent operations."""
    
    def __init__(self):
        """Initialize the observability manager with structured logging."""
        self.setup_logging()
        self.metrics: Dict[str, Any] = {
            "agent_calls": 0,
            "tool_executions": 0,
            "errors": 0,
            "total_processing_time": 0.0
        }
        self.logger = structlog.get_logger()
    
    def setup_logging(self) -> None:
        """Configure structured logging with appropriate processors."""
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    
    def log_agent_call(self, agent_name: str, task: str, **kwargs) -> None:
        """Log an agent invocation."""
        self.metrics["agent_calls"] += 1
        self.logger.info(
            "agent_call",
            agent_name=agent_name,
            task=task,
            timestamp=datetime.now().isoformat(),
            **kwargs
        )
    
    def log_tool_execution(self, tool_name: str, duration: float, success: bool, **kwargs) -> None:
        """Log a tool execution with performance metrics."""
        self.metrics["tool_executions"] += 1
        self.metrics["total_processing_time"] += duration
        
        if not success:
            self.metrics["errors"] += 1
        
        self.logger.info(
            "tool_execution",
            tool_name=tool_name,
            duration_seconds=duration,
            success=success,
            timestamp=datetime.now().isoformat(),
            **kwargs
        )
    
    def log_error(self, error_type: str, message: str, **kwargs) -> None:
        """Log an error occurrence."""
        self.metrics["errors"] += 1
        self.logger.error(
            "error_occurred",
            error_type=error_type,
            message=message,
            timestamp=datetime.now().isoformat(),
            **kwargs
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics summary."""
        return {
            **self.metrics,
            "avg_processing_time": (
                self.metrics["total_processing_time"] / self.metrics["tool_executions"]
                if self.metrics["tool_executions"] > 0 else 0
            ),
            "error_rate": (
                self.metrics["errors"] / self.metrics["tool_executions"]
                if self.metrics["tool_executions"] > 0 else 0
            )
        }
    
    def log_metrics_summary(self) -> None:
        """Log a summary of collected metrics."""
        metrics = self.get_metrics()
        self.logger.info("metrics_summary", **metrics)


def trace_execution(func: Callable) -> Callable:
    """Decorator to trace function execution time and log it."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        result = None
        error = None
        
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            error = str(e)
            raise
        finally:
            duration = time.time() - start_time
            
            # Get observability manager if available
            if hasattr(args[0], 'observability'):
                obs = args[0].observability
                obs.log_tool_execution(
                    tool_name=func.__name__,
                    duration=duration,
                    success=success,
                    error=error
                )
    
    return wrapper


# Global observability instance
observability = ObservabilityManager()

