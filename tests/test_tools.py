"""Tests for figma-mcp tool functions."""

import asyncio
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "src")

# Patch config before importing tools so it doesn't raise on missing token
with patch.dict("os.environ", {"FIGMA_ACCESS_TOKEN": "test-token"}):
    from figma_mcp.figma_client import FigmaClient
    from figma_mcp.tools.get_file import get_figma_file
    from figma_mcp.tools.get_nodes import get_frame_nodes
    from figma_mcp.tools.get_components import list_components
    from figma_mcp.tools.get_styles import list_styles
    from figma_mcp.tools.export_images import export_assets
    from figma_mcp.utils import validate_file_key, validate_node_ids


@pytest.fixture
def mock_client():
    client = MagicMock(spec=FigmaClient)
    return client


class TestValidation:
    def test_validate_file_key_valid(self):
        assert validate_file_key("abc123") == "abc123"

    def test_validate_file_key_empty(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_file_key("")

    def test_validate_file_key_invalid(self):
        with pytest.raises(ValueError, match="Invalid file_key"):
            validate_file_key("bad key!")

    def test_validate_node_ids_valid(self):
        assert validate_node_ids(["1:2", "3:4"]) == ["1:2", "3:4"]

    def test_validate_node_ids_empty(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_node_ids([])


class TestGetFile:
    def test_get_file(self, mock_client):
        mock_client.get_file.return_value = {"name": "Test File", "document": {}}
        result = asyncio.run(get_figma_file(mock_client, "abc123"))
        assert result["name"] == "Test File"
        mock_client.get_file.assert_called_once_with("abc123")


class TestGetNodes:
    def test_get_nodes(self, mock_client):
        mock_client.get_nodes.return_value = {"nodes": {"1:2": {"document": {}}}}
        result = asyncio.run(get_frame_nodes(mock_client, "abc123", ["1:2"]))
        assert "nodes" in result
        mock_client.get_nodes.assert_called_once_with("abc123", ["1:2"])


class TestListComponents:
    def test_list_components(self, mock_client):
        mock_client.get_components.return_value = {"meta": {"components": []}}
        result = asyncio.run(list_components(mock_client, "abc123"))
        assert "meta" in result


class TestListStyles:
    def test_list_styles(self, mock_client):
        mock_client.get_styles.return_value = {"meta": {"styles": []}}
        result = asyncio.run(list_styles(mock_client, "abc123"))
        assert "meta" in result


class TestExportAssets:
    def test_export_assets(self, mock_client):
        mock_client.get_images.return_value = {"images": {"1:2": "https://example.com/img.png"}}
        result = asyncio.run(export_assets(mock_client, "abc123", ["1:2"], "png", 2.0))
        assert "images" in result
        mock_client.get_images.assert_called_once_with("abc123", ["1:2"], format="png", scale=2.0)

    def test_export_assets_svg(self, mock_client):
        mock_client.get_images.return_value = {"images": {}}
        result = asyncio.run(export_assets(mock_client, "abc123", ["1:2"], "svg", 1.0))
        mock_client.get_images.assert_called_once_with("abc123", ["1:2"], format="svg", scale=1.0)
