# This script will fix main.py by removing duplicate function bodies
import re

with open('src/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the location of the comment about moved functions
start_marker = "# Functions moved to src.utils.text_processing"
end_marker = "def process_uploaded_file(uploaded_file):"

start_index = content.find(start_marker)
end_index = content.find(end_marker)

if start_index != -1 and end_index != -1:
    # Keep only the comment and the next function
    before = content[:start_index]
    comment = "# Functions moved to src.utils.text_processing to avoid circular imports\n# (clean_text, remove_duplicates, extract_themes)\n\n"
    after = content[end_index:]
    
    fixed_content = before + comment + after
    
    with open('src/main.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed main.py - removed duplicate function bodies")
else:
    print("Could not find markers to fix")