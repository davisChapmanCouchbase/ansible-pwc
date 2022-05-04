#!/usr/bin/env python3
"""This script will read in a JSON list of fts indexes and send them
to the node specified to be created."""
import os
import json
import urllib.request
import argparse

FTS_FILE = "./fts.json"

def main():
    """This is the main processing method. It reads in the fts index 
    list, then iterates through the indexes, building the defined
    fts indexes on the node specified."""
    # Parse out the command line arguments
    args = parse_args()
    data_dict = read_fts_list(args.file)
    if "fts" in data_dict:
        indexes = data_dict["fts"]
        for index in indexes:
            if index["definition"]:
                print("Working on Index " + index["name"])
                create_search(args.node, args.user, args.pwd, index)

def parse_args():
    """
    This method parses out the command-line parameters.
    """
    parser = argparse.ArgumentParser(
        description='Parse the hours remaining CSV to extract my projects.')
    parser.add_argument('-n', action='store', nargs='?', required=True, metavar='node',
                        dest='node')
    parser.add_argument('-u', action='store', nargs='?', required=True, metavar='user',
                        dest='user')
    parser.add_argument('-p', action='store', nargs='?', required=True, metavar='pwd',
                        dest='pwd')
    parser.add_argument('-f', action='store', nargs='?', required=True, metavar='file',
                        dest='file')
    return parser.parse_args()

def read_json_file(file_name):
    """Json file loader."""
    # Open and read in the file
    input_file = open(file_name, "r")
    raw_file = input_file.read()
    # Load the file contents into a JSON data dictionary for processing
    data_dict = json.loads(raw_file)
    input_file.close()
    return data_dict

def read_fts_list(file_name):
    """FTS Index file loader."""
    return read_json_file(file_name)

def create_search(node, user, pwd, index):
    """Define and build the needed FTS indexes on the buckets."""
    print("Creating " + index["name"])
    idx_cmd = "curl -u " + user + ":"
    idx_cmd += pwd + " "
    idx_cmd += "--silent -XPUT "
    idx_cmd += "http://" + node + ":8094/api/index/" + index["name"] + " "
    idx_cmd += "-H 'cache-control: no-cache' "
    idx_cmd += "-H 'content-type: application/json' "
    idx_cmd += "-d '"
    idx_cmd += load_fts_index(index["definition"])
    idx_cmd += "' >> /tmp/fts.out"
    print(idx_cmd)
    os.system(idx_cmd)

def load_fts_index(file_name):
    """Reads in the FTS index definition file."""
    input_file = open(file_name, "r")
    raw_file = input_file.read()
    input_file.close()
    return raw_file

# Processing begins here by calling the main method.
if __name__ == '__main__':
    main()
