from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Model:
    title: str
    description: str
    sizes: List[str]
    capabilities: List[str]
    pulls: str
    tags: str
    updated: str

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "sizes": self.sizes,
            "capabilities": self.capabilities,
            "pulls": self.pulls,
            "tags": self.tags,
            "updated": self.updated,
        }
