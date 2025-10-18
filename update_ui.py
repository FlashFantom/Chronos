import re

# Read the original file
with open("/srv/apps/Chronos/main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Read modern styles
with open("/srv/apps/Chronos/modern_styles.py", "r", encoding="utf-8") as f:
    styles_content = f.read()

# Extract the CSS
modern_css = styles_content.split("MODERN_CSS = \"\"\"")[1].split("\"\"\"")[0]

# Add import for modern styles after other imports
if "from modern_styles import MODERN_CSS" not in content:
    content = content.replace(
        "import sqlite3",
        "import sqlite3\nfrom modern_styles import MODERN_CSS"
    )

# Write updated content
with open("/srv/apps/Chronos/main.py.new", "w", encoding="utf-8") as f:
    f.write(content)

print("UI update script created")
