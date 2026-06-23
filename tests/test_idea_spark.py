from idea_spark import IdeaSpark, Idea, load_ideas_from_json
import pytest

@pytest.fixture
def ideas():
    data = '''
    [
        {"niche": "tech", "description": "Build a new app"},
        {"niche": "tech", "description": "Create a website"},
        {"niche": "art", "description": "Paint a picture"},
        {"niche": "music", "description": "Compose a song"}
    ]
    '''
    return load_ideas_from_json(data)

def test_filter_by_niche(ideas):
    idea_spark = IdeaSpark(ideas)
    filtered_ideas = idea_spark.filter_by_niche("tech")
    assert len(filtered_ideas) == 2
    assert all(idea.niche == "tech" for idea in filtered_ideas)

def test_get_niche_categories(ideas):
    idea_spark = IdeaSpark(ideas)
    niche_categories = idea_spark.get_niche_categories()
    assert len(niche_categories) == 3
    assert "tech" in niche_categories
    assert "art" in niche_categories
    assert "music" in niche_categories

def test_filter_by_niche_empty(ideas):
    idea_spark = IdeaSpark(ideas)
    filtered_ideas = idea_spark.filter_by_niche("non-existent")
    assert len(filtered_ideas) == 0

def test_load_ideas_from_json():
    data = '''
    [
        {"niche": "tech", "description": "Build a new app"}
    ]
    '''
    ideas = load_ideas_from_json(data)
    assert len(ideas) == 1
    assert ideas[0].niche == "tech"
    assert ideas[0].description == "Build a new app"
