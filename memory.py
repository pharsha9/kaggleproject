"""
Memory and session management for the BI Intelligence Agent System.
Provides state persistence and context management across multiple analysis sessions.
"""

import json
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict, field
from config import Config


@dataclass
class AnalysisSession:
    """Represents an analysis session with its context and history."""
    
    session_id: str
    created_at: str
    last_updated: str
    dataset_info: Dict[str, Any] = field(default_factory=dict)
    analysis_history: List[Dict[str, Any]] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    visualizations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalysisSession':
        """Create session from dictionary."""
        return cls(**data)


class MemoryBank:
    """
    Long-term memory storage for analysis sessions and learned patterns.
    Maintains context across multiple sessions for improved analysis.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize the memory bank.
        
        Args:
            storage_path: Path to store memory files
        """
        self.storage_path = storage_path or (Config.BASE_DIR / "memory")
        self.storage_path.mkdir(exist_ok=True)
        self.sessions_path = self.storage_path / "sessions"
        self.sessions_path.mkdir(exist_ok=True)
        self.insights_path = self.storage_path / "insights.json"
        self.patterns_path = self.storage_path / "patterns.json"
        
        # Load existing insights and patterns
        self.global_insights = self._load_insights()
        self.learned_patterns = self._load_patterns()
    
    def _load_insights(self) -> List[str]:
        """Load global insights from storage."""
        if self.insights_path.exists():
            with open(self.insights_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_insights(self) -> None:
        """Save global insights to storage."""
        with open(self.insights_path, 'w') as f:
            json.dump(self.global_insights, f, indent=2)
    
    def _load_patterns(self) -> Dict[str, Any]:
        """Load learned patterns from storage."""
        if self.patterns_path.exists():
            with open(self.patterns_path, 'r') as f:
                return json.load(f)
        return {
            "common_columns": {},
            "typical_ranges": {},
            "correlation_patterns": []
        }
    
    def _save_patterns(self) -> None:
        """Save learned patterns to storage."""
        with open(self.patterns_path, 'w') as f:
            json.dump(self.learned_patterns, f, indent=2)
    
    def create_session(self, dataset_info: Optional[Dict[str, Any]] = None) -> AnalysisSession:
        """
        Create a new analysis session.
        
        Args:
            dataset_info: Information about the dataset being analyzed
            
        Returns:
            New AnalysisSession object
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        session = AnalysisSession(
            session_id=session_id,
            created_at=timestamp,
            last_updated=timestamp,
            dataset_info=dataset_info or {}
        )
        
        self.save_session(session)
        return session
    
    def save_session(self, session: AnalysisSession) -> None:
        """
        Save a session to persistent storage.
        
        Args:
            session: Session to save
        """
        session.last_updated = datetime.now().isoformat()
        session_file = self.sessions_path / f"{session.session_id}.json"
        
        with open(session_file, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)
    
    def load_session(self, session_id: str) -> Optional[AnalysisSession]:
        """
        Load a session from storage.
        
        Args:
            session_id: ID of the session to load
            
        Returns:
            AnalysisSession object or None if not found
        """
        session_file = self.sessions_path / f"{session_id}.json"
        
        if not session_file.exists():
            return None
        
        with open(session_file, 'r') as f:
            data = json.load(f)
            return AnalysisSession.from_dict(data)
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all stored sessions.
        
        Returns:
            List of session summaries
        """
        sessions = []
        for session_file in self.sessions_path.glob("session_*.json"):
            with open(session_file, 'r') as f:
                data = json.load(f)
                sessions.append({
                    "session_id": data["session_id"],
                    "created_at": data["created_at"],
                    "last_updated": data["last_updated"],
                    "dataset": data.get("dataset_info", {}).get("name", "Unknown")
                })
        
        return sorted(sessions, key=lambda x: x["last_updated"], reverse=True)
    
    def add_analysis_result(self, session: AnalysisSession, 
                           analysis_type: str, result: Dict[str, Any]) -> None:
        """
        Add an analysis result to the session history.
        
        Args:
            session: Session to update
            analysis_type: Type of analysis performed
            result: Analysis results
        """
        session.analysis_history.append({
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "result": result
        })
        self.save_session(session)
    
    def add_insight(self, session: AnalysisSession, insight: str, 
                   is_global: bool = False) -> None:
        """
        Add an insight to the session and optionally to global insights.
        
        Args:
            session: Session to update
            insight: Insight text
            is_global: Whether to add to global insights
        """
        session.insights.append(insight)
        
        if is_global and insight not in self.global_insights:
            self.global_insights.append(insight)
            self._save_insights()
        
        self.save_session(session)
    
    def add_visualization(self, session: AnalysisSession, viz_path: str) -> None:
        """
        Record a visualization in the session.
        
        Args:
            session: Session to update
            viz_path: Path to the visualization file
        """
        session.visualizations.append(viz_path)
        self.save_session(session)
    
    def learn_pattern(self, pattern_type: str, pattern_data: Dict[str, Any]) -> None:
        """
        Store a learned pattern for future reference.
        
        Args:
            pattern_type: Type of pattern (e.g., 'correlation', 'range')
            pattern_data: Pattern details
        """
        if pattern_type not in self.learned_patterns:
            self.learned_patterns[pattern_type] = []
        
        self.learned_patterns[pattern_type].append({
            "timestamp": datetime.now().isoformat(),
            "data": pattern_data
        })
        
        self._save_patterns()
    
    def get_relevant_context(self, dataset_columns: List[str]) -> Dict[str, Any]:
        """
        Get relevant context from memory based on dataset characteristics.
        
        Args:
            dataset_columns: List of column names in the current dataset
            
        Returns:
            Dictionary with relevant context from memory
        """
        context = {
            "similar_analyses": [],
            "relevant_insights": [],
            "suggested_analyses": []
        }
        
        # Ensure dataset_columns is a list
        if not isinstance(dataset_columns, list):
            dataset_columns = list(dataset_columns) if dataset_columns else []
        
        # Find similar past analyses
        for session_file in self.sessions_path.glob("session_*.json"):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    past_columns = data.get("dataset_info", {}).get("columns", [])
                    
                    # Ensure past_columns is a list
                    if not isinstance(past_columns, list):
                        past_columns = list(past_columns) if past_columns else []
                    
                    # Calculate similarity based on common columns
                    if dataset_columns and past_columns:
                        common_cols = set(dataset_columns) & set(past_columns)
                        if len(common_cols) > 0:
                            similarity = len(common_cols) / len(set(dataset_columns) | set(past_columns))
                            if similarity > 0.3:  # 30% similarity threshold
                                context["similar_analyses"].append({
                                    "session_id": data["session_id"],
                                    "similarity": similarity,
                                    "common_columns": list(common_cols)
                                })
            except Exception as e:
                # Skip problematic session files
                continue
        
        # Add relevant global insights
        context["relevant_insights"] = self.global_insights[-5:]  # Last 5 insights
        
        return context


class InMemorySessionService:
    """
    In-memory session management for active analysis sessions.
    Provides fast access to current session state.
    """
    
    def __init__(self, memory_bank: MemoryBank):
        """
        Initialize the session service.
        
        Args:
            memory_bank: Memory bank for persistent storage
        """
        self.memory_bank = memory_bank
        self.active_sessions: Dict[str, AnalysisSession] = {}
        self.current_session_id: Optional[str] = None
    
    def start_session(self, dataset_info: Optional[Dict[str, Any]] = None) -> AnalysisSession:
        """
        Start a new analysis session.
        
        Args:
            dataset_info: Information about the dataset
            
        Returns:
            New AnalysisSession object
        """
        session = self.memory_bank.create_session(dataset_info)
        self.active_sessions[session.session_id] = session
        self.current_session_id = session.session_id
        return session
    
    def get_current_session(self) -> Optional[AnalysisSession]:
        """
        Get the current active session.
        
        Returns:
            Current AnalysisSession or None
        """
        if self.current_session_id:
            return self.active_sessions.get(self.current_session_id)
        return None
    
    def update_session(self, session_id: str, **kwargs) -> None:
        """
        Update session data.
        
        Args:
            session_id: Session to update
            **kwargs: Fields to update
        """
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            self.memory_bank.save_session(session)
    
    def persist_session(self, session_id: str) -> None:
        """
        Persist a session to the memory bank.
        
        Args:
            session_id: Session to persist
        """
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            self.memory_bank.save_session(session)
    
    def end_session(self, session_id: str) -> None:
        """
        End and persist a session.
        
        Args:
            session_id: Session to end
        """
        self.persist_session(session_id)
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if self.current_session_id == session_id:
            self.current_session_id = None

