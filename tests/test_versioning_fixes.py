from unittest.mock import MagicMock, patch

from src.server import update_milestone, update_project


@patch("src.server.TaigaClientWrapper")
@patch("src.server._get_session_id")
@patch("src.server._get_authenticated_client")
def test_update_project_missing_version(mock_get_client, mock_get_session, mock_wrapper_class):
    # Setup
    mock_get_session.return_value = "test_session"
    mock_client_instance = MagicMock()
    mock_get_client.return_value = mock_client_instance
    mock_client_instance.get_api.return_value = mock_client_instance.api

    # Mock get_project response to NOT have a version
    mock_client_instance.api.projects.get.return_value = {
        "id": 123,
        "name": "Test Project",
        # No "version" key
    }

    # Mock update response
    mock_client_instance.api.projects.update.return_value = {
        "id": 123,
        "name": "Updated Name",
        "version": 2,
    }

    # Execute
    result = update_project(project_id=123, kwargs='{"name": "Updated Name"}')

    # Verify
    assert result["name"] == "Updated Name"
    # Verify update was called with version=None
    call_args = mock_client_instance.api.projects.update.call_args
    assert call_args.kwargs["version"] is None


@patch("src.server.TaigaClientWrapper")
@patch("src.server._get_session_id")
@patch("src.server._get_authenticated_client")
def test_update_milestone_missing_version(mock_get_client, mock_get_session, mock_wrapper_class):
    # Setup
    mock_get_session.return_value = "test_session"
    mock_client_instance = MagicMock()
    mock_get_client.return_value = mock_client_instance
    mock_client_instance.get_api.return_value = mock_client_instance.api

    # Mock get_milestone response to NOT have a version
    mock_client_instance.api.milestones.get.return_value = {
        "id": 456,
        "name": "Test Milestone",
        # No "version" key
    }

    # Mock update response
    mock_client_instance.api.milestones.edit.return_value = {
        "id": 456,
        "name": "Updated Milestone",
        "version": 2,
    }

    # Execute - Should fail if not fixed
    result = update_milestone(milestone_id=456, kwargs='{"name": "Updated Milestone"}')

    # Verify
    assert result["name"] == "Updated Milestone"
    # Verify edit was called with version=None
    call_args = mock_client_instance.api.milestones.edit.call_args
    assert call_args.kwargs["version"] is None
