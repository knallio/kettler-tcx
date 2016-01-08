from lxml import etree

GARMIN_URL="http://www.garmin.com/xmlschemas/"

#TODO:
#xsi:schemaLocation=GARMIN_URL+"TrainingCenterDatabase/v2 "+GARMIN_URL+"TrainingCenterDatabasev2.xsd"

XML_NS="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
XSI_NS="http://www.w3.org/2001/XMLSchema-instance"
XSD_NS="http://www.w3.org/2001/XMLSchema"
NS2_NS="http://www.garmin.com/xmlschemas/ActivityExtension/v2"

NS_MAP={None: XML_NS, "xsi": XSI_NS, "xsd": XSD_NS , "ns2": NS2_NS}


tcx = etree.Element("TrainingCenterDatabase" , nsmap=NS_MAP)
activities = etree.SubElement(tcx, "Activities")

activity=etree.SubElement(activities, "Activity", Sport="Other")
time=etree.SubElement(activity, "Id")
time.text="2015"

lap=etree.SubElement(activity, "Lap", StartTime="2015")

etree.SubElement(lap, "TotalTimeSeconds").text="5"
etree.SubElement(lap, "DistanceMeters").text="100"
etree.SubElement(lap, "MaximumSpeed").text="1.0"
etree.SubElement(lap, "Calories").text="100"
etree.SubElement(lap, "Intensity").text="Active"
etree.SubElement(lap, "TriggerMethod").text="Manual"
track=etree.SubElement(lap, "Track")

etree.SubElement(track, "Trackpoint")

tree = etree.ElementTree(tcx)
tree.write("filename.xml",pretty_print=True, xml_declaration=True,encoding='utf-8')


#print(etree.tostring(root,pretty_print=True, xml_declaration=True))



