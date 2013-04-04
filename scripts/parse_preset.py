# -*- coding:utf-8 -*-
"""
Usage:
    parse_preset <file> [options]

Options:
    -f, --format <format>        Ouput format: csv, txt, json [default: txt]
    -o, --output <filepath>      Ouput filepath [default: ./output.txt]
"""

import csv
import codecs

from lxml import etree
from docopt import docopt


class Node(object):

    def __init__(self, node, depth=0, parent=None):
        self._node = node
        self.depth = depth
        self.parent = parent

    @property
    def name(self):
        return self._node.attrib['name']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class GroupNode(Node):

    def __unicode__(self):
        return u"— %s" % self.name


class ItemNode(Node):

    def __unicode__(self):
        return u"+ %s" % self.name


class KeyNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    @property
    def value(self):
        return self._node.attrib['value']

    def __unicode__(self):
        return u"%s => %s" % (self.name, self.value)


class ComboNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    @property
    def values(self):
        return self._node.attrib['values']

    def __unicode__(self):
        return u"%s => %s" % (self.name, self.values)


class TextNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    def __unicode__(self):
        return u"%s => …" % self.name


class CheckNode(Node):

    @property
    def name(self):
        return self._node.attrib['key']

    @property
    def default(self):
        try:
            default = self._node.attrib['default']
        except KeyError:
            default = "no"
        finally:
            return default

    def __unicode__(self):
        on = self.default in ("yes", "on") and "[yes]" or "yes"
        off = self.default in ("no", "off") and "[no]" or "no"
        return u"%s => %s/%s" % (self.name, on, off)


def main(path):
    with open(path) as f:
        content = f.read()
    content = content.replace(' xmlns="', ' xmlnamespace="')
    root = etree.XML(content)
    NODES = []

    def iternode(parent, depth=0):
        for child in parent.getchildren():
            try:
                cls = globals()["%sNode" % child.tag.title()]
            except (AttributeError, KeyError):
                pass
            else:
                node = cls(child, depth)
                NODES.append(node)
                iternode(child, depth=depth+1)
    iternode(root)
    return NODES


def to_txt(nodes, filepath):
    content = ""
    for node in nodes:
        content += "%s%s\n" % (u"\t" * node.depth, unicode(node))
    f = codecs.open(filepath, 'w', "utf-8")
    f.write(content)
    f.close()


def to_csv(nodes, filepath):
    writer = csv.writer(
        open("%s.csv" % filepath, "wb"),
        delimiter=",",
        quotechar='"'
    )
    for node in nodes:
        empty_cells = ["" for e in range(node.depth)]
        row = empty_cells + [node]
        writer.writerow(row)

if __name__ == "__main__":
    args = docopt(__doc__)
    nodes = main(args['<file>'])
    format = args['--format']
    output = args['--output']
    globals()["to_%s" % format](nodes, output)
