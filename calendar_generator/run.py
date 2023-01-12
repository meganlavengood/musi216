import pathlib
import pandas as pd

TEMPLATE_FILE_NAME = "template.txt"
COMPOSITION_TEMPLATE_FILE_NAME = "composition_template.txt"
DATA_FILE_NAME = "data.csv"
POST_OUTPUT_DIRECTORY = "../docs/_posts"
COMPOSITION_OUTPUT_DIRECTORY = '../docs'

template = pathlib.Path(TEMPLATE_FILE_NAME).read_text()
composition_template = pathlib.Path(COMPOSITION_TEMPLATE_FILE_NAME).read_text()

data = pd.read_csv(DATA_FILE_NAME)

data = data.fillna("")
data = data.replace("none", "")

def build_posts(data):
    for row in data.iterrows():
        row_dict = row[1].to_dict()
        day = template.format(**row_dict)
        day = day.replace("[]()", "")
        pathlib.Path(
            f'{POST_OUTPUT_DIRECTORY}/{row_dict["date"]}-{row_dict["r-title"].replace(" ", "-").lower()}.md'
        ).write_text(day)

def build_compositions(data, composition_template):
    comp_keywords = parse_composition_keywords(composition_template)
    comp_dict = {}
    for row in data.iterrows():
        row_dict = row[1].to_dict()
        title = row_dict['a-title'].lower()
        if 'project' in title:
            for kw in comp_keywords:
                if kw in title:
                    comp_keywords.remove(kw)
                    comp_dict[f'{kw}_url'] = row_dict['a-url']
                    comp_dict[f'{kw}_date'] = row_dict['post-name']
    compositions_footer = composition_template.split('\n')[-1]
    compositions = composition_template[:composition_template.rfind('\n')].format(**comp_dict) + compositions_footer
    pathlib.Path(f'{COMPOSITION_OUTPUT_DIRECTORY}/Compositions.md').write_text(compositions)


def parse_composition_keywords(template):
    result = []
    for line in template.split('\n'):
        if line.startswith('##'):
            kw = line.split(' ')[1].lower()
            if kw != 'submitting':
                result.append(kw)
    return result

build_posts(data)
build_compositions(data, composition_template)