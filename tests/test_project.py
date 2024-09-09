import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from mc_mp.modpack.project import Project

class TestProjectSQLite(unittest.TestCase):

    def setUp(self):
        # In-memory SQLite DB for testing
        self.project = Project(db_file=":memory:")
        self.project.create_tables()

    def test_create_project(self):
        # Test creating a project in SQLite
        result = self.project.create_project(title="Test Modpack", description="Test Description")
        self.assertTrue(result, "Failed to create project")

        # Save project
        result = self.project.save_project(filename="test_file")
        # Verify data in the database
        cursor = self.project.conn.cursor()
        cursor.execute("SELECT * FROM Project WHERE title=?", ("Test Modpack",))
        project = cursor.fetchone()
        self.assertIsNotNone(project, "Project should be created in the database")
        self.assertEqual(project[2], "Test Modpack", "Project title should match")
        self.assertEqual(project[3], "Test Description", "Project description should match")

    def test_add_mod(self):
        # First, create a project to add a mod to
        self.project.create_project(title="Test Modpack")
        
        # Add a mod
        mod_info = {"name": "Test Mod", "version_number": "1.0", "title": "Test Mod Title"}
        project_info = {"title": "Test Mod Title", "description": "Mod Description"}
        self.project.add_mod(name="Test Mod", version=mod_info, project_info=project_info)

        # Verify the mod is in the database
        cursor = self.project.conn.cursor()
        cursor.execute("SELECT * FROM Mod WHERE name=?", ("Test Mod",))
        mod = cursor.fetchone()

        self.assertIsNotNone(mod, "Mod should be added to the database")
        self.assertEqual(mod[4], "Test Mod", "Mod name should match")

    def tearDown(self):
        # Clean up the in-memory database
        self.project.conn.close()

if __name__ == '__main__':
    unittest.main()
