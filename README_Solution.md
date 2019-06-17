# Unbabel challenge - Moving Average

The Mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.


## Lets get started

Clone the repo and follow below steps to run the script.

### Prerequisites
* Python 3.7
* Numpy

#### Packages to install

The script is based on python version 3.7.

To Install python 3.7 follow https://www.python.org/downloads/release/python-370/

To install numpy use following command
```
pip install numpy
```

### Commands to run script

This script takes three inputs from user.

1. Input Filename -> A json file which should contain translation data.

Input Example:
```
{
	"timestamp": "2018-12-26 18:12:19.903159",
	"translation_id": "5aa5b2f39f7254a75aa4",
	"source_language": "en",
	"target_language": "fr",
	"client_name": "easyjet",
	"event_name": "translation_delivered",
	"duration": 20,
	"nr_words": 100
}
```
```
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```
2. window_size -> If user want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes, user should provide window_size as 10.

3. Output Filename -> A Json or txt file, on which output data will be kept. It is a optional command. If user doesnt give any output filename than it will consider 'data.json' as a output file name.

Output Example

```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

Script also support --h or --help and --v or --version to help user with proper commands.

## Running the script

Run the script as same as following example
```
python unbabel_challenge.py -i events.json -w 10 -o output.json

or 

python unbabel_challenge.py --input_file events.json --window_size 10 --output output.json
```

## Authors

Pratistha Anandani

