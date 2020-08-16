import Evtx.Evtx as evtx
import Evtx.Views as e_views
import argparse
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
import lxml.etree as etree

file_path = "./evtx.xml"
f = open(file_path, "w")

def main():
    parse_xml(get_xml(get_args()))

def parse_xml(events):
    parsed_events = []
    for event in events:
        parsed_events.append(ET.fromstring(event))    #xmldoc = minidom.parse(file_path)
    return parsed_events
def get_xml(args):
    with evtx.Evtx(args.evtx) as log:
        #f.write(e_views.XML_HEADER)
        #f.write("<Events>\n")
        events = []
        for record in log.records():
            doc_xml = minidom.parseString(record.xml()).toprettyxml(indent="\t", newl="\n", encoding=None)
            events.append(doc_xml)
            #f.write(doc_xml.replace('<?xml version="1.0" ?>\n', '').replace("<", '\t<'))
        #f.write("</Events>")
    return events

def get_args():
    parser = argparse.ArgumentParser(
        description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file")
    return (parser.parse_args())

if __name__ == "__main__":
    main()