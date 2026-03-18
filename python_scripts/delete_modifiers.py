import os
import shutil
from tkinter import Tk, filedialog

# ============================
# CONFIGURATION
# ============================
REMOVE_KEYS = [
    "has_completed_focus",
    "tag",
    "TAG",
    "has_war_with",
    # "has_country_flag",
]

# ============================
# CORE LOGIC
# ============================

def contains_removal_key(text, index, keys):
    for key in keys:
        if text.startswith(key, index):
            k = index + len(key)
            while k < len(text) and text[k].isspace():
                k += 1
            if k < len(text) and text[k] == "=":
                return True
    return False


def remove_modifier_blocks(text):
    result = []
    i = 0
    length = len(text)

    while i < length:
        if text.startswith("modifier", i):
            j = i + len("modifier")

            while j < length and text[j].isspace():
                j += 1

            if j < length and text[j] == "=":
                j += 1
                while j < length and text[j].isspace():
                    j += 1

                if j < length and text[j] == "{":
                    brace_depth = 1
                    j += 1
                    should_remove = False

                    while j < length and brace_depth > 0:
                        if text[j] == "{":
                            brace_depth += 1
                        elif text[j] == "}":
                            brace_depth -= 1
                        else:
                            if contains_removal_key(text, j, REMOVE_KEYS):
                                should_remove = True
                        j += 1

                    if should_remove:
                        i = j
                        continue

        result.append(text[i])
        i += 1

    return "".join(result)


def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        cleaned_text = remove_modifier_blocks(original_text)

        if cleaned_text != original_text:
            shutil.copy2(file_path, file_path + ".bak")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Processed: {filename}")


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    folder = filedialog.askdirectory(
        title="Select folder containing script files"
    )

    if folder:
        process_folder(folder)
        print("Done.")
