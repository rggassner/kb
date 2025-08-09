#!/usr/bin/env python3
import os
import re
import gzip
from multiprocessing import Pool, cpu_count
import argparse

# Move these under main if you want dynamic config
SPLITTERS = [
    {
        "name": "split_by_user",
        "split_function": r'user="(?:.*?\()?(?P<username>[a-zA-Z0-9._-]+)\s*(?:\))?"',
        "filter": [""],  # match all users if filter is [""] or empty
        "enabled": True
    },
    {
        "name": "split_by_src",
        "split_function": r'src="(?P<src>.*?)"',
        "filter": [""],
        "enabled": True
    }
]

# Precompile regexes and capture group names for enabled rules
COMPILED_SPLITTERS = []
for splitter in SPLITTERS:
    if not splitter.get("enabled", True):
        continue
    pattern = re.compile(splitter["split_function"])
    match = re.search(r'\?P<(\w+)>', splitter["split_function"])
    COMPILED_SPLITTERS.append({
        "name": splitter["name"],
        "regex": pattern,
        "filter": set(splitter.get("filter", [])),
        "group": match.group(1) if match else None
    })

def open_maybe_gz(file_path):
    if file_path.endswith(".gz"):
        return gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore')
    else:
        return open(file_path, 'r', encoding='utf-8', errors='ignore')

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def process_file(args):
    file_path, output_dir = args
    try:
        with open_maybe_gz(file_path) as infile:
            for line in infile:
                for splitter in COMPILED_SPLITTERS:
                    match = splitter["regex"].search(line)
                    if match:
                        value = match.group(splitter["group"]) if splitter["group"] else match.group(0)
                        # Match all if filter is empty or contains empty string
                        if not splitter["filter"] or "" in splitter["filter"] or value in splitter["filter"]:
                            out_dir = os.path.join(output_dir, splitter["name"])
                            make_dirs(out_dir)
                            out_path = os.path.join(out_dir, value + ".log")
                            with open(out_path, 'a') as f:
                                f.write(line)
        print("Processed:", file_path)
    except Exception as e:
        print("Error processing {}: {}".format(file_path, e))

def collect_files(input_dir):
    file_list = []
    for root, _, files in os.walk(input_dir):
        for name in files:
            file_list.append(os.path.join(root, name))
    return sorted(file_list)

def main(input_dir, output_dir, processes):
    make_dirs(output_dir)
    files = collect_files(input_dir)
    tasks = [(f, output_dir) for f in files]

    print("Discovered {} files. Starting pool with {} processes...".format(len(files), processes))
    pool = Pool(processes)
    pool.map(process_file, tasks)
    pool.close()
    pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Directory with input log files (.gz or plain text)")
    parser.add_argument("output_dir", help="Directory to store filtered logs")
    parser.add_argument("--processes", type=int, default=cpu_count(),
                        help="Number of worker processes (default: all CPUs)")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.processes)

