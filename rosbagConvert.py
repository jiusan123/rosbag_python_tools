import os
import time
import argparse
from rosbag import Bag, Compression


def parse_compression(compression):
    if compression == "none" or compression == "NONE":
        compression = Compression.NONE
    elif compression == "bz2":
        compression = Compression.BZ2
    elif compression == "lz4":
        compression = Compression.LZ4
    return compression


def get_files_list(arg_input, arg_select):
    files = None
    if " " in arg_input:
        files = arg_input.split(" ")
    elif "," in arg_input:
        files = arg_input.split(",")
    elif os.path.exists(args.input) or "*" in args.input:
        rfind_index = arg_input.rfind("/")
        dir_path = arg_input[:rfind_index]
        files = os.listdir(dir_path)
        files.sort()
        files = [dir_path + "/" + file for file in files]

    if arg_select:
        files = select_bags(files)

    print("bags list:")
    for i in range(len(files)):
        print(str(i) + "." + files[i])

    return files


def select_bags(files):
    for i in range(len(files)):
        print(str(i) + "." + files[i])
    print("Please input bag numbers to merge. split by ,")
    s_b = input()
    s_b_list = []
    if "," in s_b:
        s_b_list = s_b.split(",")
    elif " " in s_b:
        s_b_list = s_b.split(" ")
    files = [files[int(x)] for x in s_b_list]
    return files


def show_process_bar(total, i, start):
    a = "*" * i
    b = "." * (total - i)
    c = (i / total) * 100
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur))


def merge_bags(args):
    print("start merge bags.")
    compression = parse_compression(args.compression)
    # print(f"bag's compression mode is {compression}.")
    files = get_files_list(args.input, args.select)
    with Bag(args.output, "w", compression=compression) as o:
        # start = time.perf_counter()
        for i in range(len(files)):
            # show_process_bar(len(files), i + 1, start)
            with Bag(files[i], "r") as ib:
                for topic, msg, t in ib:
                    o.write(topic, msg, t)
            # show_process_bar(len(files), i + 1, start)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge one or more bag files to one file.")
    parser.add_argument("-o", "--output", help="Output bag's file path.",
                        default="output.bag", required=True)

    parser.add_argument("-i", "--input", help="Input files bags name or path, split by , .",
                        required=True)

    parser.add_argument("-c", "--compression", help="Compress the bag by bz2 or lz4",
                        default="none", choices=["none", "lz4", "bz2"])

    parser.add_argument("-s", "--select", help="Select bags to merge.",
                        default=False)

    parser.add_argument("-v", "--verbose", help="Show the verbose msg.")

    args = parser.parse_args()
    merge_bags(args)
