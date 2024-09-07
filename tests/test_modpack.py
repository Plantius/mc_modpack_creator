import pytest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
from mc_mp.modpack.modpack import Modpack
from mc_mp.modpack.mod import Mod, ProjectEncoder
import mc_mp.standard as std

@pytest.fixture
def modpack_instance():
    return Modpack(
        title="Test Modpack",
        description="A test modpack",
        build_date="2024-09-07",
        build_version="1.0",
        mc_version="1.20",
        mod_loader="forge",
        client_side="optional",
        server_side="required",
        mod_data=[
            {"title": "Mod1", "version_number": "1.0.0", "project_id": "id1", "description": "Description of Mod1"},
            {"title": "Mod2", "version_number": "2.0.0", "project_id": "id2", "description": "Description of Mod2"}
        ]
    )
    
def test_initialization(modpack_instance):
    assert modpack_instance.title == "Test Modpack"
    assert modpack_instance.description == "A test modpack"
    assert modpack_instance.build_date == "2024-09-07"
    assert modpack_instance.build_version == "1.0"
    assert modpack_instance.mc_version == "1.20"
    assert modpack_instance.mod_loader == "forge"
    assert modpack_instance.client_side == "optional"
    assert modpack_instance.server_side == "required"
    assert len(modpack_instance.mod_data) == 2
    assert isinstance(modpack_instance.mod_data[0], Mod)

def test_export_json(modpack_instance):
    with patch('mc_mp.standard.get_variables') as mock_get_variables:
        mock_get_variables.return_value = {"title": "Test Modpack", "description": "A test modpack"}
        
        # Call the method under test
        json_output = modpack_instance.export_json()
        
        # Define the expected output
        expected_output = {
            "title": "Test Modpack",
            "description": "A test modpack"
        }
        
        # Ensure the JSON output matches the expected output
        assert json.loads(json.dumps(expected_output)) == json_output
        
        # Debug: Print the actual call args for inspection
        print(f"Actual call args: {mock_get_variables.call_args}")
        
        # Assert the function was called with the correct arguments (if cls is not used, remove it)
        mock_get_variables.assert_called_once_with(modpack_instance)
        

def test_check_compatibility(modpack_instance):
    assert modpack_instance.check_compatibility() is True

def test_check_compatibility_with_duplicates():
    modpack_instance = Modpack(
        mod_data=[
            {"title": "Mod1", "version_number": "1.0.0", "project_id": "id1", "description": "Description of Mod1"},
            {"title": "Mod2", "version_number": "2.0.0", "project_id": "id1", "description": "Description of Mod2"}
        ]
    )
    assert modpack_instance.check_compatibility() is False

def test_get_mods_name_ver(modpack_instance):
    expected_mods = ["Mod1 - 1.0.0", "Mod2 - 2.0.0"]
    assert modpack_instance.get_mods_name_ver() == expected_mods

def test_get_mods_descriptions(modpack_instance):
    expected_descriptions = ["Description of Mod1", "Description of Mod2"]
    assert modpack_instance.get_mods_descriptions() == expected_descriptions

def test_sort_mods(modpack_instance):
    modpack_instance.sort_mods()
    sorted_mods = [mod.title for mod in modpack_instance.mod_data]
    assert sorted_mods == ["Mod1", "Mod2"]

def test_mod_data_empty_mods():
    modpack_instance = Modpack(mod_data=[])
    assert modpack_instance.get_mods_name_ver() == []
    assert modpack_instance.get_mods_descriptions() == []
    assert modpack_instance.check_compatibility() is True
