import pathlib
import pandas as pd
import re
from jinja2 import Environment, FileSystemLoader

TEMPLATE_FILE_NAME = "post_template.md.jinja"
COMPOSITION_TEMPLATE_FILE_NAME = "composition_template.md.jinja"
SYLLABUS_TEMPLATE_FILE_NAME = "syllabus_template.md.jinja"
DATA_FILE_NAME = "data.csv"
POST_OUTPUT_DIRECTORY = "../docs/_posts"
COMPOSITION_OUTPUT_DIRECTORY = "../docs"
SYLLABUS_OUTPUT_DIRECTORY = "../docs"

composition_template_raw = pathlib.Path(COMPOSITION_TEMPLATE_FILE_NAME).read_text()
syllabus_template_raw = pathlib.Path(SYLLABUS_TEMPLATE_FILE_NAME).read_text()

environment = Environment(loader=FileSystemLoader("."))
post_template = environment.get_template(TEMPLATE_FILE_NAME)
composition_template = environment.get_template(COMPOSITION_TEMPLATE_FILE_NAME)
syllabus_template = environment.get_template(SYLLABUS_TEMPLATE_FILE_NAME)

data = pd.read_csv(DATA_FILE_NAME)

data = data.fillna("")
data = data.replace("none", " ")
data = data.replace("None", " ")


def build_posts(data):
    for row in data.iterrows():
        row_dict = row[1].to_dict()
        row_dict["d-url"] = row_dict["d-url"] or " "
        row_dict["r-url"] = row_dict["r-url"] or " "
        row_dict["a-url"] = row_dict["a-url"] or " "
        row_dict["post_name"] = row_dict["post-name"]
        row_dict["homework_due_links"] = make_links(
            row_dict["d-title"], row_dict["d-url"]
        )
        row_dict["class_topic_links"] = make_links(
            row_dict["r-title"], row_dict["r-url"]
        )
        row_dict["homework_assigned_links"] = make_links(
            row_dict["a-title"], row_dict["a-url"]
        )
        post_filename = f'{POST_OUTPUT_DIRECTORY}/{row_dict["date"]}-{format_title(row_dict["r-title"])}.md'

        with open(post_filename, mode="w", encoding="utf-8") as results:
            results.write(post_template.render(row_dict))
        print(f"... wrote {post_filename}")


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


def listify(item):
    return item if isinstance(item, list) else [item]


def make_links(titles, urls):
    links = []
    titles = listify(titles.splitlines())
    urls = listify(urls.splitlines())
    for pair in zip(titles, urls):
        if pair[1] == " ":
            links.append(f"{pair[0]}")
        else:
            links.append(f"[{pair[0]}]({pair[1]})")

    return links


def build_compositions(data, composition_template_raw):
    comp_dict = get_composition_details(data, composition_template_raw)
    composition_filename = f"{COMPOSITION_OUTPUT_DIRECTORY}/compositions.md"

    with open(composition_filename, mode="w", encoding="utf-8") as results:
        results.write(composition_template.render(comp_dict))
    print(f"... wrote {composition_filename}")


def build_syllabus(data, syllabus_template, composition_template_raw):
    comp_dict = get_composition_details(data, composition_template_raw)
    syllabus_filename = f"{SYLLABUS_OUTPUT_DIRECTORY}/syllabus.md"
    with open(syllabus_filename, mode="w", encoding="utf-8") as results:
        results.write(syllabus_template.render(comp_dict))
    print(f"... wrote {syllabus_filename}")


def get_composition_details(data, composition_template_raw):
    comp_keywords = parse_composition_keywords(composition_template_raw)
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
            kw = line.split(" ")[1].split("-")[0].lower()
            if kw != "submitting":
                result.append(kw)
    return result


build_posts(data)
build_compositions(data, composition_template_raw)
build_syllabus(data, syllabus_template, composition_template_raw)
