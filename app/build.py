import os
import sys
import shutil
import PyInstaller.__main__

# Config
ENTRY_FILE = "app/app.py"

DATA_DIRS = [
    ("app/.pollination", ".pollination"),
    ("app/assets", "assets"),
    ("app/callbacks", "callbacks"),
]

def clean_build_folders():
    """Remove PyInstaller build directories."""
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Removed folder: {folder}")


def build():
    """Build the application using PyInstaller."""
    print("============================================")
    print(" Building Design Explorer")
    print("============================================")

    clean_build_folders()

    # Build PyInstaller command
    cmd = [
        "--name", "Design Explorer",
        "--onefile",
        "--console",  # If no console wanted: replace with "--noconsole"
        ENTRY_FILE,
    ]

    # Add data folders
    for src, target in DATA_DIRS:
        cmd.append("--add-data")
        # Format: source_path:target_path (mac/linux)
        #         source_path;target_path (windows)
        sep = ";" if os.name == "nt" else ":"
        cmd.append(f"{src}{sep}{target}")

    print("\nRunning PyInstaller with arguments:")
    for c in cmd:
        print(" ", c)

    # Execute PyInstaller
    PyInstaller.__main__.run(cmd)

    print("============================================")
    print(" Build complete! Output in dist/")
    print("============================================")


if __name__ == "__main__":
    build()