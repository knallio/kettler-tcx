from lxml import etree

class tcx:
	#Namespaces:
	XML_NS="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
	XSI_NS="http://www.w3.org/2001/XMLSchema-instance"
	XSD_NS="http://www.w3.org/2001/XMLSchema"
	NS2_NS="http://www.garmin.com/xmlschemas/ActivityExtension/v2"
	#Schemalocation:
	XML_SCHEMA="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"


	def __init__(self):
		NS_MAP={None: self.XML_NS, "xsi": self.XSI_NS, "xsd": self.XSD_NS , "ns2": self.NS2_NS}
		self.tcx = etree.Element("TrainingCenterDatabase" , nsmap=NS_MAP)
		self.tcx.set("{%s}schemaLocation" % self.XSI_NS, self.XML_SCHEMA)

		self.activities = etree.SubElement(self.tcx, "Activities")

	def add_activity(self):
		self.activity=etree.SubElement(self.activities, "Activity", Sport="Other")
		time=etree.SubElement(self.activity, "Id")
		time.text="2015"

		self.lap=etree.SubElement(self.activity, "Lap", StartTime="2015")

		etree.SubElement(self.lap, "TotalTimeSeconds").text="5"
		etree.SubElement(self.lap, "DistanceMeters").text="100"
		etree.SubElement(self.lap, "MaximumSpeed").text="1.0"
		etree.SubElement(self.lap, "Calories").text="100"
		etree.SubElement(self.lap, "Intensity").text="Active"
		etree.SubElement(self.lap, "TriggerMethod").text="Manual"
		self.track=etree.SubElement(self.lap, "Track")

	def add_trackpoint(self):

		etree.SubElement(self.track, "Trackpoint")

	def write_xml(self,filename):
		tree = etree.ElementTree(self.tcx)
		tree.write(filename,pretty_print=True, xml_declaration=True,encoding='utf-8')



workout=tcx()
workout.add_activity()
workout.add_trackpoint()

workout.write_xml("filename.xml")
