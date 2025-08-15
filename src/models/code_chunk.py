"""Data models for code chunks"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import numpy as np


@dataclass
class CodeChunk:
    """Represents a chunk of code or documentation"""
    
    id: str
    content: str
    file_path: str
    language: str
    start_line: int
    end_line: int
    metadata: Dict = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "content": self.content,
            "file_path": self.file_path,
            "language": self.language,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CodeChunk':
        """Create instance from dictionary"""
        return cls(
            id=data["id"],
            content=data["content"],
            file_path=data["file_path"],
            language=data["language"],
            start_line=data["start_line"],
            end_line=data["end_line"],
            metadata=data.get("metadata", {})
        )