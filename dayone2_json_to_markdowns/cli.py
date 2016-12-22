# -*- encoding: utf-8 -*-

import argparse
import json
import dateutil.parser
import dateutil.tz
import pytz
import os.path
import io


def execute():
    args = _parse_args()

    input_file_path = args.input_file
    output_dir_path = args.output_dir

    entry_writer = EntryWriter(output_dir_path)

    day_one_json = DayOneJson(input_file_path, entry_writer)
    day_one_json.process()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file')
    parser.add_argument('--output-dir')
    return parser.parse_args()


class EntryWriter:
    def __init__(self, output_dir_path):
        self._output_dir_path = output_dir_path

    def write(self, timestamp, text):
        output_file_path = os.path.join(self._output_dir_path, timestamp.strftime('%Y-%m-%dT%H-%M') + '.md')

        with io.open(output_file_path, 'w', encoding='utf8') as f:
            f.write(text)


class DayOneJson:
    def __init__(self, input_file_path, entry_writer):
        self._local_tzinfo = dateutil.tz.tzlocal()

        with io.open(input_file_path, 'r', encoding='utf8') as f:
            self._document = json.load(f)

        self._entry_writer = entry_writer

    def process(self):
        entries = self._document['entries']
        for entry in entries:
            self._process_entry(entry)

    def _process_entry(self, entry):
        creation_date = entry['creationDate']
        utc_timestamp = dateutil.parser.parse(creation_date)
        local_timestamp = utc_timestamp.astimezone(self._entry_tzinfo(entry))

        text = entry["text"]

        self._entry_writer.write(local_timestamp, text)

    def _entry_tzinfo(self, entry):
        if 'timeZone' in entry:
            return pytz.timezone(entry['timeZone'])
        else:
            return self._local_tzinfo
