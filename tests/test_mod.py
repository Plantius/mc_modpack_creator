import pytest
import json
from unittest.mock import patch, MagicMock
from mc_mp.modpack.mod import Mod, ProjectEncoder

# Sample data for testing
sample_mod_data = {
    "title": "Test Mod",
    "description": "A test mod",
    "name": "Test Mod 1.0.0",
    "changelog": "Test changelog",
    "version_number": "1.0.0",
    "dependencies": [{"id": "mod1", "version": "1.0"}],
    "mc_versions": ["1.19", "1.18"],
    "version_type": "release",
    "mod_loaders": ["fabric"],
    "id": "MODID123",
    "project_id": "PROJECTID123",
    "date_published": "2024-09-07",
    "files": [{"file_id": "file1", "url": "http://example.com/file1"}]
}

@pytest.fixture
def mod_instance():
    return Mod(**sample_mod_data)

def test_export_json(mod_instance):
    with patch('mc_mp.standard.get_variables') as mock_get_variables:
        mock_get_variables.return_value = sample_mod_data
        
        json_output = mod_instance.export_json()
        
        expected_output = sample_mod_data
        
        assert json.loads(json.dumps(expected_output)) == json_output
        mock_get_variables.assert_called_once_with(mod_instance)

def test_load_json(mod_instance):
    new_data = {
        "title": "Updated Mod",
        "description": "Updated description",
        "name": "Updated Mod 2.0.0",
        "changelog": "Updated changelog",
        "version_number": "2.0.0",
        "dependencies": [{"id": "mod2", "version": "2.0"}],
        "mc_versions": ["1.20"],
        "version_type": "beta",
        "mod_loaders": ["forge"],
        "id": "MODID456",
        "project_id": "PROJECTID456",
        "date_published": "2024-09-08",
        "files": [{"file_id": "file2", "url": "http://example.com/file2"}]
    }
    
    mod_instance.load_json(new_data)
    
    for key, value in new_data.items():
        assert getattr(mod_instance, key) == value

def test_update_self(mod_instance):
    latest_version = {
        "name": "Updated Mod 3.0.0",
        "changelog": "Updated changelog again",
        "version_number": "3.0.0",
        "dependencies": [{"id": "mod3", "version": "3.0"}],
        "game_versions": ["1.21"],
        "version_type": "alpha",
        "loaders": ["quilt"],
        "id": "MODID789",
        "project_id": "PROJECTID789",
        "date_published": "2024-09-09",
        "files": [{"file_id": "file3", "url": "http://example.com/file3"}]
    }

    project_info = {
        "title": "Updated Project Title",
        "description": "Updated Project Description"
    }

    mod_instance.update_self(latest_version, project_info)

    for key, value in latest_version.items():
        if key == "game_versions":
            key = "mc_versions"
        if hasattr(mod_instance, key):  # Check if attribute exists
            assert getattr(mod_instance, key) == value

    for key, value in project_info.items():
        if hasattr(mod_instance, key):  # Check if attribute exists
            assert getattr(mod_instance, key) == value


def test_project_encoder():
    mod_instance = Mod(**sample_mod_data)
    encoder = ProjectEncoder()
    
    json_output = json.dumps(mod_instance, cls=ProjectEncoder)
    expected_output = json.dumps(mod_instance.export_json())
    
    assert json.loads(json_output) == json.loads(expected_output)
