import json

from mcp.server.fastmcp import FastMCP

from figma_mcp.config import FIGMA_ACCESS_TOKEN
from figma_mcp.figma_client import FigmaClient
from figma_mcp.utils import logger, validate_file_key, validate_node_ids

mcp = FastMCP("figma-mcp")
client = FigmaClient(FIGMA_ACCESS_TOKEN)


@mcp.tool()
def get_figma_file(file_key: str) -> dict:
    """Get a complete Figma file by its key."""
    file_key = validate_file_key(file_key)
    logger.info(f"Getting file: {file_key}")
    return client.get_file(file_key)


@mcp.tool()
def get_frame_nodes(file_key: str, node_ids: list[str]) -> dict:
    """Get specific nodes/frames from a Figma file."""
    file_key = validate_file_key(file_key)
    node_ids = validate_node_ids(node_ids)
    logger.info(f"Getting nodes {node_ids} from file: {file_key}")
    return client.get_nodes(file_key, node_ids)


@mcp.tool()
def list_components(file_key: str) -> dict:
    """List all components in a Figma file."""
    file_key = validate_file_key(file_key)
    logger.info(f"Listing components for file: {file_key}")
    return client.get_components(file_key)


@mcp.tool()
def list_styles(file_key: str) -> dict:
    """List all styles in a Figma file."""
    file_key = validate_file_key(file_key)
    logger.info(f"Listing styles for file: {file_key}")
    return client.get_styles(file_key)


@mcp.tool()
def export_assets(
    file_key: str,
    node_ids: list[str],
    format: str = "png",
    scale: float = 2.0,
) -> dict:
    """Export nodes as images (PNG, JPG, SVG, PDF)."""
    file_key = validate_file_key(file_key)
    node_ids = validate_node_ids(node_ids)
    logger.info(f"Exporting {format} assets from file: {file_key}, nodes: {node_ids}")
    return client.get_images(file_key, node_ids, format=format, scale=scale)


def main():
    logger.info("Starting figma-mcp server")
    mcp.run()
