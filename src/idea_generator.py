from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Idea:
    name: str
    category: str

class IdeaGenerator:
    def __init__(self, ideas: List[Idea]):
        self.ideas = ideas

    def filter_by_category(self, category: str) -> List[Idea]:
        return [idea for idea in self.ideas if idea.category == category]

    def get_all_ideas(self) -> List[Idea]:
        return self.ideas

def main():
    ideas = [
        Idea("Idea 1", "Category 1"),
        Idea("Idea 2", "Category 1"),
        Idea("Idea 3", "Category 2"),
        Idea("Idea 4", "Category 2"),
    ]

    generator = IdeaGenerator(ideas)
    print("All Ideas:")
    for idea in generator.get_all_ideas():
        print(f"{idea.name} - {idea.category}")

    category = "Category 1"
    print(f"\nIdeas in {category}:")
    for idea in generator.filter_by_category(category):
        print(f"{idea.name} - {idea.category}")

if __name__ == "__main__":
    main()
