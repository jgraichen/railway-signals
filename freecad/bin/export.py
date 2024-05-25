#!/usr/bin/env fccmd
# pylint: disable=missing-docstring,invalid-name
# pyright: reportMissingImports=false, reportMissingModuleSource=false
"""
Export first root object to STL or STEP.
"""

import argparse
import os
import os.path

# pylint: disable=import-error,wrong-import-position
import FreeCAD  # noqa: E402
import Mesh  # noqa: E402
import Part  # noqa: E402

FORMAT_MESH = ["obj", "stl"]
FORMAT_PART = ["step", "wrl"]


def export(output: str):
    _, fmt = os.path.splitext(output)

    os.makedirs(os.path.dirname(output), exist_ok=True)

    doc = FreeCAD.activeDocument()

    # Only export all part features objects from the first root element
    root = doc.RootObjects[0]

    # pprint((root, root.Label, root.TypeId))

    if root.isDerivedFrom("Part::Feature"):
        # Root is a part body: We can directly export that
        objects = [root]

    elif root.isDerivedFrom("App::Part"):
        # Root is an assembly: Scan for all individual parts
        objects = doc.findObjects("Part::Feature")
        objects = [o for o in objects if root in o.InListRecursive]

    # pprint([(o, o.Label, o.TypeId) for o in objects])

    if fmt.lower() in FORMAT_MESH:
        Mesh.export([root], output)
    else:
        Part.export(objects, output)


parser = argparse.ArgumentParser()
parser.add_argument("trash", nargs="*")
parser.add_argument("--pass", dest="output", nargs=1)
args = parser.parse_args()

export(args.output[0])
