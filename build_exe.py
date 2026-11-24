"""Build a single-file desktop app with PyInstaller.

    pip install -e ".[dev]"
    python build_exe.py

The result is dist/MathematicsVisualiser.exe on Windows (dist/MathematicsVisualiser
elsewhere). GitHub Actions runs this for every release; see .github/workflows/release.yml.
"""

import PyInstaller.__main__

PyInstaller.__main__.run([
    "mathviz/__main__.py",
    "--name", "MathematicsVisualiser",
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--clean",
    "--hidden-import", "matplotlib.backends.backend_tkagg",
    "--hidden-import", "PIL._tkinter_finder",
    # Not used by the app; leaving them out keeps the download small
    "--exclude-module", "IPython",
    "--exclude-module", "notebook",
    "--exclude-module", "pytest",
    "--exclude-module", "PyQt5",
    "--exclude-module", "PySide6",
])
