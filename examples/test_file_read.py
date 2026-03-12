"""Example script to read a Figma file."""

import argparse
import json
import sys

sys.path.insert(0, "src")

from figma_mcp.config import FIGMA_ACCESS_TOKEN
from figma_mcp.figma_client import FigmaClient


def main():
    parser = argparse.ArgumentParser(description="Read a Figma file")
    parser.add_argument("--file-key", required=True, help="Figma file key")
    args = parser.parse_args()

    client = FigmaClient(FIGMA_ACCESS_TOKEN)
    result = client.get_file(args.file_key)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
