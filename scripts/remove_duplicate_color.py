#!/usr/bin/env python3
"""Script to remove duplicate Color class from chromo_map/color.py"""

import re

def remove_duplicate_color_class():
    """Remove the duplicate Color class from the main color.py file."""
    file_path = 'chromo_map/color.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start of the Color class
    class_start = content.find('class Color:')
    if class_start == -1:
        print("No Color class found")
        return
    
    # Find the end of the Color class by looking for the next top-level definition
    # Look for the next "def " or "class " that's not indented
    lines = content.split('\n')
    class_start_line = None
    for i, line in enumerate(lines):
        if 'class Color:' in line:
            class_start_line = i
            break
    
    if class_start_line is None:
        print("Could not find Color class start line")
        return
    
    # Find the end of the class by looking for the next non-indented line that's not empty
    class_end_line = None
    for i in range(class_start_line + 1, len(lines)):
        line = lines[i]
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            continue
        # If we find a non-indented line that starts with def or class, that's the end
        if not line.startswith(' ') and not line.startswith('\t'):
            class_end_line = i
            break
    
    if class_end_line is None:
        print("Could not find Color class end line")
        return
    
    print(f"Found Color class from line {class_start_line + 1} to {class_end_line}")
    
    # Remove the class definition
    new_lines = lines[:class_start_line] + lines[class_end_line:]
    new_content = '\n'.join(new_lines)
    
    # Write back the modified content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Removed duplicate Color class. New file has {len(new_lines)} lines (was {len(lines)} lines)")

if __name__ == '__main__':
    remove_duplicate_color_class()
