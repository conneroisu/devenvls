import re
from typing import Dict, List, Optional, Any
import json

class TreeSitterParser:
    @staticmethod
    def parse_position(text: str) -> Optional[Dict[str, int]]:
        """Parse position string like [0, 0] - [54, 1] into position dict."""
        pattern = r'\[(\d+),\s*(\d+)\]\s*-\s*\[(\d+),\s*(\d+)\]'
        match = re.match(pattern, text)
        if not match:
            return None
            
        start_row, start_col, end_row, end_col = map(int, match.groups())
        return {
            "row_start": start_row,
            "row_end": end_row,
            "col_start": start_col,
            "col_end": end_col
        }

    @staticmethod
    def parse_line(line: str) -> Optional[Dict[str, Any]]:
        """Parse a single line of tree-sitter output."""
        # Get indent level and clean line
        indent_spaces = len(line) - len(line.lstrip())
        indent_level = indent_spaces // 2
        line = line.strip()

        # Split into components
        parts = line.split(':', 1)
        if len(parts) < 2:
            return None

        node_type, rest = parts
        node_type = node_type.strip()

        # Split rest into name and position
        rest_parts = rest.strip().split(' ', 1)
        if len(rest_parts) < 2:
            return None

        node_name, position = rest_parts
        position_dict = TreeSitterParser.parse_position(position)

        return {
            "indent": indent_level,
            "type": node_type,
            "name": node_name.strip(),
            "position": position_dict
        }

    @staticmethod
    def convert_to_json(tree_output: str) -> Dict[str, Any]:
        """Convert tree-sitter output to JSON structure."""
        lines = [line for line in tree_output.split('\n') if line.strip()]
        stack = [{"children": []}]
        last_indent = -1

        for line in lines:
            parsed = TreeSitterParser.parse_line(line)
            if not parsed:
                continue

            # Create node structure
            node = {
                "type": parsed["type"],
                **parsed["position"],
                "children": []
            }
            
            # Add name only if different from type
            if parsed["name"] != parsed["type"]:
                node["name"] = parsed["name"]

            # Handle indentation
            while parsed["indent"] <= last_indent and len(stack) > 1:
                stack.pop()
                last_indent -= 1

            # Add node to parent's children
            stack[-1]["children"].append(node)

            # Push node to stack if it might have children
            stack.append(node)
            last_indent = parsed["indent"]

        # Return first real node (skip root wrapper)
        return stack[0]["children"][0]

def main():
    try:
        with open("meta.nix.treesitter", "r", encoding="utf-8") as file:
            tree_output = file.read()

        parser = TreeSitterParser()
        result = parser.convert_to_json(tree_output)
        
        # Write the result to a JSON file
        with open("meta.nix.json", "w", encoding="utf-8") as outfile:
            json.dump(result, outfile, indent=2)
        
        print(f"Successfully parsed treesitter output and saved to meta.nix.json")
    except FileNotFoundError:
        print("Error: Could not find meta.nix.treesitter")
    except json.JSONDecodeError:
        print("Error: Failed to generate valid JSON")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
