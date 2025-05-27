# AutoLibrarian

AutoLibrarian is a lightweight Python utility designed to automatically organize PDF files into categorized folders based on their content. The ultimate goal of this project is to create a fully autonomous system that determines the optimal storage structure and sorts all books without any user input—much like a real librarian. Initially, I started building a version with a graphical user interface, but I later realized that this shifted the project toward a typical library management system, which wasn’t my original intention.
## Usage

### Step 1: Define the storage structure

Manually create the folder layout, the following is an example:


``` 
AutoLibrarian
├── unsorted              # Place new or unorganized PDF files here
├── sorted                # Organized files will be moved here
│   ├── science
│   │   ├── engineering
│   │   └── physics
│   ├── humanities
│   └── sics

```

### Step 2: Manually categorize some books

To help generate accurate keywords, manually move a few well-categorized books into the appropriate leaf folders under `sorted/`.

### Step 3: Generate keywords

Run the keyword generation script to analyze the files you've sorted manually:

```
python keyword_generator.py
```

This script will:
- Analyze PDFs in the `sorted` folder
- Filter out stopwords
- Show the top 20 most frequent words found in the index or the first and last 20 pages of each file and update the `.keywords` file in every leaf folder

### Step 5: Move files to be processed

Put the new or unorganized PDF files into the `unsorted` folder.

### Step 6: Run `SortAll.py`

Execute the main sorting script:

```
python SortAll.py
```

This will:
- Read each PDF file in the `unsorted` folder
- Extract text from the index (if found), or the first and last 20 pages
- Match the content to categories based on keyword proportions
- Move each file to the most relevant folder inside `sorted/`

## Notes

- Stopwords are handled using the NLTK library (downloaded locally).
- You can customize keyword sets and folder depth by editing the category definitions in the script.
- All analysis is offline and file movement is local.
