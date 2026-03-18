import os
from tkinter import Tk, filedialog

def copy_folder_structure_only(source_root, target_root):
    source_root = os.path.abspath(source_root)
    target_root = os.path.abspath(target_root)

    for root, dirs, files in os.walk(source_root):
        # Determine relative path from base game root
        rel_path = os.path.relpath(root, source_root)

        # Skip the root "." case
        if rel_path == ".":
            target_dir = target_root
        else:
            target_dir = os.path.join(target_root, rel_path)

        # Create directory if it does not exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f"Created folder: {target_dir}")

        # We explicitly ignore files
        # dirs are handled automatically by os.walk

def main():
    root = Tk()
    root.withdraw()

    base_game_folder = filedialog.askdirectory(
        title="Select BASE GAME root folder"
    )
    if not base_game_folder:
        return

    mod_folder = filedialog.askdirectory(
        title="Select MOD root folder"
    )
    if not mod_folder:
        return

    copy_folder_structure_only(base_game_folder, mod_folder)
    print("Folder structure copy complete.")

if __name__ == "__main__":
    main()
