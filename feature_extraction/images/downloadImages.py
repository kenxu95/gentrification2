import os
import sys
import urllib2
import math
from PIL import Image
import StringIO

URL_PREFIX = "https://api.mapbox.com/v4/digitalglobe.nal0g75k/"
URL_SUFFIX = ".png?access_token=pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpdzhmNWFxMTAxd3IyeXBvdTB6dXZldWYifQ.MA1bofL4EsEJsKBUqmgUpg"
SIZE = 256

def downloadImage(z, x, y):
  url_args = str(z) + "/" + str(x) + "/" + str(y)
  str_img = urllib2.urlopen(URL_PREFIX + url_args + URL_SUFFIX).read()

  # Convert string to an image
  tempBuff = StringIO.StringIO()
  tempBuff.write(str_img)
  tempBuff.seek(0)
  return Image.open(tempBuff)

def xFromLon(z, lon):
  return int(math.floor(math.pow(2, z) * ((lon + 180) / 360)))

def yFromLat(z, lat):
  return int(math.floor(math.pow(2, z-1) * (1 - (math.log(math.tan(lat * math.pi / 180) + 1 / math.cos(lat * math.pi / 180))/ math.pi))))

def downloadRegion(lon1, lat1, lon2, lat2, regionName):
  z = 16 # Default zoom level - can change if need be
  xstart = xFromLon(z, lon1)
  ystart = yFromLat(z, lat1)
  xend = xFromLon(z, lon2)
  yend = yFromLat(z, lat2)

  if (xstart > xend):
    xstart, xend = xend, xstart
  if (ystart > yend):
    ystart, yend = yend, ystart

  # Piece the images together
  numWidth = xend - xstart + 1
  numHeight = yend - ystart + 1
  img = Image.new('RGB', (numWidth * SIZE, numHeight * SIZE))
  for y in xrange(yend - ystart + 1):
    for x in xrange(xend - xstart + 1):
      img.paste(downloadImage(z, x + xstart, y + ystart), (x * SIZE, y * SIZE))
  img.save(regionName + ".png")


# CODE START
longitude1 = float(sys.argv[1])
latitude1 = float(sys.argv[2])
longitude2 = float(sys.argv[3])
latitude2 = float(sys.argv[4])
outputName = sys.argv[5]
if (len(sys.argv) == 4):
  downloadRegion(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
else:
  downloadRegion(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])




