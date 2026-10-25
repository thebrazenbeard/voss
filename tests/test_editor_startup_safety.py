"""Static regression checks; never execute disguised startup content."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EditorStartupSafetyTests(unittest.TestCase):
    def test_tasks_configuration_is_parseable(self):
        data = json.loads((ROOT / ".vscode" / "tasks.json").read_text(encoding="utf-8"))
        self.assertIsInstance(data.get("tasks"), list)

    def test_no_implicit_folder_open_execution(self):
        tasks = (ROOT / ".vscode" / "tasks.json").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r'"runOn"\s*:\s*"folderOpen"', tasks))
        self.assertIsNone(re.search(r"\bnode\s+[^\n]*public/fonts/", tasks))

    def test_automatic_tasks_disabled(self):
        settings = json.loads((ROOT / ".vscode" / "settings.json").read_text(encoding="utf-8"))
        self.assertIs(settings.get("task.allowAutomaticTasks"), False)
        self.assertNotIn("tasks", settings)

    def test_disguised_script_absent(self):
        self.assertFalse((ROOT / "public/fonts/fa-solid.lkf").exists())


if __name__ == "__main__":
    unittest.main()
