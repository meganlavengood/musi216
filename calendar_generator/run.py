import pathlib
import pandas as pd

TEMPLATE_FILE_NAME = "template.txt"
DATA_FILE_NAME = "data.csv"
OUTPUT_DIRECTORY = "../docs/_posts"

template = pathlib.Path(TEMPLATE_FILE_NAME).read_text()

data = pd.read_csv(DATA_FILE_NAME)

data = data.fillna("")
data = data.replace("none", "")

for row in data.iterrows():
    row_dict = row[1].to_dict()
    day = template.format(**row_dict)
    day = day.replace("[]()", "")
    pathlib.Path(
        f'{OUTPUT_DIRECTORY}/{row_dict["date"]}-{row_dict["r-title"].replace(" ", "-").lower()}.md'
    ).write_text(day)
