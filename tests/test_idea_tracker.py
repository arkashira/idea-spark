from idea_tracker import Idea, Product, IdeaTracker
import pytest
from datetime import datetime, timedelta

def test_add_idea():
    tracker = IdeaTracker()
    idea = Idea(1, 'Test Idea', datetime.now())
    tracker.add_idea(idea)
    assert idea.id in tracker.ideas

def test_add_product():
    tracker = IdeaTracker()
    product = Product(1, 1, datetime.now())
    tracker.add_product(product)
    assert product.id in tracker.products

def test_link_idea_to_product():
    tracker = IdeaTracker()
    idea = Idea(1, 'Test Idea', datetime.now())
    product = Product(1, 1, datetime.now())
    tracker.add_idea(idea)
    tracker.add_product(product)
    assert tracker.link_idea_to_product(1, 1)

def test_track_conversion_rate():
    tracker = IdeaTracker()
    idea1 = Idea(1, 'Test Idea 1', datetime.now())
    idea2 = Idea(2, 'Test Idea 2', datetime.now())
    product1 = Product(1, 1, datetime.now())
    tracker.add_idea(idea1)
    tracker.add_idea(idea2)
    tracker.add_product(product1)
    tracker.link_idea_to_product(1, 1)
    assert tracker.track_conversion_rate() == 0.5

def test_generate_nsm_report():
    tracker = IdeaTracker()
    idea1 = Idea(1, 'Test Idea 1', datetime.now())
    idea2 = Idea(2, 'Test Idea 2', datetime.now())
    product1 = Product(1, 1, datetime.now())
    tracker.add_idea(idea1)
    tracker.add_idea(idea2)
    tracker.add_product(product1)
    tracker.link_idea_to_product(1, 1)
    report = tracker.generate_nsm_report()
    assert report['conversion_rate'] == 0.5
    assert report['ideas'] == 2
    assert report['products'] == 1

def test_get_90_day_conversion_rate():
    tracker = IdeaTracker()
    idea1 = Idea(1, 'Test Idea 1', datetime.now())
    idea2 = Idea(2, 'Test Idea 2', datetime.now())
    product1 = Product(1, 1, datetime.now() - timedelta(days=60))
    tracker.add_idea(idea1)
    tracker.add_idea(idea2)
    tracker.add_product(product1)
    tracker.link_idea_to_product(1, 1)
    assert tracker.get_90_day_conversion_rate() == 0.5

def test_edge_case_no_ideas():
    tracker = IdeaTracker()
    assert tracker.track_conversion_rate() == 0

def test_edge_case_no_products():
    tracker = IdeaTracker()
    idea = Idea(1, 'Test Idea', datetime.now())
    tracker.add_idea(idea)
    assert tracker.track_conversion_rate() == 0
