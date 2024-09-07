import unittest
from mc_mp.modpack.modpack import Modpack
from mc_mp.modpack.mod import Mod

class TestModpack(unittest.TestCase):

    def setUp(self):
        """Set up a basic Modpack instance for testing."""
        self.modpack = Modpack(title="Test Modpack")

    def test_export_json(self):
        """Test export_json method to ensure it outputs correct data."""
        result = self.modpack.export_json()
        self.assertIn("title", result)
        self.assertEqual(result["title"], "Test Modpack")

    def test_check_compatibility(self):
        """Test the compatibility check of the modpack for duplicate mods."""
        self.modpack.mod_data = [
            Mod(project_id="mod1"), Mod(project_id="mod2")
        ]
        self.assertTrue(self.modpack.check_compatibility())

        # Introduce duplicate project_id
        self.modpack.mod_data.append(Mod(project_id="mod1"))
        self.assertFalse(self.modpack.check_compatibility())

    def test_get_mods_name_ver(self):
        """Test retrieval of mod names and version numbers."""
        self.modpack.mod_data = [
            Mod(title="Mod1", version_number="1.0"),
            Mod(title="Mod2", version_number="2.0")
        ]
        result = self.modpack.get_mods_name_ver()
        self.assertEqual(result, ["Mod1 - 1.0", "Mod2 - 2.0"])

    def test_sort_mods(self):
        """Test sorting of mods by project ID."""
        self.modpack.mod_data = [
            Mod(project_id="B"), Mod(project_id="A"), Mod(project_id="C")
        ]
        self.modpack.sort_mods()
        self.assertEqual([mod.project_id for mod in self.modpack.mod_data], ["A", "B", "C"])

if __name__ == '__main__':
    unittest.main()