import json
import os
from typing import Dict, List


class PromptStorage:
    """
    Simple JSON‑file based storage for user prompts.
    The file format is:
    {
        "user_id": {
            "prompt_name": "template text",
            ...
        },
        ...
    }
    """

    def __init__(self, path: str = "prompts.json"):
        self.path = path
        self._data: Dict[str, Dict[str, str]] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get_user_prompts(self, user_id: str) -> Dict[str, str]:
        """Return the mutable dict of prompts for a user."""
        return self._data.setdefault(user_id, {})

    def save_user_prompts(self, user_id: str, prompts: Dict[str, str]) -> None:
        """Persist the given prompts for a user."""
        self._data[user_id] = prompts
        self._save()


class PromptManager:
    """
    Business logic for creating, editing and retrieving prompts.
    Enforces a 500‑token limit (tokens = whitespace‑separated words).
    """

    MAX_TOKENS = 500

    def __init__(self, storage: PromptStorage):
        self.storage = storage

    @staticmethod
    def _token_count(text: str) -> int:
        """Count tokens as whitespace‑separated words."""
        return len(text.split())

    def add_prompt(self, user_id: str, name: str, template: str) -> None:
        """Add a new prompt for a user."""
        if self._token_count(template) > self.MAX_TOKENS:
            raise ValueError("Prompt exceeds 500 token limit")
        prompts = self.storage.get_user_prompts(user_id)
        if name in prompts:
            raise ValueError(f"Prompt '{name}' already exists")
        prompts[name] = template
        self.storage.save_user_prompts(user_id, prompts)

    def edit_prompt(self, user_id: str, name: str, new_template: str) -> None:
        """Edit an existing prompt."""
        if self._token_count(new_template) > self.MAX_TOKENS:
            raise ValueError("Prompt exceeds 500 token limit")
        prompts = self.storage.get_user_prompts(user_id)
        if name not in prompts:
            raise ValueError(f"Prompt '{name}' does not exist")
        prompts[name] = new_template
        self.storage.save_user_prompts(user_id, prompts)

    def get_prompt(self, user_id: str, name: str) -> str:
        """Retrieve a prompt template; returns None if missing."""
        prompts = self.storage.get_user_prompts(user_id)
        return prompts.get(name)

    def list_prompts(self, user_id: str) -> List[str]:
        """Return a list of prompt names for UI dropdowns."""
        prompts = self.storage.get_user_prompts(user_id)
        return list(prompts.keys())


def generate_idea(user_id: str, prompt_name: str, manager: PromptManager, seed: str = "") -> str:
    """
    Very simple idea generator that substitutes a `{{seed}}` placeholder
    in the selected prompt template.
    """
    template = manager.get_prompt(user_id, prompt_name)
    if template is None:
        raise ValueError(f"Prompt '{prompt_name}' not found for user '{user_id}'")
    result = template.replace("{{seed}}", seed)
    return f"Idea: {result}"
