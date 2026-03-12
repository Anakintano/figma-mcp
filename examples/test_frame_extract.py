"""Example script to extract specific frames/nodes from a Figma file."""

import argparse
import json
import sys

sys.path.insert(0, "src")

from figma_mcp.config import FIGMA_ACCESS_TOKEN
from figma_mcp.figma_client import FigmaClient


def main():
    parser = argparse.ArgumentParser(description="Extract nodes from a Figma file")
    parser.add_argument("--file-key", required=True, help="Figma file key")
    parser.add_argument("--node-ids", required=True, nargs="+", help="Node IDs to extract")
    args = parser.parse_args()

    client = FigmaClient(FIGMA_ACCESS_TOKEN)
    result = client.get_nodes(args.file_key, args.node_ids)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
