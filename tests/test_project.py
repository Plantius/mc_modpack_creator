import unittest
import asyncio
from mc_mp.modpack.project import Project, Modpack
from unittest.mock import patch, MagicMock
from unittest import TestCase, mock

class TestProject(TestCase):

    def setUp(self):
        """Setup a basic Project instance for testing."""
        self.project = Project()
        self.project.modpack = MagicMock(spec=Modpack)

    def test_is_mod_installed(self):
        """Test mod installation check by ID."""
        self.project.modpack.mod_data = [MagicMock(project_id='mod1'), MagicMock(project_id='mod2')]
        result = self.project.is_mod_installed('mod1')
        self.assertEqual(result, 0)  # Should find at index 0

    def test_is_date_newer(self):
        """Test date comparison for newer mod."""
        new_date = "2024-09-06"
        current_date = "2023-09-06"
        self.assertTrue(self.project.is_date_newer(new_date, current_date))

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', unittest.mock.mock_open(read_data='{"metadata": {"project_id": "123"}}'))
    @patch('json.load', return_value={'metadata': {'project_id': '123'}})
    def test_load_project_success(self, mock_json, mock_open, mock_exists):
        """Test loading a project from a valid file."""
        self.project.modpack = MagicMock()
        result = asyncio.run(self.project.load_project('valid.modpack'))
        self.assertTrue(result)
        self.assertTrue(self.project.metadata["loaded"])

    def test_add_mod_success(self):
        """Test adding a mod successfully to the modpack."""
        self.project.modpack.mod_data = []
        mod_info = {"title": "Mod1", "description": "Test Mod"}
        version_info = {"name": "Mod1.0", "changelog": "Changes", "version_number": "1.0.0", "dependencies": [], "game_versions": ["1.19"], "loaders": ["fabric"], "id": "id1", "project_id": "proj1", "date_published": "2024-09-06", "files": []}
        result = self.project.add_mod("Mod1", version_info, mod_info)
        self.assertTrue(result)

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_save_project_success(self, mock_open):
        """Test saving a project successfully to a file."""
        self.project.metadata = {"filename": "test_project"}
        self.project.modpack = MagicMock()
        self.project.modpack.export_json.return_value = {}
        result = asyncio.run(self.project.save_project())
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
