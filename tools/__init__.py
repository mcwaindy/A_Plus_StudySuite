"""tools package - Contains standalone utility scripts."""

import sys
from pathlib import Path

# Ensure parent directory is in Python path for relative imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

