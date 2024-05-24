#!/usr/bin/env python3
# pylint: disable=missing-docstring,invalid-name
# pyright: reportMissingImports=false, reportMissingModuleSource=false
"""
Export first root object to STL or STEP.
"""

import argparse
import os
import os.path
import sys
from pprint import pprint

for path in [
    "~/.local/lib/freecad/lib",
    "~/.local/share/freecad/Mod",
    "/usr/local/lib/freecad/lib",
    "/usr/local/share/freecad/Mod",
    "/usr/lib/freecad/lib",
    "/usr/share/freecad/Mod",
]:
    path = os.path.expanduser(path)
    if os.path.exists(path):
        sys.path.append(path)

# pylint: disable=import-error,wrong-import-position
import FreeCAD  # noqa: E402
import Mesh  # noqa: E402
import Part  # noqa: E402

FORMAT_MESH = ["obj", "stl"]
FORMAT_PART = ["step", "wrl"]


def export(output: str, src: str | None = None):
    _, ext = os.path.splitext(output)
    fmt = ext.strip(".")

    os.makedirs(os.path.dirname(output), exist_ok=True)

    pprint((output, fmt))

    if src:
        FreeCAD.open(src)
    doc = FreeCAD.activeDocument()

    # Only export all part features objects from the first root element
    root = doc.RootObjects[0]

    pprint((root, root.Label, root.TypeId))

    # Mesh is easy to export; pass root object and be done
    if fmt.lower() in FORMAT_MESH:
        Mesh.export([root], output)
        return

    if root.isDerivedFrom("Part::Feature"):
        # Root is a part body: We can directly export that
        objects = [root]

    elif root.isDerivedFrom("App::Part"):
        # Root is an assembly: Scan for all individual parts
        objects = list()
        objects.extend(doc.findObjects("Part::Feature"))
        objects.extend(doc.findObjects("App::Link"))
        objects = [o for o in objects if root in o.InListRecursive]

    pprint(objects)

    Part.export(objects, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", nargs=1)
    parser.add_argument("output", nargs=1)
    args = parser.parse_args()

    export(args.output[0], args.src[0])
else:
    parser = argparse.ArgumentParser()
    parser.add_argument("trash", nargs="*")
    parser.add_argument("--pass", dest="output", nargs=1)
    args = parser.parse_args()

    export(args.output[0])
