import pathlib
import pandas as pd
import re

TEMPLATE_FILE_NAME = "template.txt"
COMPOSITION_TEMPLATE_FILE_NAME = "composition_template.txt"
SYLLABUS_TEMPLATE_FILE_NAME = "syllabus_template.txt"
DATA_FILE_NAME = "data.csv"
POST_OUTPUT_DIRECTORY = "../docs/_posts"
COMPOSITION_OUTPUT_DIRECTORY = "../docs"
SYLLABUS_OUTPUT_DIRECTORY = "../docs"

template = pathlib.Path(TEMPLATE_FILE_NAME).read_text()
composition_template = pathlib.Path(COMPOSITION_TEMPLATE_FILE_NAME).read_text()
syllabus_template = pathlib.Path(SYLLABUS_TEMPLATE_FILE_NAME).read_text()

data = pd.read_csv(DATA_FILE_NAME)

data = data.fillna("<DELETE>")
data = data.replace("none", "<DELETE>")
data = data.replace("None", "<DELETE>")


def build_posts(data):
    for row in data.iterrows():
        row_dict = row[1].to_dict()
        row_dict["d-links"] = make_links(row_dict["d-title"], row_dict["d-url"])
        row_dict["r-links"] = make_links(row_dict["r-title"], row_dict["r-url"])
        row_dict["a-links"] = make_links(row_dict["a-title"], row_dict["a-url"])
        day = template.format(**row_dict)
        day = day.replace("[<DELETE>](<DELETE>)", "<DELETE>")
        day = delete_sections(day)

        pathlib.Path(
            f'{POST_OUTPUT_DIRECTORY}/{row_dict["date"]}-{format_title(row_dict["r-title"])}.md'
        ).write_text(day)


def format_title(title):
    return (
        title.rstrip()
        .replace(" ", "-")
        .replace("\r\n", "-")
        .replace("\n", "-")
        .replace("\r", "-")
        .replace(",", "")
        .replace("?", "")
        .lower()
    )


def make_links(titles, urls):
    links = []
    titles = titles.split("\r\n")
    urls = urls.split("\r\n")
    for pair in zip(titles, urls):
        if pair[0] and pair[1] == "<DELETE>":
            links.append(f"{pair[0]}")
        else:
            links.append(f"[{pair[0]}]({pair[1]})")
    return "\n\n".join(links)


def delete_sections(day):
    res = re.sub(r"## [\w\d\n ]*<DELETE>", "", day)
    res = re.sub(r"[\n]{3,}", r"\n\n", res)
    return res


def build_compositions(data, composition_template):
    comp_dict = get_composition_details(data, composition_template)
    compositions_footer = composition_template.split("\n")[-1]
    compositions = (
        composition_template[: composition_template.rfind("\n")].format(**comp_dict)
        + compositions_footer
    )
    pathlib.Path(f"{COMPOSITION_OUTPUT_DIRECTORY}/compositions.md").write_text(
        compositions
    )


def build_syllabus(data, syllabus_template, composition_template):
    comp_dict = get_composition_details(data, composition_template)
    syllabus = syllabus_template.format(**comp_dict)
    pathlib.Path(f"{SYLLABUS_OUTPUT_DIRECTORY}/syllabus.md").write_text(syllabus)


def get_composition_details(data, composition_template):
    comp_keywords = parse_composition_keywords(composition_template)
    comp_dict = {}
    for row in data.iterrows():
        row_dict = row[1].to_dict()
        title = row_dict["d-title"].lower()
        if "project" in title:
            for kw in comp_keywords:
                if kw in title:
                    comp_keywords.remove(kw)
                    comp_dict[f"{kw}_url"] = row_dict["d-url"]
                    comp_dict[f"{kw}_date"] = row_dict["post-name"]
    return comp_dict


def parse_composition_keywords(template):
    result = []
    for line in template.split("\n"):
        if line.startswith("##"):
            kw = line.split(" ")[1].split('-')[0].lower()
            if kw != "submitting":
                result.append(kw)
    return result


build_posts(data)
build_compositions(data, composition_template)
build_syllabus(data, syllabus_template, composition_template)