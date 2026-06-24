import json
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Idea:
    id: int
    name: str
    created_at: datetime
    product_id: int = None

@dataclass
class Product:
    id: int
    idea_id: int
    launched_at: datetime

class IdeaTracker:
    def __init__(self):
        self.ideas = {}
        self.products = {}

    def add_idea(self, idea):
        self.ideas[idea.id] = idea

    def add_product(self, product):
        self.products[product.id] = product

    def link_idea_to_product(self, idea_id, product_id):
        if idea_id in self.ideas and product_id in self.products:
            self.ideas[idea_id].product_id = product_id
            return True
        return False

    def track_conversion_rate(self):
        if not self.ideas:
            return 0
        launched_ideas = [idea for idea in self.ideas.values() if idea.product_id is not None]
        conversion_rate = len(launched_ideas) / len(self.ideas)
        return conversion_rate

    def generate_nsm_report(self):
        report = {
            'conversion_rate': self.track_conversion_rate(),
            'ideas': len(self.ideas),
            'products': len(self.products)
        }
        return report

    def get_90_day_conversion_rate(self):
        if not self.ideas:
            return 0
        launched_ideas = [idea for idea in self.ideas.values() if idea.product_id is not None and (datetime.now() - self.products[idea.product_id].launched_at).days <= 90]
        conversion_rate = len(launched_ideas) / len(self.ideas)
        return conversion_rate
