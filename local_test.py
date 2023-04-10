import xml.etree.ElementTree as ET

# Define the file path
file_path = '/Users/itaynussbaum/Downloads/discogs_20230301_releases.xml'

# Iterate through elements in the XML file
for event, element in ET.iterparse(file_path, events=('start', 'end')):
    if event == 'start':
        # Process the element at the start event
        print("Start:", element.tag, element.attrib)
    elif event == 'end':
        # Process the element at the end event
        print("End:", element.tag)

    # Clear the element to free up memory
    element.clear()