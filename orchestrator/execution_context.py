from datetime import datetime
from typing import List, Dict, Any


class ExecutionContext:
    """Tracks agent execution metadata throughout the pipeline."""
    
    PIPELINE_VERSION = "1.0.0"
    
    def __init__(self):
        """Initialize execution context with empty agent list and current timestamp."""
        self.agents_involved: List[str] = []
        self.execution_timestamp: str = datetime.now().isoformat()
    
    def record_agent(self, agent_name: str) -> None:
        if agent_name not in self.agents_involved:
            self.agents_involved.append(agent_name)
    
    def generate_meta(self, page_type: str) -> Dict[str, Any]:
        """Generate _meta object for final JSON outputs."""
        return {
            "generated_by": self._get_final_agent(page_type),
            "agents_involved": self.agents_involved.copy(),
            "execution_timestamp": self.execution_timestamp,
            "pipeline_version": self.PIPELINE_VERSION
        }
    
    def _get_final_agent(self, page_type: str) -> str:
        return "PageBuilder"
