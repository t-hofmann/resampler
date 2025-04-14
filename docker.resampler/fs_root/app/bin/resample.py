#!/usr/bin/env python3

import os.path
import sys

import numpy as np
import samplerate  # https://pypi.org/project/samplerate/

SAMPLERATE_OUT = float(os.environ["SAMPLERATE_OUT"]) # Hz
TIME_START=float(os.environ["TIME_START"])
TIME_END=float(os.environ["TIME_END"])

TIME_RESAMPLED_START = 300 # ms

if len(sys.argv) != 3:
    print("error: wrong number of commandline parameters")
    print("usage:")
    print(sys.argv[0], "FILE_IN DIR_OUT")
    sys.exit(1)

fileIn = sys.argv[1]
dirOut = sys.argv[2]

fileOut = dirOut + '/' + os.path.basename(fileIn)

def findIndexOfRowWithHeaders(data):
    '''findIndexOfRowWithHeaders returns the index of the first row where the first
       field has the value "t(ms)"
    '''
    index=-1
    for row in data:
        index+=1
        cell = row[0]
        if cell == "t(ms)":
            return index

    print("error: row with column headlines not found")
    sys.exit(1)

def cleanupData(dataRaw):
    '''cleanupData removes any row before the row with the headers and
       - each column without a header
       - and each column with the header "t(ms)" if it is not the first column

       assumptions:
       - column 1 is always "t(ms)"
       - columns without a header are senseless and can be deleted
    '''
    indexOfRowWithHeaders = findIndexOfRowWithHeaders(dataRaw)
    data = dataRaw[indexOfRowWithHeaders:] # delete rows until and excluding headers

    columnsToBeDeleted = []
    col=-1
    for header in data[0]:
        col+=1
        if col == 0 and header != "t(ms)":
            print("error: first column is expected to be 't(ms)")
            sys.exit(1)
        if header == "": # no header => delete col
            columnsToBeDeleted.append(col)
        if col > 0 and header == "t(ms)": # duplicate => delete col
            columnsToBeDeleted.append(col)

    columnsToBeDeleted.reverse() # must be deleted in reverse order, because it works on the data itself and would change the index of the actual columns in question
    for col in columnsToBeDeleted:
        data = np.delete(data, col, 1)

    return data

dataRaw = np.loadtxt(fileIn, delimiter=",", dtype=str)
print()
print("*** data raw ***")
print(dataRaw[0:3])

dataClean = cleanupData(dataRaw)
print()
print("*** data clean ***")
print(dataClean[0:3])
print()

columnHeaders = dataClean[0]

# leave away first line "column-headers"
# then transpose (.T)
# and convert type
dataIn = dataClean[1:].T.astype(float)

timestampsIn = dataIn[0]
timeStart = timestampsIn[0]
timeEnd = timestampsIn[-1]
duration = timeEnd - timeStart

numberOfSamplesIn = len(dataIn[0])
samplerateIn = 1000 * numberOfSamplesIn / duration

dataResampled = []

# list of available converter types:
# print(list(samplerate.converters.ConverterType))
CONVERTER = 'sinc_best'  # or 'sinc_fastest', ...
conversionRatio = samplerateIn / SAMPLERATE_OUT

col=-1
# resample data:
for data in dataIn:
    col+=1
    if col==0: # skip first column "t(ms)"
        continue

    valuesOut = samplerate.resample(data, 1/conversionRatio, CONVERTER)
    dataResampled.append(valuesOut)

numberOfSamplesOut = len(dataResampled[0])
timestampsOut = np.arange(numberOfSamplesOut)

# add time axis:
timeBetweenSamplesOut = 1000 / SAMPLERATE_OUT # ms
timestampsOut = timestampsOut * timeBetweenSamplesOut
timestampsOut = timestampsOut + TIME_RESAMPLED_START
dataResampled.insert(0, timestampsOut)

dataResampled = np.array(dataResampled).T

print()
print("*** data resampled ***")
print(dataResampled[0:3])
print()


dataFiltered = dataResampled[(
    (dataResampled[:,0] > TIME_START)
    & (dataResampled[:,0] <= TIME_END)
)]

dataFiltered = np.concatenate(([columnHeaders], dataFiltered), axis=0)

np.savetxt(fileOut, dataFiltered, delimiter=',', fmt='%s')
