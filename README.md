# AutoLibrarian

AutoLibrarian is a small tool that helps automatically organize PDF files by analyzing their content and sorting them into folders based on predefined keywords.

## Requirements

- Python
- Install required Python packages:

```
pip install nltk PyMuPDF

```

## Setup

1. Create the storage structure as you wanted
2. Manually categorize some books into the leaf folders
3. Use keyword\_generator.py to generate the keywords
```
python keyword\_generator.py
```

This script will:

- Analyze PDFs in the `sorted` folder
- Filter out stopwords
- Show the top 20 most frequent words for the index or the first and final 20 pages in each file
- Help you decide which keywords to add to your categories
5. Move files to be solved into the unsorted folder
6. Run autolibrarian.py to sort all the files in unsorted folder

```
python autolibrarian.py
```

This will:

- Read each PDF file in the `unsorted` folder
- Extract text from the index (if there is an index in the file) or the first and last 20 pages
- Match the content to categories based on keyword proportion
- Move the file to the most relevant folder inside `sorted`



## Notes

- All NLTK data is stored locally in `./nltk_data`
- Stopwords are filtered using NLTK's built-in list, extended with some domain-specific terms
- Only the first 20 pages and the final few pages (for index) are analyzed

This is an experimental utility intended to make organizing technical and academic PDF files easier.
