#!/usr/bin/env fccmd
# pylint: disable=missing-docstring,invalid-name
# pyright: reportMissingImports=false, reportMissingModuleSource=false
"""
Export first root object to STL or STEP.
"""

import argparse
import os
import os.path
from pprint import pprint

# pylint: disable=import-error,wrong-import-position
import FreeCAD  # noqa: E402
import Mesh  # noqa: E402
import Part  # noqa: E402

FORMAT_MESH = ["obj", "stl"]
FORMAT_PART = ["step", "wrl"]


def export(output: str):
    _, ext = os.path.splitext(output)
    fmt = ext.strip(".")

    os.makedirs(os.path.dirname(output), exist_ok=True)

    doc = FreeCAD.activeDocument()

    # Only export all part features objects from the first root element
    root = doc.RootObjects[0]

    pprint(("ROOT", root, root.Label, root.TypeId))

    if fmt.lower() in FORMAT_MESH:
        Mesh.export([root], output)
        return

    if root.isDerivedFrom("Part::Feature"):
        # Root is a part body: We can directly export that
        Part.export([root], output)

    elif root.isDerivedFrom("Assembly::AssemblyObject"):
        # Root is a new assembly: Export assembly shape directly
        root.Shape.exportStep(output)

    elif root.isDerivedFrom("App::Part"):
        # Root is an old assembly: Scan for all individual parts
        objects = [o for o in doc.Objects if root in o.InListRecursive]
        Part.export(objects, output)


parser = argparse.ArgumentParser()
parser.add_argument("trash", nargs="*")
parser.add_argument("--pass", dest="output", nargs=1)
args = parser.parse_args()

export(args.output[0])
