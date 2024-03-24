#!/usr/bin/env python3
# vim: ft=python:fs=4


import argparse
import re
import xml.etree.ElementTree as ET
from os import path

import yaml


def createElement(parent: ET.Element, tag, text=None, tail=None, **attrib):
    el = ET.SubElement(parent, tag, attrib=attrib)
    el.text = text
    el.tail = tail
    return el


def generate_preview(td, name, default):
    count = len(default["images"])
    if count < 2:
        for pattern in default["images"]:
            createElement(td, "img", src=pattern.format(name=name))
    else:
        for pattern in default["images"]:
            createElement(
                td, "img", src=pattern.format(name=name), width=f"{90 / count}%"
            )

    createElement(td, "br")
    createElement(td, "a", href=f"export/{name}.step", text="STEP", tail=" · ")
    createElement(td, "a", href=f"export/{name}.stl", text="STL")
    return True


def generate(data, section="default"):
    root = ET.Element("table", width="100%")
    thead = createElement(root, "thead")
    tbody = createElement(root, "tbody")

    config = data.get(section, {})
    default = {
        "columns": 2,
        "width": 200,
        "images": ["export/{name}-front.png"],
    }
    if "default" in config:
        default |= config.pop("default")

    thr = createElement(thead, "tr")
    createElement(thr, "th", colspan=f"{default['columns']}", text="Vorschau")
    createElement(thr, "th", text="Anmerkungen")

    for key, data in config.items():
        tr = createElement(tbody, "tr")

        if not data:
            data = {}
        if isinstance(data, list):
            data = {"notes": data}

        if "files" not in data:
            if path.isfile(f"{key}__A.FCStd") or path.isfile(f"{key}__B.FCStd"):
                data["files"] = [f"{key}__A", f"{key}__B"]
            else:
                data["files"] = [f"{key}"]

        for idx in range(default["columns"]):
            td = createElement(tr, "td", width=f"{default['width']}", align="center")
            files = data.get('files', [])
            if len(files) > idx:
                file = files[idx]
                if path.isfile(f"{file}.FCStd"):
                    generate_preview(td, file, default)

        td = createElement(tr, "td")
        if "notes" in data:
            ul = createElement(td, "ul")
            for note in data["notes"]:
                createElement(ul, "li", text=note)

    ET.indent(root)
    return ET.tostring(root, encoding="unicode", method="html")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", type=argparse.FileType("r", encoding="utf8"))
    parser.add_argument("templatefile", type=argparse.FileType("r", encoding="utf8"))
    parser.add_argument("outputfile")
    args = parser.parse_args()

    data = yaml.safe_load(args.datafile)
    tmpl = args.templatefile.read()

    def replace(match):
        return generate(data, match.group(1))

    output = re.sub(
        "<!--\\s*yield\\s+(\\w+)\\s*-->",
        replace,
        tmpl,
        flags=re.DOTALL,
    )
    with open(args.outputfile, "w", encoding="utf8") as fd:
        fd.write(output)


if __name__ == "__main__":
    main()
