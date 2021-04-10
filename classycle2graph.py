#!/usr/bin/env python3

from sys import argv, stderr
import xml.etree.ElementTree as ET

import networkx as nx


def get_packages_dependency_graph(packages):
    graph = nx.DiGraph()
    for package in packages:
        graph.add_node(
            package.attrib["name"],
            label=package.attrib["name"].split(".")[-1],
            full_name=package.attrib["name"],
            short_name=package.attrib["name"].split(".")[-1],
            size=int(package.attrib["size"]),
            module_size=int(package.attrib["size"]),
            layer=int(package.attrib["layer"]),
            usedBy=int(package.attrib["usedBy"]),
            usesInternal=int(package.attrib["usesInternal"]),
            usesExternal=int(package.attrib["usesExternal"]),
            cycle=package.attrib["cycle"] != "",
        )
        for package_ref in package:
            if package_ref.attrib["type"] == "usesInternal":
                graph.add_edge(package.attrib["name"], package_ref.attrib["name"])
    return graph


def get_classes_dependency_graph(classes):
    graph = nx.DiGraph()
    for class_file in classes:
        graph.add_node(
            class_file.attrib["name"],
            label=class_file.attrib["name"].split(".")[-1],
            full_name=class_file.attrib["name"],
            short_name=class_file.attrib["name"].split(".")[-1],
            type=class_file.attrib["type"],
            innerClass=class_file.attrib["innerClass"],
            size=int(class_file.attrib["size"]),
            class_size=int(class_file.attrib["size"]),
            layer=int(class_file.attrib["layer"]),
            usedBy=int(class_file.attrib["usedBy"]),
            usesInternal=int(class_file.attrib["usesInternal"]),
            usesExternal=int(class_file.attrib["usesExternal"]),
            cycle=class_file.attrib["cycle"] != "",
        )
        for class_ref in class_file:
            if class_ref.attrib["type"] == "usesInternal":
                graph.add_edge(class_file.attrib["name"], class_ref.attrib["name"])
    return graph


def main():
    if len(argv) != 4:
        print(
            "usage:\t%s <classycle-output.xml> <module_dependencies.graphml> <class_dependencies.graphml>",
            file=stderr,
        )
        exit(2)

    tree = ET.parse(argv[1])
    root = tree.getroot()
    print("Anlyzing %s (snapshot %s)" % (root.attrib["title"], root.attrib["date"]))

    packages_dependency_graph = get_packages_dependency_graph(root.find("packages"))
    print("%d modules" % len(packages_dependency_graph.nodes))
    nx.write_graphml(packages_dependency_graph, argv[2])

    classes_dependency_graph = get_classes_dependency_graph(root.find("classes"))
    print("%d classes" % len(classes_dependency_graph.nodes))
    nx.write_graphml(classes_dependency_graph, argv[3])


if __name__ == '__main__':
    main()
