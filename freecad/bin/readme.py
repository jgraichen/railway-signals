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


def generate_preview(td, name):
    createElement(td, "img", src=f"export/{name}-front.png")
    createElement(td, "br")
    createElement(td, "a", href=f"export/{name}.step", text="STEP", tail=" · ")
    createElement(td, "a", href=f"export/{name}.stl", text="STL")
    return True


def generate(data, section="default"):
    root = ET.Element("table")
    thead = createElement(root, "thead")
    tbody = createElement(root, "tbody")

    thr = createElement(thead, "tr")
    createElement(thr, "th", colspan="2", text="Vorschau")
    createElement(thr, "th", text="Anmerkungen")

    for key, notes in data.get(section, {}).items():
        tr = createElement(tbody, "tr")

        if path.isfile(f"{key}__A.FCStd") or path.isfile(f"{key}__B.FCStd"):
            td = createElement(tr, "td", width="130", align="center")
            if path.isfile(f"{key}__A.FCStd"):
                generate_preview(td, f"{key}__A")

            td = createElement(tr, "td", width="130", align="center")
            if path.isfile(f"{key}__B.FCStd"):
                generate_preview(td, f"{key}__B")
        else:
            td = createElement(tr, "td", width="130", align="center")
            generate_preview(td, key)
            createElement(tr, "td")

        td = createElement(tr, "td")
        if notes:
            ul = createElement(td, "ul")
            for note in notes:
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
