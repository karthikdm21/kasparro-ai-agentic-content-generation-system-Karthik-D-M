"""
Execution Context Tracker - Lightweight metadata tracking for agent execution.

This module provides a simple utility to track agent execution order and
generate metadata for output files without modifying existing agent logic.
"""

from datetime import datetime
from typing import List, Dict, Any


class ExecutionContext:
    """
    Tracks agent execution metadata throughout the pipeline.
    
    This class maintains a record of which agents have executed and in what
    order, enabling transparent execution tracking without global state or
    invasive changes to existing agent logic.
    """
    
    PIPELINE_VERSION = "1.0.0"
    
    def __init__(self):
        """Initialize execution context with empty agent list and current timestamp."""
        self.agents_involved: List[str] = []
        self.execution_timestamp: str = datetime.now().isoformat()
    
    def record_agent(self, agent_name: str) -> None:
        """
        Record an agent execution.
        
        Args:
            agent_name: Name of the agent that executed
        """
        if agent_name not in self.agents_involved:
            self.agents_involved.append(agent_name)
    
    def generate_meta(self, page_type: str) -> Dict[str, Any]:
        """
        Generate _meta object for a specific page type.
        
        Args:
            page_type: Type of page (faq, product, comparison)
            
        Returns:
            Dictionary containing metadata for the page
        """
        return {
            "generated_by": self._get_final_agent(page_type),
            "agents_involved": self.agents_involved.copy(),
            "execution_timestamp": self.execution_timestamp,
            "pipeline_version": self.PIPELINE_VERSION
        }
    
    def _get_final_agent(self, page_type: str) -> str:
        """
        Determine the final agent responsible for a page type.
        
        Args:
            page_type: Type of page
            
        Returns:
            Name of the final agent
        """
        return "PageBuilderAgent"
