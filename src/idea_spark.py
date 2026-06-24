import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

@dataclass
class Idea:
    title: str
    value_proposition: str
    validation_score: int

class IdeaSpark:
    def __init__(self):
        self.interests_to_ideas = {}
        self.id_to_idea = {}

    def generate_ideas(self, user_id, interests):
        if len(interests) > 200:
            raise ValueError("Interests cannot be longer than 200 characters")
        
        if user_id not in self.interests_to_ideas:
            self.interests_to_ideas[user_id] = []
        if len(self.interests_to_ideas[user_id]) >= 3:
            self.interests_to_ideas[user_id] = self.interests_to_ideas[user_id][-3:]
        ideas = []
        for _ in range(3):
            title = f"Idea {random.randint(1, 100)} for {interests}"
            value_proposition = f"This idea is related to {interests} and has a validation score of {random.randint(1, 100)}"
            validation_score = random.randint(1, 100)
            idea = Idea(title, value_proposition, validation_score)
            ideas.append(idea)
            self.id_to_idea[len(self.id_to_idea) + 1] = idea
        self.interests_to_ideas[user_id].extend(ideas)
        return ideas

    def get_ideas(self, user_id):
        if user_id not in self.interests_to_ideas:
            return []
        return self.interests_to_ideas[user_id]

def main():
    idea_spark = IdeaSpark()
    user_id = 1
    interests = "AI and machine learning"
    ideas = idea_spark.generate_ideas(user_id, interests)
    print(json.dumps([{"title": idea.title, "value_proposition": idea.value_proposition, "validation_score": idea.validation_score} for idea in ideas]))

if __name__ == "__main__":
    main()
