import pytest
from unittest.mock import patch, AsyncMock
from mc_mp.modpack.project_api import ProjectAPI

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ClientSession')
async def test_request_fail(mock_client_session):
    mock_client = mock_client_session.return_value
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = Exception("Request failed")
    
    mock_client.__aenter__.return_value = mock_session
    mock_client.__aexit__.return_value = False
    mock_session.get.return_value = mock_response
    
    result = await ProjectAPI.request('/test-endpoint')
    assert result is None

def test_parse_url():
    params = {'key1': 'value1', 'key2': 'value2'}
    result = ProjectAPI.parse_url(params)
    assert result == 'key1=value1&key2=value2'

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_is_slug_valid(mock_request):
    mock_request.return_value = {'exists': True}
    result = await ProjectAPI.is_slug_valid('valid-slug')
    assert result == {'exists': True}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_is_slug_valid_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.is_slug_valid('invalid-slug')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_dependencies(mock_request):
    mock_request.return_value = {'dependencies': ['dep1', 'dep2']}
    result = await ProjectAPI.get_dependencies('project-name')
    assert result == {'dependencies': ['dep1', 'dep2']}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_dependencies_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.get_dependencies('project-name')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_search_project(mock_request):
    mock_request.return_value = {'results': ['proj1', 'proj2']}
    result = await ProjectAPI.search_project(param1='value1')
    assert result == {'results': ['proj1', 'proj2']}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_search_project_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.search_project(param1='value1')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_project(mock_request):
    mock_request.return_value = {'project': 'details'}
    result = await ProjectAPI.get_project('project-name')
    assert result == {'project': 'details'}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_project_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.get_project('project-name')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_projects(mock_request):
    mock_request.return_value = {'projects': ['proj1', 'proj2']}
    result = await ProjectAPI.get_projects(param1='value1')
    assert result == {'projects': ['proj1', 'proj2']}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_projects_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.get_projects(ids='value1')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_list_versions(mock_request):
    mock_request.return_value = {'versions': ['v1', 'v2']}
    result = await ProjectAPI.list_versions(id='project-id')
    assert result == {'versions': ['v1', 'v2']}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_list_versions_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.list_versions(id='project-id')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_version(mock_request):
    mock_request.return_value = {'version': 'details'}
    result = await ProjectAPI.get_version('version-id')
    assert result == {'version': 'details'}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_version_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.get_version('version-id')
    assert result is None

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_versions(mock_request):
    mock_request.return_value = {'versions': ['v1', 'v2']}
    result = await ProjectAPI.get_versions(id='project-id')
    assert result == {'versions': ['v1', 'v2']}

@pytest.mark.asyncio
@patch('mc_mp.modpack.project_api.ProjectAPI.request')
async def test_get_versions_fail(mock_request):
    mock_request.side_effect = Exception("Request failed")
    result = await ProjectAPI.get_versions(id='project-id')
    assert result is None