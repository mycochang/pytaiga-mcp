from unittest.mock import MagicMock, patch

from src.server import update_epic, update_task


@patch("src.server.TaigaClientWrapper")
@patch("src.server._get_session_id")
@patch("src.server._get_authenticated_client")
def test_update_epic_subject(mock_get_client, mock_get_session, mock_wrapper_class):
    # Setup
    mock_get_session.return_value = "test_session"
    mock_client_instance = MagicMock()
    mock_get_client.return_value = mock_client_instance
    mock_client_instance.get_api.return_value = mock_client_instance.api

    # Mock get response (need version)
    mock_client_instance.api.epics.get.return_value = {
        "id": 789,
        "subject": "Old Epic Name",
        "version": 5,
    }

    # Mock update response
    mock_client_instance.api.epics.edit.return_value = {
        "id": 789,
        "subject": "New Epic Name",
        "version": 6,
    }

    # Execute
    result = update_epic(epic_id=789, kwargs='{"subject": "New Epic Name"}')

    # Verify
    assert result["subject"] == "New Epic Name"

    # Critical verification: Check if 'subject' was passed to the API
    call_args = mock_client_instance.api.epics.edit.call_args
    assert call_args.kwargs["subject"] == "New Epic Name"


@patch("src.server.TaigaClientWrapper")
@patch("src.server._get_session_id")
@patch("src.server._get_authenticated_client")
def test_update_task_subject(mock_get_client, mock_get_session, mock_wrapper_class):
    # Setup
    mock_get_session.return_value = "test_session"
    mock_client_instance = MagicMock()
    mock_get_client.return_value = mock_client_instance
    mock_client_instance.get_api.return_value = mock_client_instance.api

    # Mock get response
    mock_client_instance.api.tasks.get.return_value = {
        "id": 101,
        "subject": "Old Task Name",
        "version": 10,
    }

    # Mock update response
    mock_client_instance.api.tasks.edit.return_value = {
        "id": 101,
        "subject": "New Task Name",
        "version": 11,
    }

    # Execute
    result = update_task(task_id=101, kwargs='{"subject": "New Task Name"}')

    # Verify
    assert result["subject"] == "New Task Name"
    call_args = mock_client_instance.api.tasks.edit.call_args

    # Fix: Tasks.edit uses 'data' parameter, not **kwargs
    assert call_args.kwargs["data"]["subject"] == "New Task Name"
