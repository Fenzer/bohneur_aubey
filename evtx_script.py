import Evtx.Evtx as evtx
import Evtx.Views as e_views
import argparse
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import lxml.etree as etree
import re
import csv

file_path = "./evtx.xml"
f = open(file_path, "w")

def main():
    events = parse_xml(get_xml(get_args()))
    for event in events:
        i = 1
        children = event.getchildren()
        for child in children:
            greatchildren = child.getchildren()
            for greatchild in greatchildren:
                if i == 1:
                    print("tag=%s, attrib=%s" % (re.sub( r"{.*}", "", event.tag), re.sub( r"{.*}", "", event.attrib) if event.attrib else "None"))
                    i = 0
                print("\t%s=%s" % (re.sub(r"{.*}", "", child.tag), child.text))
                print("\t\t%s=%s" % (re.sub( r"{.*}", "", greatchild.tag), greatchild.text))

def parse_xml(events):
    parsed_events = []
    for event in events:
        parsed_events.append(ET.fromstring(event))    #xmldoc = minidom.parse(file_path)
    return parsed_events

def get_xml(args):
    with evtx.Evtx(args.evtx) as log:
        events = []
        for record in log.records():
            doc_xml = minidom.parseString(record.xml()).toprettyxml()
            events.append(doc_xml)
    return events

def get_args():
    parser = argparse.ArgumentParser(
        description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file")
    return (parser.parse_args())

if __name__ == "__main__":
    main()