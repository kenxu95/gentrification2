
def convertToFloat(x):
  if x == '':
    return 0
  else:
    return float(x)

def getMedianLabel(idx):
  f = open('feature_extraction/images/labels2.csv')
  firstLine = f.readline()
  print 'Statistics for: ' + firstLine.split(',')[idx]

  labels = []
  for line in f:
    labels.append([convertToFloat(x) for x in line.split(',')][idx])

  labels.sort()
  print 'Median: ' + str(labels[len(labels) / 2])
  print 'Average: ' + str(sum(labels) / len(labels))
  return labels[len(labels) / 2]