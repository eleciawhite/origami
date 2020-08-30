import argparse
from xml.dom import minidom

def filter_by_color(parsed_file, keep_color):
    doc = parsed_file
    xml_contents = doc.documentElement 
    lines = xml_contents.getElementsByTagName("line")

    for line in xml_contents.getElementsByTagName("line"):
       color = line.getAttribute("stroke")
       if (color.lower() != keep_color.lower()):
           	xml_contents.removeChild(line)
    return doc

def output_file(parsed_file, output_filename):
    with open(output_filename, "w") as xml_file:
        parsed_file.writexml(xml_file)

def main():
    parser = argparse.ArgumentParser(description='Group svg by colors')
    parser.add_argument("--input", help="input svg file", default=None, required=True)
    parser.add_argument("--output", help="output svg file ending", default=None)
    args = parser.parse_args()

    if args.output is None:
        args.output=args.input

    colors = { 'yellow': '#ffff00', 
              'red':    '#ff0000',
              'blue':   '#0000ff',
              'green':  '#00ff00',
              'black':  '#000000'}

    for color in colors:
        doc = minidom.parse(args.input)
        doc = filter_by_color(doc, colors[color])
        output_file(doc, color+'_'+args.output)


if __name__ == "__main__":
    main()
