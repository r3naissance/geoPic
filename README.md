# GeoPic
A tool to see where you've been, help organize, and map your photos

![World](https://github.com/r3naissance/GeoPic/blob/master/images/world.gif)

## API Key Required
Visit https://locationiq.com/ to sign up for a free API key. It is valid for 10,000 requests per day.

## Installation
```
git clone --depth 1 https://github.com/r3naissance/GeoPic
cd GeoPic
python3 -m pip install -r requirements.txt
./geo.py -h
```

## Usage
```
usage: geo.py [-h] -s SOURCE [-d DESTINATION] -k KEY [-m KML] [-v] [-l]

Finds all pictures given a source, extracts GPS data and asks LocationIQ for location data. Optionally, save picture
data to KML format to import into your favorite mapping software. Optionally, sort your photos and store them in
corresponding Country/City/State directory structure. It will even rename your picture if a point of interest (POI) is
found.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        This is the source directory to begin search for pictures
  -d DESTINATION, --destination DESTINATION
                        This is the destination directory to move pictures. If none is provided, verbose is set to
                        true
  -k KEY, --key KEY     This is the LocationIQ API Key. Visit https://locationiq.com/ to get a free API key (10K
                        requests/day)
  -m KML, --kml KML     This is the KML file for importing into Google Earth/Maps and database for picture hashes.
  -v, --verbose         This boolean flag will trigger all response data from the API to stdout
  -l, --location        This boolean flag will trigger the file location in the KML
```

### -s, --source [Required]
Directory to recursively look for pictures
```
./geo.py -s /home/user/pictures/
./geo.py -s c:\Users\user\Pictures\
```
### -k, --key [Required]
LocationIQ API Key
```
./geo.py -k 982gdsv67dguy
```
### -d, --destination
If you want GeoPic to organize your pictures for you based on location data, this parameter should tells GeoPic where to create sub-folders and move pictures
```
./geo.py -d /mnt/nas/scrapbook
./geo.py -d "d:\My Scrapbook"
```
### -m, --kml
If you want to save your picture data to KML format, this parameter should be used to tell GeoPic where to save your KML.
If you use this option, GeoPic will also create a list of hashes (same as kml file but with "db" at the end) that it has already processed in an attempt to avoid duplicates.
Additionally, this option will see if the location data/POI and year aleady exist in the KML. If it does, it won't create a new data point but if it doesn't, it will.
```
./geo.py -m /home/user/pics.kml
./geo.py -m c:\Users\user\pictures.kml
```
### -v, --verbose
This option will show you the json that returns from LocationIQ which has more information than what is extracted by GeoPic. Usually used if the location/POI data is returning with strange/incorrect results.
```
./geo.py -v
```
### -l, --location
This option will save where the picture is located in the KML. This was added so that while exploring your map in Google Earth and you select a pin, the data that is returned will include where the picture is stored so you know where to find the original.
```
./geo.py -l
```
### Putting it all together
If you want to simply output where the pictures were taken but nothing else:
```
./geo.py -s c:\temp -k ncba72387rhfbj67serf
[Info] Counting pictures to be processed...
[Info] 4 pictures found
[1/4] [Info] c:\temp\DSC00366.JPG | (Sunset viewpoint) Siem Reap, Cambodia - 2019
[2/4] [Info] c:\temp\E42398234.JPG | Hortonville, Wisconsin - 2015
[3/4] [Info] Rate Limited..
[3/4] [Info] c:\temp\E7619453.JPG | (Champ de Mars) Paris, France - 2013
[4/4] [Info] c:\temp\T74982324.JPG | Addis Ababa, Ethiopia - 2014
```
If you want to organize the pictures:
```
./geo.py -s c:\temp -k ncba72387rhfbj67serf -d x:\Pictures
[Info] Counting pictures to be processed...
[Info] 4 pictures found
[1/4] [Info] c:\temp\DSC3545673457.JPG | (Sunset viewpoint) Siem Reap, Cambodia - 2019
[1/4] [Info] Moved c:\temp\DSC3545673457.JPG to x:\Pictures\Cambodia\Siem Reap\Sunset viewpoint.JPG
[2/4] [Info] c:\temp\E42398234.JPG | Hortonville, Wisconsin - 2015
[2/4] [Info] Moved c:\temp\E42398234.JPG to x:\Pictures\United States\Wisconsin\Hortonville\E42398234.JPG
[3/4] [Info] Rate Limited..
[3/4] [Info] c:\temp\E53456475.JPG | (Champ de Mars) Paris, France - 2013
[3/4] [Info] Moved c:\temp\E53456475.JPG to x:\Pictures\France\Paris\Champ de Mars.JPG
[4/4] [Info] c:\temp\T74982324.JPG | Addis Ababa, Ethiopia - 2014
[4/4] [Info] Moved c:\temp\T74982324.JPG to x:\Pictures\Ethiopia\Addis Ababa\T74982324.JPG
```
If you want to organize, create a KML file, store the location of the picture, and see verbose output:
```
./geo.py -s c:\temp -k 9872gfg8cbv8fbfgs82313r -d x:\Pictures -m x:\pics.kml -l -v
[Info] Counting pictures to be processed...
[Info] 4 pictures found
[1/4] [Info] c:\temp\DSC3545673457.JPG | (Sunset viewpoint) Siem Reap, Cambodia - 2019
[1/4] [Info] Moved c:\temp\DSC3545673457.JPG to x:\Pictures\Cambodia\Siem Reap\Sunset viewpoint.JPG
[2/4] [Info] c:\temp\E42398234.JPG | Hortonville, Wisconsin - 2015
[2/4] [Info] Moved c:\temp\E42398234.JPG to x:\Pictures\United States\Wisconsin\Hortonville\E42398234.JPG
[3/4] [Info] Rate Limited..
[3/4] [Info] c:\temp\E53456475.JPG | (Champ de Mars) Paris, France - 2013
[3/4] [Info] Moved c:\temp\E53456475.JPG to x:\Pictures\France\Paris\Champ de Mars.JPG
[4/4] [Info] c:\temp\T74982324.JPG | Addis Ababa, Ethiopia - 2014
[4/4] [Info] Moved c:\temp\T74982324.JPG to x:\Pictures\Ethiopia\Addis Ababa\T74982324.JPG

C:\Users\r3naissance\Google Drive>
C:\Users\r3naissance\Google Drive>
C:\Users\r3naissance\Google Drive>
C:\Users\r3naissance\Google Drive>geo.py -k 0b77c1e8b5fba9 -s c:\temp -d x:\Pictures -m x:\pics.mkl -l -v
[Info] Imported 0 photos into already tagged list
[Info] Counting pictures to be processed...
[Info] 4 pictures found
[1/4] [Info] c:\temp\E3465475.JPG | (Champ de Mars) Paris, France - 2013
{
  "place_id": "82120272",
  "licence": "https://locationiq.com/attribution",
  "osm_type": "way",
  "osm_id": "4208595",
  "lat": "48.85614465",
  "lon": "2.29782039332223",
  "display_name": "Champ de Mars, Avenue du Docteur Brouardel, Quartier du Gros-Caillou, Paris, Paris, Ile-de-France, 75007, France",
  "address": {
    "name": "Champ de Mars",
    "road": "Avenue du Docteur Brouardel",
    "suburb": "Quartier du Gros-Caillou",
    "city": "Paris",
    "county": "Paris",
    "state": "Ile-de-France",
    "postcode": "75007",
    "country": "France",
    "country_code": "fr"
  },
  "boundingbox": [
    "48.8522459",
    "48.8600801",
    "2.2918711",
    "2.303791"
  ]
}
[1/4] [Info] Moved c:\temp\E3465475.JPG to x:\Pictures\France\Paris\Champ de Mars.JPG
[1/4] [Info] c:\temp\E3465475.JPG added to KML
[2/4] [Info] c:\temp\E42398234.JPG | Hortonville, Wisconsin - 2015
{
  "place_id": "332192677444",
  "licence": "https://locationiq.com/attribution",
  "lat": "44.328329",
  "lon": "-88.63919",
  "display_name": "652, S Nash Street, Hortonville, Outagamie County, Wisconsin, 54944, USA",
  "boundingbox": [
    "44.328329",
    "44.328329",
    "-88.63919",
    "-88.63919"
  ],
  "importance": 0.2,
  "address": {
    "house_number": "652",
    "road": "S Nash Street",
    "city": "Hortonville",
    "county": "Outagamie County",
    "state": "Wisconsin",
    "postcode": "54944",
    "country": "United States of America",
    "country_code": "us"
  }
}
[2/4] [Info] Moved c:\temp\E42398234.JPG to x:\Pictures\United States\Wisconsin\Hortonville\E42398234.JPG
[2/4] [Info] c:\temp\E42398234.JPG added to KML
[3/4] [Info] c:\temp\T634563456.JPG | (Sunset viewpoint) Siem Reap, Cambodia - 2019
{
  "place_id": "278535466",
  "licence": "https://locationiq.com/attribution",
  "osm_type": "node",
  "osm_id": "7263335486",
  "lat": "13.4270801",
  "lon": "103.8594615",
  "display_name": "Sunset viewpoint, Tonle Om Gate, Siem Reap, Siem Reap, 17262, Cambodia",
  "address": {
    "name": "Sunset viewpoint",
    "road": "Tonle Om Gate",
    "city": "Siem Reap",
    "state": "Siem Reap",
    "postcode": "17262",
    "country": "Cambodia",
    "country_code": "kh"
  },
  "boundingbox": [
    "13.4269801",
    "13.4271801",
    "103.8593615",
    "103.8595615"
  ]
}
[3/4] [Info] Moved c:\temp\T634563456.JPG to x:\Pictures\Cambodia\Siem Reap\Sunset viewpoint.JPG
[3/4] [Info] c:\temp\T634563456.JPG added to KML
[4/4] [Info] c:\temp\T74982324.JPG | Addis Ababa, Ethiopia - 2014
{
  "place_id": "157539233",
  "licence": "https://locationiq.com/attribution",
  "osm_type": "way",
  "osm_id": "301735351",
  "lat": "8.98004838367508",
  "lon": "38.791285960908",
  "display_name": "Bole, Bole, Addis Ababa, 1044, Ethiopia",
  "address": {
    "suburb": "Bole",
    "county": "Bole",
    "state": "Addis Ababa",
    "postcode": "1044",
    "country": "Ethiopia",
    "country_code": "et"
  },
  "boundingbox": [
    "8.9789062",
    "8.9819886",
    "38.7874299",
    "38.7979601"
  ]
}
[4/4] [Info] Moved c:\temp\T74982324.JPG to x:\Pictures\Ethiopia\Addis Ababa\T74982324.JPG
[4/4] [Info] c:\temp\T74982324.JPG added to KML
[Info] Tagged 4 new photos to x:\pics.kml.db
[Info] Sorting 1 places in the Northwest
[Info] Sorting 3 places in the Northeast
[Info] Sorting 0 places in the Southwest
[Info] Sorting 0 places in the Southeast
[Info] Wrote KML to x:\pics.kml
```
The above would create a map that looks like this:

![Sample](https://github.com/r3naissance/GeoPic/blob/master/images/sample-France.png)
