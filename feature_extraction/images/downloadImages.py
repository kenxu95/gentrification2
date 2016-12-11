import os
import sys
import urllib2
import math
from PIL import Image
import StringIO
from matplotlib import pyplot as plt
from collections import defaultdict

URL_PREFIX = "https://api.mapbox.com/v4/digitalglobe.nal0g75k/"
URL_SUFFIX = ".png?access_token=pk.eyJ1IjoiZGlnaXRhbGdsb2JlIiwiYSI6ImNpdzhmNWFxMTAxd3IyeXBvdTB6dXZldWYifQ.MA1bofL4EsEJsKBUqmgUpg"
SIZE = 256
ZOOM_LEVEL = 16 # Default zoom level - can change if need be

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

def getTileIndexes(z, lon1, lat1, lon2, lat2):
  xstart = xFromLon(z, lon1)
  ystart = yFromLat(z, lat1)
  xend = xFromLon(z, lon2)
  yend = yFromLat(z, lat2)
  if xstart > xend:
    xstart, xend = xend, xstart
  if ystart > yend:
    ystart, yend = yend, ystart
  return xstart, ystart, xend, yend

def downloadRegion(z, lon1, lat1, lon2, lat2, regionName):
  xstart, ystart, xend, yend = getTileIndexes(ZOOM_LEVEL, lon1, lat1, lon2, lat2)

  # Piece the images together
  numWidth = xend - xstart + 1
  numHeight = yend - ystart + 1
  img = Image.new('RGB', (numWidth * SIZE, numHeight * SIZE))
  for y in xrange(yend - ystart + 1):
    for x in xrange(xend - xstart + 1):
      img.paste(downloadImage(z, x + xstart, y + ystart), (x * SIZE, y * SIZE))
  img.save(regionName + ".png")

# IMPORTANT: Downloads a bunch of images!!
def downloadImages():
  f = open('labels.csv')
  lines = []
  f.readline()
  for line in f:
    lines.append([float(x.strip()) for x in line.split(',')])
  f.close()

  # Sort by size
  def sortByTile(elem):
    return numTiles(elem[-3], elem[-4], elem[-1], elem[-2])
  lines.sort(key=sortByTile)

  # DOWNLOAD THE IMAGES IN THE FILE
  for i in xrange(len(lines)):
    if i > 508 and i <= 1000:
      lat1, lon1, lat2, lon2 = lines[i][-4:]
      downloadRegion(ZOOM_LEVEL, lon1, lat1, lon2, lat2, str(int(lines[i][0])))
      print str(i) + "th zip code has been downloaded!"

  # numTilesArr = []
  # for i in xrange(len(lines)):
  #   if i < 1000:
  #     lat1, lon1, lat2, lon2 = lines[i][-4:]
  #     numTilesArr.append(numTiles(lon1, lat1, lon2, lat2))
  # print "Num tiles needed: " + str(sum(numTilesArr))


# ASSESS HOW MANY IMAGES ARE NEEDED
# Helper function: Counts the number of tiles needed for a particular long/lat box
def numTiles(lon1, lat1, lon2, lat2):
  xstart, ystart, xend, yend = getTileIndexes(ZOOM_LEVEL, lon1, lat1, lon2, lat2)
  return (xend - xstart + 1) * (yend - ystart + 1)

def calcNumTilesNeeded():
  f = open('labels.csv')
  numLines = 0
  tiles = []
  f.readline() # Header line
  for line in f:
    lat1, lon1, lat2, lon2 = [float(x.strip()) for x in line.split(',')[-4:]]
    numLines = numLines + 1 
    tiles.append(numTiles(lon1, lat1, lon2, lat2))
  f.close()

  tiles.sort()
  print "Total number of tiles needed: " + str(sum(tiles))
  print "Average number of tiles needed: " + str(sum(tiles) / numLines)
  print "Median of tiles per zip code: " + str(tiles[len(tiles) / 2])

  tiles = [0.302 * x for x in tiles]
  tilesHist = defaultdict(int)
  for elem in tiles:
    tilesHist[elem - (elem % 10)] += 1

  xAxes = [x for x in sorted(tilesHist.keys()) if x < 250]
  yAxes = []
  for x in xAxes:
    yAxes.append(tilesHist[x])

  # plt.figure()
  # plt.title("Distribution of Zip Code Sizes in USA")
  # plt.xlabel("Square Miles")
  # plt.ylabel("# of Zip Codes")
  # plt.plot(xAxes, yAxes)
  # plt.show()

# calcNumTilesNeeded()
# downloadImages()

# CODE START
longitude1 = float(sys.argv[1])
latitude1 = float(sys.argv[2])
longitude2 = float(sys.argv[3])
latitude2 = float(sys.argv[4])
outputName = sys.argv[5]
if (len(sys.argv) == 4):
  downloadRegion(ZOOM_LEVEL, float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
else:
  downloadRegion(ZOOM_LEVEL, float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5])




