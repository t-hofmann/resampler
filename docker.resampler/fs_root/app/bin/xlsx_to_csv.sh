#!/usr/bin/env bash
set -e

file_in=${1?"error: parameter FILE_IN missing"}
dir_out=${2?"error: parameter DIR_OUT missing"}

if [ ! -f "$file_in" ]; then
    >&2 echo "error: '$file_in' does not exist"
    exit 1
fi

if [ ! -d "$dir_out" ]; then
    >&2 echo "error: '$dir_out' is not a directory"
    exit 1
fi

set -x
libreoffice --headless --convert-to csv "$file_in" --outdir "$dir_out"

# https://marceichenseher.de/de/how-to/cli-libreoffice-von-xlsx-zu-csv/
# StarCalc:$feldTrenner,$textTrenner,$zeichensatz,$nummerDerErstenZeile,$ersteSpalte/$formattierungDerErstenSpalte
#libreoffice --headless --convert-to "csv:Text - txt - csv (StarCalc):44,34,76,1,1/1" $xlsDatei --outdir $ausgabeOrdner

