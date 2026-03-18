import os
from tkinter import Tk, filedialog

# =========================
# CORE LOGIC
# =========================

def comment_set_technology_blocks(text):
    lines = text.splitlines()
    out = []

    in_block = False
    brace_depth = 0

    for line in lines:
        stripped = line.strip()

        # Detect block start
        if not in_block and stripped.startswith("add_dynamic_modifier") and "{" in stripped:
            in_block = True
            brace_depth = stripped.count("{") - stripped.count("}")
            out.append("# " + line)
            continue

        if in_block:
            brace_depth += stripped.count("{")
            brace_depth -= stripped.count("}")

            out.append("# " + line)

            if brace_depth <= 0:
                in_block = False

            continue

        out.append(line)

    return "\n".join(out)


# =========================
# FILE WALK
# =========================

def main():
    root = Tk()
    root.withdraw()

    folder = filedialog.askdirectory(title="Select root folder")
    if not folder:
        print("No folder selected.")
        return

    modified = 0

    for root_dir, _, files in os.walk(folder):
        for filename in files:
            path = os.path.join(root_dir, filename)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    original = f.read()

                updated = comment_set_technology_blocks(original)

                if updated != original:
                    with open(path + ".bak", "w", encoding="utf-8") as f:
                        f.write(original)

                    with open(path, "w", encoding="utf-8") as f:
                        f.write(updated)

                    modified += 1

            except Exception as e:
                print(f"Failed on {path}: {e}")

    print(f"Done. Files modified: {modified}")


if __name__ == "__main__":
    main()
