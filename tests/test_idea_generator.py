from idea_generator import Idea, IdeaGenerator

def test_filter_by_category():
    ideas = [
        Idea("Idea 1", "Category 1"),
        Idea("Idea 2", "Category 1"),
        Idea("Idea 3", "Category 2"),
        Idea("Idea 4", "Category 2"),
    ]

    generator = IdeaGenerator(ideas)
    filtered_ideas = generator.filter_by_category("Category 1")
    assert len(filtered_ideas) == 2
    for idea in filtered_ideas:
        assert idea.category == "Category 1"

def test_get_all_ideas():
    ideas = [
        Idea("Idea 1", "Category 1"),
        Idea("Idea 2", "Category 1"),
        Idea("Idea 3", "Category 2"),
        Idea("Idea 4", "Category 2"),
    ]

    generator = IdeaGenerator(ideas)
    all_ideas = generator.get_all_ideas()
    assert len(all_ideas) == 4

def test_filter_by_category_empty():
    ideas = [
        Idea("Idea 1", "Category 1"),
        Idea("Idea 2", "Category 1"),
        Idea("Idea 3", "Category 2"),
        Idea("Idea 4", "Category 2"),
    ]

    generator = IdeaGenerator(ideas)
    filtered_ideas = generator.filter_by_category("Category 3")
    assert len(filtered_ideas) == 0

def test_get_all_ideas_empty():
    generator = IdeaGenerator([])
    all_ideas = generator.get_all_ideas()
    assert len(all_ideas) == 0
