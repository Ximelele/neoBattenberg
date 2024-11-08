import argparse
from turtledemo.penrose import start

import StrVCTVRE
import AnnotSV
import threading

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Run StrVCTVRE analysis on a patient VCF file.")
    parser.add_argument("-s","--str",nargs="+",type=str, help="Run StrVCTVRE analysis")
    parser.add_argument("-a","--ann",nargs="+",type=str, help="Run AnnotSV analysis")

    args = parser.parse_args()

    threads = []
    if args.str:
        print("Setting job for SyrVCTVRE")
        str_thread = threading.Thread(target=StrVCTVRE.start_analysis, args=(args.str[0],))
        threads.append(str_thread)

    if args.ann:
        print("Setting job for AnnotSV")
        ann_thread = threading.Thread(target=AnnotSV.start_analysis_annotsv, args=(args.ann[0],))
        threads.append(ann_thread)
    print("Starting threads")
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
