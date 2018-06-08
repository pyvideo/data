#!/usr/bin/env python3
# coding: utf-8
"""
Prints a table of contents for a lightning talks description field.

Translates a lightning talk timetable from csv timetable to a table of contents
in ReStructuredText format, for use in the description field. The input csv
should be in the following format:

  Time,Speaker,Title
  00:00,Albus Dumbledore,"Not who, but how?"
  06:25,Hermione Granger,Fear of a name only increases fear of the thing itself
  11:51,Lord Voldemort,Avada Kedavra
  ...
"""

import argparse
import csv
import json
import logging
import os.path
from constants import JSON_FORMAT_KWARGS


def create_sample_csv(filename):
    """Create sample file as base of the lightning talk table"""
    table = [['Time', 'Speaker', 'Title'], ['00:00', 'Unknown', 'Unknown']]

    with open(filename, 'w', newline='') as csvfile:
        lightning_writer = csv.writer(csvfile)
        for line in table:
            lightning_writer.writerow(line)


def csv_description_to_rst(filename, url):
    """Prints a ReStructuredText list-table in json, in the description value
    """

    def body_line(time, speaker, title, first_line=False):
        """Prints a row of ReStructuredText list-table"""
        if first_line:
            hiperlink_underscore = ''
        else:
            hiperlink_underscore = '_'
        return ("   * - {}{}\n"
                "     - {}\n"
                "     - {}\n").format(time, hiperlink_underscore,
                                      speaker.strip(), title.strip())

    head = (".. list-table:: Lightning Talks\n"
            "   :widths: 10 30 60\n"
            "   :header-rows: 1\n\n")
    body = "\n" + body_line('Time', 'Speaker', 'Title', first_line=True)
    footer = "\n\n"
    if '?' in url:
        url_argument_operator = '&'
    else:
        url_argument_operator = '?'
    with open(filename, newline='') as csvfile:
        lightning_reader = csv.DictReader(csvfile)
        for row in lightning_reader:
            body += body_line(row['Time'], row['Speaker'], row['Title'])
            timestamp = row['Time'].split(':')
            if len(timestamp) == 2:
                minutes, seconds = timestamp
                footer += ".. _{}: {}{}t={}m{}s\n".format(
                    row['Time'], url, url_argument_operator, minutes, seconds)
            elif len(timestamp) == 3:
                hours, minutes, seconds = timestamp
                footer += ".. _{}: {}{}t={}h{}m{}s\n".format(
                    row['Time'], url, url_argument_operator, hours, minutes,
                    seconds)
    return head + body + footer


def add_description(json_file, description):
    """Read json file and add description value"""
    try:
        data = json.load(json_file)
    except ValueError:
        logging.error('Json syntax error in file %s', json_file.name)
        raise
    data['description'] = description
    return data


def main():
    """Translates a lightning talk description from csv to ReStructuredText"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "csv", default='lightning.csv', help="path to csv file", type=str)
    parser.add_argument("video_url", help="youtube video url", type=str)
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show debug messages")
    parser.add_argument(
        "-n",
        "--new_csv",
        action="store_true",
        help="create new csv empty file skeleton")
    parser.add_argument(
        "-j",
        "--json",
        nargs='?',
        type=argparse.FileType('r'),
        help="Read json file and replace description with csv data")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Arguments: %s', args)
    else:
        logging.basicConfig(level=logging.WARNING)
    json_output = args.json
    csv_path = args.csv
    video_url = args.video_url
    if args.new_csv:
        if os.path.exists(csv_path):
            raise Exception(
                'Error creating new file. File exists: {}'.format(csv_path))
        else:
            create_sample_csv(csv_path)
    description = csv_description_to_rst(csv_path, video_url)
    json_file = args.json
    if json_output:
        print(
            json.dumps(
                add_description(json_file, description), **JSON_FORMAT_KWARGS))
    else:
        print(description)


if __name__ == '__main__':
    main()
