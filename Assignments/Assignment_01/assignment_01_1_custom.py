import os
import sys

# Ensure the project root is on sys.path so local packages (like 'shapes') can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from shapes import Square

Square.build().side_length(150).render()

input()