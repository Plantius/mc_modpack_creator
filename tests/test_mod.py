import unittest
from mc_mp.modpack.mod import Mod

class TestMod(unittest.TestCase):

    def test_export_json(self):
        """Test the export_json method to ensure it outputs correct data."""
        mod = Mod(title="Test Mod", version_number="1.0")
        result = mod.export_json()
        self.assertIn("title", result)
        self.assertEqual(result["title"], "Test Mod")

    def test_load_json(self):
        """Test the load_json method to ensure data is correctly loaded."""
        mod = Mod()
        json_data = {"title": "Loaded Mod", "version_number": "2.0"}
        mod.load_json(json_data)
        self.assertEqual(mod.title, "Loaded Mod")
        self.assertEqual(mod.version_number, "2.0")

    def test_update_self(self):
        """Test updating the mod with new version and project information."""
        mod = Mod(title="Old Mod", version_number="1.0")
        latest_version = {
            "name": "New Mod", "version_number": "2.0", "changelog": "Updated",
            "dependencies": [], "game_versions": ["1.19"], "loaders": ["fabric"],
            "id": "XYZ123", "project_id": "ABCD1234", "date_published": "2024-09-06",
            "files": []
        }
        project_info = {"title": "Updated Mod", "description": "New description"}
        mod.update_self(latest_version, project_info)

        self.assertEqual(mod.title, "Updated Mod")
        self.assertEqual(mod.version_number, "2.0")
        self.assertEqual(mod.changelog, "Updated")

if __name__ == '__main__':
    unittest.main()
