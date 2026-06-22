import os
import tempfile

import pytest

from prompt_manager import PromptManager, PromptStorage, generate_idea


@pytest.fixture
def temp_storage():
    """Create a temporary JSON file for PromptStorage."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)  # close the descriptor; PromptStorage will open it later
    try:
        storage = PromptStorage(path)
        yield storage
    finally:
        if os.path.exists(path):
            os.remove(path)


@pytest.fixture
def manager(temp_storage):
    return PromptManager(temp_storage)


def test_add_prompt_happy(manager):
    user = "user1"
    manager.add_prompt(user, "greeting", "Say hello to {{seed}}")
    assert "greeting" in manager.list_prompts(user)
    assert manager.get_prompt(user, "greeting") == "Say hello to {{seed}}"


def test_add_prompt_duplicate_raises(manager):
    user = "user2"
    manager.add_prompt(user, "dup", "First")
    with pytest.raises(ValueError, match="already exists"):
        manager.add_prompt(user, "dup", "Second")


def test_add_prompt_token_limit(manager):
    user = "user3"
    long_template = "word " * 501  # 501 tokens
    with pytest.raises(ValueError, match="exceeds 500 token"):
        manager.add_prompt(user, "too_long", long_template)


def test_edit_prompt_happy(manager):
    user = "user4"
    manager.add_prompt(user, "edit_me", "Old template")
    manager.edit_prompt(user, "edit_me", "New template with {{seed}}")
    assert manager.get_prompt(user, "edit_me") == "New template with {{seed}}"


def test_edit_prompt_nonexistent_raises(manager):
    user = "user5"
    with pytest.raises(ValueError, match="does not exist"):
        manager.edit_prompt(user, "missing", "Anything")


def test_generate_idea_uses_template(manager):
    user = "user6"
    manager.add_prompt(user, "idea", "Create a slogan for {{seed}}")
    result = generate_idea(user, "idea", manager, seed="solar charger")
    assert result == "Idea: Create a slogan for solar charger"


def test_generate_idea_after_edit(manager):
    user = "user7"
    manager.add_prompt(user, "dynamic", "Version 1 for {{seed}}")
    first = generate_idea(user, "dynamic", manager, seed="X")
    manager.edit_prompt(user, "dynamic", "Version 2 for {{seed}}")
    second = generate_idea(user, "dynamic", manager, seed="X")
    assert "Version 1" in first
    assert "Version 2" in second


def test_generate_idea_missing_prompt(manager):
    user = "user8"
    with pytest.raises(ValueError, match="not found"):
        generate_idea(user, "nonexistent", manager)


def test_list_prompts_multiple(manager):
    user = "user9"
    manager.add_prompt(user, "first", "A")
    manager.add_prompt(user, "second", "B")
    names = manager.list_prompts(user)
    assert set(names) == {"first", "second"}
