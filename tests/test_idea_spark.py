import pytest
from idea_spark import IdeaSpark, Idea

def test_generate_ideas():
    idea_spark = IdeaSpark()
    user_id = 1
    interests = "AI and machine learning"
    ideas = idea_spark.generate_ideas(user_id, interests)
    assert len(ideas) == 3
    for idea in ideas:
        assert isinstance(idea, Idea)
        assert idea.title
        assert idea.value_proposition
        assert 0 <= idea.validation_score <= 100

def test_get_ideas():
    idea_spark = IdeaSpark()
    user_id = 1
    interests = "AI and machine learning"
    ideas = idea_spark.generate_ideas(user_id, interests)
    retrieved_ideas = idea_spark.get_ideas(user_id)
    assert len(retrieved_ideas) == 3
    for idea in retrieved_ideas:
        assert isinstance(idea, Idea)
        assert idea.title
        assert idea.value_proposition
        assert 0 <= idea.validation_score <= 100

def test_unique_ideas():
    idea_spark = IdeaSpark()
    user_id = 1
    interests = "AI and machine learning"
    ideas1 = idea_spark.generate_ideas(user_id, interests)
    ideas2 = idea_spark.generate_ideas(user_id, interests)
    assert len(ideas1) == 3
    assert len(ideas2) == 3
    for idea1, idea2 in zip(ideas1, ideas2):
        assert idea1.title != idea2.title
        assert idea1.value_proposition != idea2.value_proposition
        assert idea1.validation_score != idea2.validation_score

def test_edge_case_empty_interests():
    idea_spark = IdeaSpark()
    user_id = 1
    interests = ""
    ideas = idea_spark.generate_ideas(user_id, interests)
    assert len(ideas) == 3
    for idea in ideas:
        assert isinstance(idea, Idea)
        assert idea.title
        assert idea.value_proposition
        assert 0 <= idea.validation_score <= 100

def test_edge_case_long_interests():
    idea_spark = IdeaSpark()
    user_id = 1
    interests = "a" * 201
    with pytest.raises(ValueError):
        idea_spark.generate_ideas(user_id, interests)
