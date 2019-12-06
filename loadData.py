
# coding: utf-8
import urllib2, re, os, gzip
from io import BytesIO

#Specify target location for files
folder = "Data"

if not os.path.exists(folder): # Directory that I want to save the image to
    os.mkdir(folder) # If no directory create it

#Source of NWS data
url = "https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
source = urllib2.urlopen(url).read()

#Files we are interested in: data from 1996-2019
zips = re.findall('StormEvents\_(?=fatalities|details|locations).*d(?=199[6-9]|20[0-9][0-9]).*\.gz(?=")',source, re.M)

for z in zips:
    remote = url + z;
    target = folder + "/" 
    
    year = re.findall('(?<=d)[0-9]{4}',z)    #regex matching to find year of data
    if len(year) != 1:
        print "Can't find year of file!): "+z
    else:
        year = year[0]
        
    if "details" in z:    #matching to find type of data
        target += "Details_"+year+".csv"
    elif "fatalities" in z:
        target += "Fatalities_"+year+".csv"
    elif "locations" in z:
        target += "Locations_"+year+".csv"
    else:
        print "Unexpected file (not about details, fatalities, or locations!): "+z
        continue
        
    print "Copying from " + remote + " and unzipping to " + target
    if not os.path.exists(target):
        resp = urllib2.urlopen(remote)
        compressed_file = BytesIO(resp.read())
        
        f = gzip.GzipFile(fileobj=compressed_file, mode='rb')
        s = f.read()
        f.close()

        output = open(target, 'wb')
        output.write(s)
        output.close()
        
print("done!")

