#!/usr/bin/env python3

import requests, json, os, argparse, exifread, sys, shutil, hashlib, time, itertools
from lxml import etree as ET

parser = argparse.ArgumentParser(
	description="Finds all pictures given a source, extracts GPS data and asks LocationIQ for location data. Optionally, save picture data to KML format to import into your favorite mapping software.\
	Optionally, sort your photos and store them in corresponding Country/City/State directory structure. It will even rename your picture if a point of interest (POI) is found.",
)
parser.add_argument('-s','--source', action='store',
					dest='source', required=True,
					help='This is the source directory to begin search for pictures')
parser.add_argument('-d','--destination', action='store',
					dest='destination',
					help='This is the destination directory to move pictures. If none is provided, verbose is set to true')
parser.add_argument('-k','--key', action='store',
					dest='key', required=True,
					help='This is the LocationIQ API Key. Visit https://locationiq.com/ to get a free API key (10K requests/day)')
parser.add_argument('-m','--kml', action='store',
					dest='kml',
					help='This is the KML file for importing into Google Earth/Maps and database for picture hashes.')
parser.add_argument('-v','--verbose', action='store_true',
					dest='verbose',
					help='This boolean flag will trigger all response data from the API to stdout')
parser.add_argument('-l','--location', action='store_true',
					dest='location',
					help='This boolean flag will trigger the file location in the KML')
args = parser.parse_args()

hasher = hashlib.sha1()
headers = {}
headers['Content-Type'] = 'application/json'
root_url = 'https://us1.locationiq.com/v1/reverse.php?format=json&normalizecity=1&normalizeaddress=1&key=' + args.key + '&'
places = []
tagged = []
re_ext = ["jpg", "jpeg", "JPG", "JPEG"]

base_kml = [
'<kml>\n',
'  <Document>\n',
"    <name>Where We've Been</name>\n",
'    <Style id="pin">\n',
'      <IconStyle>\n',
'        <scale>3</scale>\n',
'        <Icon>\n',
'          <href>http://maps.google.com/mapfiles/ms/micons/red-dot.png</href>\n',
'        </Icon>\n',
'        <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n',
'      </IconStyle>\n',
'    </Style>\n',
'    <Folder name="NW">\n',
'      <name>Northwest</name>\n',
'    </Folder>\n',
'    <Folder name="NE">\n',
'      <name>Northeast</name>\n',
'    </Folder>\n',
'    <Folder name="SW">\n',
'      <name>Southwest</name>\n',
'    </Folder>\n',
'    <Folder name="SE">\n',
'      <name>Southeast</name>\n',
'    </Folder>\n',
'  </Document>\n',
'</kml>'
]

def get_kml():
	tree = ET.parse(args.kml)
	return tree.getroot()

def dms_to_dd(coord, direction):
	d = float(coord.values[0].num) / float(coord.values[0].den)
	m = float(coord.values[1].num) / float(coord.values[1].den)
	s = float(coord.values[2].num) / float(coord.values[2].den)
	
	if (str(direction) == 'S') or (str(direction) == 'W'):
		return -(d + (m / 60.0) + (s / 3600.0))
	else:
		return d + (m / 60.0) + (s / 3600.0)
		
def normalize(location):
	city_or_state, state_or_country, poi = ("" for l in range(3))
	data = {}
	if location['country'] == 'United States of America' or location['country'] == 'United Kingdom':
		if 'city' in location:
			city_or_state = location['city']
		else:
			city_or_state = "Unknown"
		if 'state' in location:
			state_or_country = location['state']
		else:
			state_or_country = "Unknown"
	else:
		if 'city' in location and location['city'] != location['country']: # this logic was added for: Vatican City, Vatican City'
			city_or_state = location['city']
		elif 'state' in location and location['state'] != location['country']: # this logic was added for: Vatican City, Vatican City'
			city_or_state = location['state']
		else:
			city_or_state = "Unknown"
		state_or_country = location['country']
	if 'name' in location:
			poi = location['name']
	
	data['city_or_state'] = city_or_state
	data['state_or_country'] = state_or_country
	data['poi'] = poi
		
	return data
	
def increment_file(path):
    yield path
    prefix, ext = os.path.splitext(path)
    for i in itertools.count(start=2, step=1):
        yield prefix + ' ({0})'.format(i) + ext

if args.kml:
	if not os.path.isfile(args.kml):
		file = open(args.kml, 'w')
		file.writelines(base_kml)
		file.close()
	parser = ET.XMLParser(remove_blank_text=True)
	tree = ET.parse(args.kml, parser)
	kml = tree.getroot()
	document = kml.find("Document")
	for folder in document.findall("Folder"):
		if folder.attrib['name'] == "NW":
			NW = folder
		elif folder.attrib['name'] == "NE":
			NE = folder
		elif folder.attrib['name'] == "SW":
			SW = folder
		elif folder.attrib['name'] == "SE":
			SE = folder
		
		for pm in folder.findall("Placemark"):
			if pm[0].text not in places:
				places.append(pm[0].text)
	
	if os.path.isfile(args.kml + ".db"):
		with open(args.kml + ".db", "r") as tagged_db:
			for tag in tagged_db:
				tagged.append(tag.strip())
	tagged_start = len(tagged)
	print("[Info] Imported {} photos into already tagged list".format(tagged_start))

	tagged_db = open(args.kml + ".db", "a")

total_pictures = 0
count_pictures = 0	
print('[Info] Counting pictures to be processed...')
for root, dirs, files in os.walk(args.source):
	for filename in files:
		if filename.endswith(tuple(re_ext)):
			total_pictures += 1

print('[Info] {} picture(s) found'.format(total_pictures))
for root, dirs, files in os.walk(args.source):
	for filename in files:
		if filename.endswith(tuple(re_ext)):
			base_name, file_ext = os.path.splitext(filename)
			path_to_picture = os.path.abspath(root)
			count_pictures += 1
			file = open(os.path.join(root,filename), 'rb')
			buf = file.read()
			hasher.update(buf)
			tags = exifread.process_file(file, details=False)
			file.close()
			sha1 = hasher.hexdigest()
			
			sys.stdout.write('[{}/{}] '.format(count_pictures,total_pictures))
			
			if sha1 in tagged:
				try:
					print('[Skip] {} has already been processed'.format(os.path.join(root,filename)))
				except:
					print('[Program Error] could not print filename in {}'.format(root))
			else:
				if ('GPS GPSLatitude' in tags) and ('GPS GPSLatitudeRef' in tags) and ('GPS GPSLongitude' in tags) and ('GPS GPSLongitudeRef' in tags):
					date_taken = str(tags['EXIF DateTimeOriginal'])
					year = date_taken.split(':')[0]
					dir_quad = str(tags['GPS GPSLatitudeRef']) + str(tags['GPS GPSLongitudeRef'])
					lat = dms_to_dd(tags['GPS GPSLatitude'], tags['GPS GPSLatitudeRef'])
					lon = dms_to_dd(tags['GPS GPSLongitude'], tags['GPS GPSLongitudeRef'])

					response = requests.get(root_url + "lat=" + str(lat) + '&' + "lon=" + str(lon), headers=headers).json()
					
					if 'error' in response and response['error'] == 'Rate Limited Second':
						while 'error' in response and response['error'] == 'Rate Limited Second':
							print("[Info] Rate Limited..")
							sys.stdout.write('[{}/{}] '.format(count_pictures,total_pictures))
							time.sleep(1)
							response = requests.get(root_url + "lat=" + str(lat) + '&' + "lon=" + str(lon), headers=headers).json()
						
					if 'error' in response and response['error'] == "Invalid Request":
						print("[Err ] {} | Bad Coordinates: {},{}".format(os.path.join(root,filename), lat, lon))
					elif 'address' in response:
						normalized = normalize(response['address'])
						poi = normalized['poi']
						city_or_state = normalized['city_or_state']
						state_or_country = normalized['state_or_country']
						if poi != "":
							place_name = "({}) {}, {} - {}".format(poi, city_or_state, state_or_country, year)
						else:
							place_name = "{}, {} - {}".format(city_or_state, state_or_country, year)
						print('[Info] {} | {}'.format(os.path.join(root,filename), place_name))
						
						if args.verbose:
							print(json.dumps(response, indent=2))
						
						if args.destination:
							sys.stdout.write('[{}/{}] '.format(count_pictures,total_pictures))
							if response['address']['country'] == "United States of America":
								destination_path = os.path.join(args.destination,"United States",state_or_country,city_or_state)
							else:
								destination_path = os.path.join(args.destination,state_or_country,city_or_state)
							if not os.path.exists(destination_path):
								os.makedirs(destination_path)

							if poi != "":
								destination_file = poi + file_ext
							else:
								destination_file = filename
							for uniq_filename in increment_file(os.path.join(destination_path,destination_file)):
								if not os.path.exists(uniq_filename):
									try:
										shutil.move(os.path.join(root,filename),uniq_filename)
										path_to_picture = os.path.abspath(destination_path)
										print("[Info] Moved {} to {}".format(os.path.join(root,filename), uniq_filename))
									except shutil.Error as error:
										print('[Err] {}'.format(error))
									break
										
						
						if args.kml:
							sys.stdout.write('[{}/{}] '.format(count_pictures,total_pictures))
							if place_name not in places:
								if args.location:
									detailed_desc = "Date Taken: {}\n\n{}\n\n{}\n".format(date_taken, path_to_picture, json.dumps(response['address'], indent=2))
								else:
									detailed_desc = "Date Taken: {}\n\n{}\n".format(date_taken, json.dumps(response['address'], indent=2))
								placemark = ET.Element("Placemark")
								name = ET.Element("name")
								name.text = place_name
								placemark.append(name)
								description = ET.Element("description")
								description.text = detailed_desc
								placemark.append(description)
								style = ET.Element("styleUrl")
								style.text = '#pin'
								placemark.append(style)
								point = ET.Element("Point")
								coord = ET.Element("coordinates")
								coord.text = str(lon) + ',' + str(lat)
								point.append(coord)
								placemark.append(point)
								
								if dir_quad == "NW":
									NW.append(placemark)
								elif dir_quad == "NE":
									NE.append(placemark)
								elif dir_quad == "SW":
									SW.append(placemark)
								elif dir_quad == "SE":
									SE.append(placemark)
									
								places.append(place_name)
							
								tree.write(args.kml, encoding='utf-8', pretty_print=True)
								print('[Info] {} added to KML'.format(os.path.join(root,filename)))
							else:
								print('[Skip] {} has already been tagged in KML'.format(os.path.join(root,filename)))
							tagged_db.write(sha1 + "\n")
						
						tagged.append(sha1)
						
						
					else:
						print('[Err ] {} | Unexpected response'.format(os.path.join(root,filename)))
				else:
					print('[Warn] {} does not have GPS coordinates'.format(os.path.join(root,filename)))

if args.kml:
	tagged_db.close()
	print("[Info] Tagged {} new photos to {}".format(len(tagged) - tagged_start, args.kml + ".db"))
				
	def getkey(elem):
		return elem.findtext("name")
					
	for folder in document.findall("Folder"):
		folder_name = folder.findtext('name')
		folder_attr = folder.attrib['name']

		container = folder.findall("Placemark")
		container[:] = sorted(container, key=getkey)
		print("[Info] Sorting {} places in the {} ".format(len(container), folder_name))
		document.remove(folder)
		folder = ET.Element('Folder')
		folder.set('name', folder_attr)
		name = ET.Element('name')
		name.text = folder_name
		folder.append(name)
		for elem in container:
			folder.append(elem)
		document.append(folder)
		
		tree.write(args.kml, encoding='utf-8', pretty_print=True)
	print("[Info] Wrote KML to {}".format(os.path.abspath(args.kml)))

