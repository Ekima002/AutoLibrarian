import os
import shutil

# Define directories
SORTED_DIR = "./sorted"
UNSORTED_DIR = "./unsorted"
INDEX_FILE = "./library_index.txt"

# Ensure the unsorted directory exists
os.makedirs(UNSORTED_DIR, exist_ok=True)

def clear_index():
    """ Clear the library index file. """
    open(INDEX_FILE, "w").close()
    print(f"🗑️ Cleared index file: {INDEX_FILE}")

def move_sorted_pdfs_back():
    """ Move all PDFs from 'sorted' back to 'unsorted' and clear index file. """
    moved_files = 0

    for root, _, files in os.walk(SORTED_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                sorted_path = os.path.join(root, file)
                unsorted_path = os.path.join(UNSORTED_DIR, file)

                # Check if the file already exists in unsorted
                if os.path.exists(unsorted_path):
                    print(f"⚠️ Skipped '{file}' (already in unsorted)")
                    continue

                shutil.move(sorted_path, unsorted_path)
                moved_files += 1
                print(f"✅ Moved '{file}' to unsorted")

    if moved_files:
        print(f"\n📦 Successfully moved {moved_files} PDFs to '{UNSORTED_DIR}'")
        clear_index()  # Clear index once all files are moved
    else:
        print("\n🚨 No PDFs found to move!")

# Run the script
if __name__ == "__main__":
    move_sorted_pdfs_back()
