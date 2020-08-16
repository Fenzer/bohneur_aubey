import Evtx.Evtx as evtx
import Evtx.Views as e_views
import argparse
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import lxml.etree as etree

file_path = "./evtx.xml"
f = open(file_path, "w")

def main():
    get_xml(get_args())
    parse_xml()

def parse_xml():
    #xmldoc = minidom.parse(file_path)
    tree = ET.ElementTree(file=file_path)
    root = tree.getroot()
    print(root)

def get_xml(args):
    with evtx.Evtx(args.evtx) as log:
        f.write(e_views.XML_HEADER)
        f.write("<Events>\n")
        for record in log.records():
            doc_xml = minidom.parseString(record.xml()).toprettyxml(indent="\t", newl="\n", encoding=None)
            f.write(doc_xml.replace('<?xml version="1.0" ?>\n', '').replace("<", '\t<'))
        f.write("</Events>")

def get_args():
    parser = argparse.ArgumentParser(
        description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file")
    return (parser.parse_args())

if __name__ == "__main__":
    main()