import os
import fitz  # PyMuPDF
import string
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re

# Define a local data path
nltk_data_dir = "./nltk_data"

# Make sure the directory exists
os.makedirs(nltk_data_dir, exist_ok=True)

# Set the NLTK data path globally in your script
nltk.data.path.append(nltk_data_dir)

# Download stopwords only if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Use stopwords from NLTK
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
# Optional: add your own domain-specific stopwords
STOPWORDS.update(["fig", "figure", "table", "et", "al", "using", "based", "results", "thus", "therefore", "also", "chapter", 
                "section", "page", "figures", "tables", "data", "analysis", "methodology", "one", "two", "three", "four", "five",
                "first", "second", "third", "fourth", "fifth", "firstly", "secondly", "thirdly", "fourthly", "fifthly"])

SORTED_DIR = "./sorted"

def is_index_page(page_text):
    """ Determine if a page is likely an index page based on headers and formatting patterns. """
    lines = page_text.splitlines()

    # Check if the first word is 'Index' (case-insensitive)
    if lines and lines[0].strip().lower() == "index":
        return True

    return False

def extract_text_from_folder(folder_path):
    """ Extract text from PDFs in a folder based on index detection or fallback rules. """
    text = ""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            try:
                doc = fitz.open(pdf_path)
                n_pages = len(doc)
                index_page = None

                # Search for an index page
                for i in range(max(0,n_pages-50),n_pages):
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
                print(f"⚠️ Failed to read {filename}: {e}")
    return text.lower()

def clean_and_count_words(text):
    # Remove punctuation and split into words
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    text = text.translate(translator)
    words = text.split()

    # Filter out stopwords and short words
    filtered = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return Counter(filtered)

def refresh_keywords():
    print("🔁 Refreshing keywords based on actual PDF content...\n")
    for root, dirs, files in os.walk(SORTED_DIR):
        # Skip folders without any PDFs
        pdfs = [f for f in files if f.lower().endswith(".pdf")]
        if not pdfs:
            continue

        print(f"📁 Processing: {root}")
        text = extract_text_from_folder(root)
        if not text.strip():
            print("⚠️ Skipped (no readable text)\n")
            continue

        word_counts = clean_and_count_words(text)
        top_words = [word for word, count in word_counts.most_common(200)]

        keyword_path = os.path.join(root, ".keywords")
        with open(keyword_path, "w", encoding="utf-8") as f:
            for word in top_words:
                f.write(f"{word}\n")
        print(f"✅ Updated .keywords with top {len(top_words)} terms\n")

if __name__ == "__main__":
    refresh_keywords()
