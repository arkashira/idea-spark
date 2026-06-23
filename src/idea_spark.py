import json
from dataclasses import dataclass
from typing import List

@dataclass
class Idea:
    niche: str
    description: str

class IdeaSpark:
    def __init__(self, ideas: List[Idea]):
        self.ideas = ideas

    def filter_by_niche(self, niche: str) -> List[Idea]:
        return [idea for idea in self.ideas if idea.niche == niche]

    def get_niche_categories(self) -> List[str]:
        return list(set(idea.niche for idea in self.ideas))

def load_ideas_from_json(data: str) -> List[Idea]:
    ideas = json.loads(data)
    return [Idea(idea['niche'], idea['description']) for idea in ideas]
