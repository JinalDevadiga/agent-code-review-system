import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from utils.llm_client import LLMClient
from dataclasses import dataclass, asdict
import time


@dataclass
class AgentResult:
    """Structure for agent execution results"""
    agent_type: str
    model: str
    success: bool
    result: Dict[str, Any]
    error: Optional[str] = None
    execution_time: float = 0.0
    tokens_used: int = 0
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        if self.metadata is None:
            data['metadata'] = {}
        return data


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model: str, system_prompt: str, temperature: float = 0.7):
        """
        Initialize agent
        
        Args:
            model: LLM model to use
            system_prompt: System prompt for the agent
            temperature: LLM temperature parameter
        """
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.llm = LLMClient(model=model, temperature=temperature)
        self.execution_history = []
        
    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's primary task
        
        Must be implemented by subclasses
        """
        pass
    
    def _call_llm(
        self,
        user_message: str,
        json_mode: bool = True,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Call the LLM with error handling
        
        Args:
            user_message: Message to send to LLM
            json_mode: Whether to expect JSON response
            max_tokens: Maximum tokens to generate
            
        Returns:
            LLM response dictionary
        """
        result = self.llm.call(
            system_prompt=self.system_prompt,
            user_message=user_message,
            max_tokens=max_tokens,
            json_mode=json_mode
        )
        return result
    
    def _create_result(
        self,
        success: bool,
        result: Dict[str, Any],
        error: Optional[str] = None,
        execution_time: float = 0.0,
        tokens_used: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        """Create a structured result"""
        return AgentResult(
            agent_type=self.__class__.__name__,
            model=self.model,
            success=success,
            result=result,
            error=error,
            execution_time=execution_time,
            tokens_used=tokens_used,
            metadata=metadata or {}
        )
    
    def get_execution_history(self) -> list:
        """Get all execution history"""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        return self.llm.get_metrics()
