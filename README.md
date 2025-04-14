# Resample

## Usage
The resampler is containerized. In order to use it:

1. Configure

   The file `docker-compose.yml` allows to configure:
   - the target samplerate `SAMPLERATE`
   - define the data to be resampled:
     - from its start `TIME_START`
     - to its end `TIME_END`

2. place the original files in the folder `./data.in/.`
3. execute `$ docker-compose up`
4. find the resampled data in `./data.out/.`

## Quality

This resampling tool uses the samplerate converter developed by Erik de Castro Lopo (http://www.mega-nerd.com/SRC). 
It is configured to use its "sinc_best" interpolator, which Erik describes (see: http://www.mega-nerd.com/SRC/api_misc.html) as follows: 

```
SRC_SINC_BEST_QUALITY - This is a bandlimited interpolator derived from the
mathematical sinc function and this is the highest quality sinc based
converter, providing a worst case Signal-to-Noise Ratio (SNR) of 97 decibels
(dB) at a bandwidth of 97%. All three SRC_SINC_* converters are based on the
techniques of Julius O. Smith although this code was developed independantly. 
```

### Update
In order to get an up to date version of the software:
1. get most recent version from repository

   `$ git pull`

2. the service and build container with updated software

   `$ docker-compose up --build`


---

## Project Description
### Given
The input-files are provided as Excel-Files (`.xlsx`).
- Lines before the line with the headers can be ignored.
- The header line is not line 1.
- The line with the headers can be detected by the first columns data, which is "t(ms)".
- Each line after the header-line is treated as data.
- Columns with no header are ignored.
- All columns beside the first column with the header "t(ms)" are also discarded.

The timestamps start at some value usually around 300 ms.
The end is undefined.
The samplerate is undefined.

### To be determined:
- the original `samplerate` can be derived from the number of samples divided by the overall duration:
  `duration = timeEnd - timeStart`
  `samplerate = numberOfSamples / duration`

### Goal
The output shall contain two columns with resampled data:
  1. data before the timestamp `2500 ms` is dismissed
  2. the last `1000 ms` of data shall also be dismissed
  3. The target samplerate is a configuration parameter, during development: 200 Hz

### Solution

The solution consists of the following steps:
1. convert Excel files to csv - provided by a shell script employing `libreoffice`:
  `$ ./xlsx_to_csv.sh data.in/FILE data.csv/.`

2. resample data provided by a Python script (which relies mainly on the modules `numpy` and `samplerate`):
  `$ ./resample.py data.csv/FILE data.resampled/.`

3. convert csv to Excel - provided by a shell script employing `libreoffice`:
  `$ ./csv_to_xslx.sh data.resampled/FILE ./data.out`

#### The central Script: `convert-in2out.sh`
The script `convert-in2out.sh` automates the process described above. Data files found  in the directory `data.in` is converted and the results are placed in the directory `data.out`.

#### Docker

In order to enhance the portability and make the installation/runtime requirements explicit, the application is containerized.

The file `docker-compose.yml` defines the service `resampler`, mounts the local directories `./data.in` and `./data.out` as volumes inside of the container and defines the command `/app/convert-in2out.sh` to be executed inside of the container.

The built of the resampler service' underlying image is defined in the file `docker.resampler/Dockerfile`.
It bases upon the python image `python:3-slim` and on top of that installs the following prerequisites:
- `$ apt install libreoffice-calc`
- `$ apt install libreoffice-java-common`
- `$ apt install openjdk-11-jre`
- `$ apt install libsamplerate0`
- `$ pip install numpy`
- `$ pip install samplerate`
  http://libsndfile.github.io/libsamplerate/
  [Quality](http://libsndfile.github.io/libsamplerate/quality.html)
  For the samplerate conversion the library "libsamplerate" (aka "Secret Rabbit Code" is used. The converter type 'sinc_best' is chosen, - other types are available (e. g. 'linear', 'sinc_fastest', and others).
- libreoffice to convert between (from/to) `.csv` and `.xlsx`
