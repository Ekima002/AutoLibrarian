import os
import shutil
import fitz  # PyMuPDF

# Define folder structure
UNSORTED_DIR = "./unsorted"
SORTED_DIR = "./sorted"
INDEX_FILE = "./library_index.txt"

# Step 1: Load all .keywords from the tree under /sorted
def load_categories_from_folders(root_folder):
    categories = {}
    for root, dirs, files in os.walk(root_folder):
        if ".keywords" in files:
            keyword_file = os.path.join(root, ".keywords")
            with open(keyword_file, "r", encoding="utf-8") as f:
                keywords = [line.strip().lower() for line in f if line.strip()]
                rel_path = os.path.relpath(root, root_folder)
                categories[rel_path] = keywords
    return categories

# Step 2: Extract index text only if there is an index page
def is_index_page(page_text):
    """ Determine if a page is likely an index page based on headers and formatting patterns. """
    lines = page_text.splitlines()

    # Check if the first word is 'Index' (case-insensitive)
    if lines and lines[0].strip().lower() == "index":
        return True

    return False

def extract_text(pdf_path):
    """ Extract relevant text from a PDF file and return it with page count. """
    text = ""
    n_pages = 0
    try:
        doc = fitz.open(pdf_path)
        n_pages = len(doc)
        index_page = None

        # Search for an index page in the last 50 pages
        for i in range(max(0, n_pages - 50), n_pages):
            page_text = doc[i].get_text()
            if is_index_page(page_text):
                index_page = i
                break  # Stop at the first occurrence of an index page

        if index_page is not None:
            # Extract text from pages on and after the detected index page
            for i in range(index_page, n_pages):
                text += doc[i].get_text()
        else:
            # If no index page is found, extract text from the first and last 20 pages without duplication
            first_pages = set(range(min(20, n_pages)))
            last_pages = set(range(max(0, n_pages - 20), n_pages))
            pages_to_extract = first_pages.union(last_pages)

            for i in sorted(pages_to_extract):
                text += doc[i].get_text()
    except Exception as e:
        print(f"⚠️ Failed to read {pdf_path}: {e}")
    return text.lower(), n_pages

# Step 3: Match based on most keyword hits
def classify_text(text, categories):
    best_score = 0
    best_category = "misc/unknown"

    for category, keywords in categories.items():
        if not keywords:
            continue
        match_count = sum(1 for keyword in keywords if keyword in text)
        score = match_count / len(keywords)  # Proportion of keywords matched
        if score > best_score:
            best_score = score
            best_category = category

    return best_category

# Step 4: Update library index file
def update_index():
    """ Generate a library index based on the sorted folder structure. """
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        for root, dirs, files in os.walk(SORTED_DIR):
            rel_path = os.path.relpath(root, SORTED_DIR)
            if rel_path == ".":
                continue  # Skip the root directory
            f.write(f"{rel_path}/\n")
            for file in sorted(files):
                if file.lower().endswith(".pdf"):
                    f.write(f"    {file}\n")
    print(f"📚 Library index updated: {INDEX_FILE}")

# Step 5: Move file to best-matching folder (with duplicate check)
def move_file_to_category(filepath, category):
    dest_folder = os.path.join(SORTED_DIR, category)
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(filepath)
    dest_path = os.path.join(dest_folder, filename)

    # Check for existing file
    if os.path.exists(dest_path):
        print(f"⚠️ Skipped '{filename}' (already exists in '{category}')")
        return

    shutil.move(filepath, dest_path)
    print(f"✅ Moved '{filename}' to '{category}'")
    update_index()  # Update index after sorting

# Main control
def sortAll():
    for file in os.listdir(UNSORTED_DIR):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(UNSORTED_DIR, file)
            print(f"\n📄 Processing: {file}")
            text, n_pages = extract_text(full_path)

            if not text.strip():
                print("⚠️ Skipped (empty or no intro section)")
                continue

            if n_pages < 100:
                categories = load_categories_from_folders(os.path.join(SORTED_DIR, "papers"))
            else:
                categories = load_categories_from_folders(os.path.join(SORTED_DIR, "books"))

            if not categories:
                print("⚠️ No .keywords files found for appropriate category.")
                continue

            best_category = classify_text(text, categories)
            move_file_to_category(full_path, os.path.join("papers" if n_pages < 100 else "books", best_category))

if __name__ == "__main__":
    sortAll()
