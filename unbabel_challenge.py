import numpy as np
import json
from collections import OrderedDict
from optparse import OptionParser
from argparse import ArgumentParser
import argparse
import sys
import os
import datetime

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

class Moving_Average:
    def __init__(self,input_filename,window_size,output_filename):
        '''
        Initialization of Moving_Average class
        :param input_filename: Input Filename given by user
        :param window_size: Window Size given by user
        :param output_filename: Output filename given by user
        '''
        self.output = OrderedDict()
        self.start_time = None
        self.moving_dataset = [0]
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.window_size = int(window_size)

    def moving_average(self,values,window):
        '''
        Logic to find out moving average from list of value and window size
        :param values: list of value
        :param window: window size
        :return: Moving average based on inputs
        '''
        weights = np.repeat(1.0, window)/window
        smas = np.convolve(values,weights,'valid')
        return smas

    def calculating_value(self,moving_dataset,every_minute,timestamp):
        '''
        Trigger for moving average calculation and formatting proper output format
        :param moving_dataset: Moving dataset based on window size and duration in input file
        :param every_minute: Every Minute starting from first event of input file to the last minute of last event.
        :param timestamp: Timestamp given in Input file based on each event
        '''
        window = 1
        if len(moving_dataset) != 1:
            window = len(moving_dataset)-1
        value = self.moving_average(moving_dataset, window)
        value = value[len(value) - 1]
        self.output_format = timestamp.strftime("%Y-%m-%d %H") + ':' + str(every_minute) + ':00'
        self.output[self.output_format] = value

    def reading_json(self,file_name):
        '''
        Reading Json from Input file
        :param file_name: Input File Name
        :return: Return list of timestamp object and duration for each event
        '''
        timestamps = []
        duration = []
        try:
            data = json.loads(open(self.input_filename).read())
        except ValueError as e:
            print('invalid json: %s' % e)
            return None,e
        for key,value in data.items():
            timestamps.append(datetime.datetime.strptime(value['timestamp'].split('.')[0], '%Y-%m-%d %H:%M:%S'))
            duration.append(value['duration'])
        return timestamps,duration

    def reset_window(self,count):
        '''
        Reset window once it crosses given window_size
        :param count: Window size count
        :return: Window size count
        '''
        if count == self.window_size:
            count = 0
            if len(self.moving_dataset) != 1:
                self.moving_dataset.pop(0)
        return count

    def check_time_diff(self,time1,time2):
        '''
        Calculate difference of different timestamps
        :param time1: Every minute timestamp
        :param time2: Timestamp given by user
        :return: Returns True if timestamps are equal otherwise returns False
        '''
        diff = time2 - time1
        if diff.days <= 0 and diff.seconds < 60:
            return True
        else:
            return False

    def output_generator(self):
        '''
        Calculate moving average for every minute
        :return: Returns True if the moving average of the transactions is determined successfully otherwise gives error
        '''
        timestamps, duration = self.reading_json(self.input_filename)
        if timestamps == None:
            return duration
        end_original_time = timestamps[len(timestamps)-1]
        self.start_time = timestamps[0].strftime("%H:%M")+':00'
        self.start_time = datetime.datetime.strptime(self.start_time, '%H:%M:%S')

        self.output_format = timestamps[0].strftime("%Y-%m-%d %H:%M") + ':00'
        every_minute_time = datetime.datetime.strptime(self.output_format, '%Y-%m-%d %H:%M:%S')
        next_time = False
        new_index = 0
        count = -2

        var = 1
        if end_original_time.minute != '00':
            var = 2
        last_index = 0

        elapsedTime = timestamps[2] - timestamps[0]
        diff_time = divmod(elapsedTime.total_seconds(), 60)[0]
        end_time = int(diff_time + self.start_time.minute + var)

        for every_minute in range(self.start_time.minute,end_time):
            count = count + 1
            for index in range(len(timestamps)):
                if self.check_time_diff(every_minute_time,timestamps[index]) or next_time:
                    if next_time and new_index != index:
                        continue
                    next_time = False
                    if self.check_time_diff(every_minute_time,timestamps[index]) and self.start_time.second < timestamps[index].second:
                        next_time = True
                        new_index = index
                        count = self.reset_window(count)
                        self.calculating_value(self.moving_dataset,every_minute,timestamps[last_index])
                        break
                    count = self.reset_window(count)
                    if self.start_time.second <= timestamps[index].second:
                        self.moving_dataset.append(duration[index])
                    self.calculating_value(self.moving_dataset, every_minute,timestamps[index])
                    last_index = index
                    break
                else:
                    count = self.reset_window(count)
                    if index == len(timestamps)-1:
                        self.calculating_value(self.moving_dataset, every_minute,timestamps[last_index])
                    continue
            every_minute_time = every_minute_time + datetime.timedelta(minutes=1)
        return True

    def writing_json(self,output):
        '''
        Writing determined moving average to output file
        '''
        if self.output_filename == None:
            self.output_filename = 'data.json'
        with open(self.output_filename, 'w') as outfile:
            json.dump([{'date': k, 'average_delivery_time': v} for k, v in output.items()], outfile, indent=1)
        print('Output is generated to',self.output_filename)

if __name__ == "__main__":
    usage = "usage: %prog [options] arg1 arg2"
    version = "Version: %(prog)s 1.0"
    parser = OptionParser(usage="%prog [-f] [-q]", version=version)
    parser = ArgumentParser(description='Find out moving average based on input file data')
    parser = MyParser()

    parser.add_argument('-i', '--input_file',
                        metavar='infile',
                        default=None,
                        nargs='?',
                        type=str,
                        help='Input file containing the information'
                        )

    parser.add_argument('-o', '--output',
                        metavar='outfile',
                        default=None,
                        nargs='?',
                        type=str,
                        help='Optional output file to dump the data to'
                        )

    parser.add_argument('-w', '--window_size',
                        metavar='window_size',
                        default=None,
                        nargs='?',
                        type=str,
                        help='Window Size helps to calculate moving average'
                        )

    parser.add_argument('-v', '--version', action='version', version=version)

    args = parser.parse_args()

    if args.input_file == None and args.window_size == None:
        MyParser(args).error("please provide proper command and corresponding files")
    if args.input_file == None:
        parser.error("Please provide input file.")
    else:
        if not os.path.exists(args.input_file):
            parser.error('Input file is incorrect.\nPlease provide a proper input file.')

    if args.window_size == None:
        parser.error('Please provide window size.')


    obj = Moving_Average(args.input_file,args.window_size,args.output)
    error = obj.output_generator()
    if error != True:
        parser.error(error)
    obj.writing_json(obj.output)