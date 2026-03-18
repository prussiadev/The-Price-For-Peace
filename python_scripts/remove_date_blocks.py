import os
import shutil
from tkinter import Tk, filedialog

def remove_date_blocks(text):
    result = []
    i = 0
    length = len(text)

    while i < length:
        # Look for start of a date block: YYYY.M.D = {
        if (
            i + 10 < length
            and text[i].isdigit()
            and text[i:i+4].isdigit()
            and text[i+4] == '.'
        ):
            # Try to parse the full date pattern
            j = i
            while j < length and (text[j].isdigit() or text[j] == '.'):
                j += 1

            # Skip whitespace
            k = j
            while k < length and text[k].isspace():
                k += 1

            # Check for "= {"
            if k + 1 < length and text[k] == '=':
                k += 1
                while k < length and text[k].isspace():
                    k += 1

                if k < length and text[k] == '{':
                    # Found start of date block
                    brace_depth = 1
                    k += 1

                    while k < length and brace_depth > 0:
                        if text[k] == '{':
                            brace_depth += 1
                        elif text[k] == '}':
                            brace_depth -= 1
                        k += 1

                    # Skip everything in this block
                    i = k
                    continue

        # Normal character, keep it
        result.append(text[i])
        i += 1

    return ''.join(result)


def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        cleaned_text = remove_date_blocks(original_text)

        if cleaned_text != original_text:
            # Backup
            shutil.copy2(file_path, file_path + ".bak")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Processed: {filename}")


if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select folder containing files")
    if folder:
        process_folder(folder)
        print("Done.")
