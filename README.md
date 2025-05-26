# AutoLibrarian

AutoLibrarian is a small tool that helps automatically organize PDF files by analyzing their content and sorting them into folders based on predefined keywords.

## Requirements

- Python
- Install required Python packages:

```
pip install nltk PyMuPDF

```

## Setup

1. Create the following folder structure:

.
├── unsorted            # Folder where downloaded PDFs are placed
├── sorted              # Folder where categorized PDFs will be moved
│   ├── science
│   │   ├── engineering
│   │   └── physics
│   ├── humanities
│   └── sics


2. The script will download NLTK stopwords locally if not present. This avoids writing to global directories.

3. Run the classification script:

```

python autolibrarian.py
```

This will:

- Read each PDF file in the `unsorted` folder
- Extract text from the introduction or preface sections (and optionally index)
- Match the content to categories based on keyword proportion
- Move the file to the most relevant folder inside `sorted`

## Updating Keywords

To improve classification accuracy, you can run a helper script to extract the top frequent words from already sorted PDFs:

```

python keyword\_generator.py

```

This script will:

- Analyze PDFs in the `sorted` folder
- Filter out stopwords
- Show the top 20 most frequent words for each file
- Help you decide which keywords to add to your categories

## Notes

- All NLTK data is stored locally in `./nltk_data`
- Stopwords are filtered using NLTK's built-in list, extended with some domain-specific terms
- Only the first 20 pages and the final few pages (for index) are analyzed

This is an experimental utility intended to make organizing technical and academic PDF files easier.
