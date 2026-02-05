from unittest.mock import MagicMock, patch

from src.server import create_wiki_page


@patch("src.server.TaigaClientWrapper")
@patch("src.server._get_session_id")
@patch("src.server._get_authenticated_client")
def test_create_wiki_page(mock_get_client, mock_get_session, mock_wrapper_class):
    # Setup
    mock_get_session.return_value = "test_session"
    mock_client_instance = MagicMock()
    mock_get_client.return_value = mock_client_instance
    mock_client_instance.get_api.return_value = mock_client_instance.api

    # Mock create response
    mock_client_instance.api.wiki.create.return_value = {
        "id": 555,
        "slug": "home",
        "content": "Welcome to the wiki",
        "project": 123,
        "version": 1,
    }

    # Execute
    result = create_wiki_page(project_id=123, slug="home", content="Welcome to the wiki")

    # Verify
    assert result["slug"] == "home"
    assert result["content"] == "Welcome to the wiki"

    # Verify call args
    mock_client_instance.api.wiki.create.assert_called_once()
    call_args = mock_client_instance.api.wiki.create.call_args
    assert call_args.kwargs["project"] == 123
    assert call_args.kwargs["slug"] == "home"
    assert call_args.kwargs["content"] == "Welcome to the wiki"
