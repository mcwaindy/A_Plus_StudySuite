import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from tools.coordinate_picker_main import CoordinatePickerUI
if __name__ == '__main__':
    app = CoordinatePickerUI()
    app.mainloop()
