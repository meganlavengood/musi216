## Running this script

* delete old files
* in terminal, navigate to this folder and enter `poetry shell` followed by `python run.py`


## Adapting this to other courses

### Changing composition names

Throughout the Syllabus and Compositions template files, compositions are referred to by composition keywords, which are the first word in each heading in `composition_template.txt` if the first word isn't `Submitting`. Only the first part of a hyphenated word is used, so a composition called `Debussy-style` is referred to as `debussy`.

Make sure all `*_date` and `*_url` variables in double square brackets `{{ }}` start with a valid composition keyword throughout `syllabus_template.txt` and `composition_template.txt`. 

### Composition dates and URLs

Composition dates and URLs are pulled from the data file (`data.csv`). The script iterates over every row performs the following steps:

- find a row with the word `project` in the `d-title` cell
- iterate through all composition keywords
- if a keyword is part of the title string, store the entries `{composition_keyword}_url` and `{composition_keyword}_date` with values from the `d-url` and `post-name` columns, respectively in a dictionary

Entries in this dictionary are used to replace variables in `{{ }}` in both templates.