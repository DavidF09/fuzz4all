"""Collect the coverage of a set of python files on some Python packages.

By default it collects the coverage of all the files related to qiskit, namely
all those in the site-packages folder starting with "qiskit".
"""
import argparse
import multiprocessing
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from functools import partial
from multiprocessing import Pool
from typing import Any, Dict, List, Tuple

import coverage
import pandas as pd


def run_coverage(
    python_file_path: str, timeout: int = None, verbose: bool = False
) -> bool:
    """Run the coverage on the python file using the coverage cmd.

    It runs the command:
    `coverage run {python_file_path}` with a timeout
    Nota that this assumes that the environment variables are set:
    - COVERAGE_FILE
    - COVERAGE_RCFILE

    It returns True if the command was executed successfully, False otherwise.
    """
    # Create the command to run
    cmd: List[str] = [
        "coverage",
        "run",
        python_file_path,
    ]
    # Run the command
    print(f"Running: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, timeout=timeout, capture_output=True, check=True)
        if verbose:
            print(
                f"{python_file_path} \n - Stdout: \n{res.stdout}, \n - Stderr: \n{res.stderr}"
            )
    except subprocess.TimeoutExpired as e:
        print(f"Timeout: {e}")
        return False
    except Exception as e:
        print(f"Error in subprocess run: {e}")
        return False
    return True


def run_files(
    sorted_files: List[str],
    data_file: str = None,
    config_file: str = None,
    save_coverage_every_n_files: int = None,
    out_folder: str = None,
    timeout: int = None,
    verbose: bool = False,
) -> Tuple[int, int]:
    """Run a list of files in isolated environments.

    it returns the number of files that were executed successfully and the
    number of files that failed (e.g. timeout)
    """
    # run each file
    # chunck them in groups of n
    groups = [
        sorted_files[i : i + save_coverage_every_n_files]
        for i in range(0, len(sorted_files), save_coverage_every_n_files)
    ]
    total_success = 0
    total_failure = 0
    for i, group in enumerate(groups):
        print(f"Running group {i}")
        try:
            # run all the files together
            start_time = time.time()
            # run_coverage(
            #     python_file_path=f,
            #     timeout=timeout
            # )
            # parallel version
            n_processors = multiprocessing.cpu_count()
            results = []
            print(f"Using {n_processors} processors.")
            with multiprocessing.Pool() as pool:
                # divide the group in groups of n_processors elements
                # e.g. if n_processors = 4 and group = [1,2,3,4,5,6,7,8,9,10]
                # then the new_groups will be:
                # [[1,2,3,4], [5,6,7,8], [9,10]]
                partial_groups = [
                    group[i : i + n_processors]
                    for i in range(0, len(group), n_processors)
                ]
                for partial_group in partial_groups:
                    print(f"Running group: {partial_group}")
                    partial_results = pool.map(
                        partial(run_coverage, timeout=timeout, verbose=verbose),
                        partial_group,
                    )
                    # add results to the total
                    results += partial_results
            # count how many True (success) and False (failure)
            n_success = sum(results)
            n_failure = len(results) - n_success
            total_success += n_success
            total_failure += n_failure
            end_time = time.time()
            diff = end_time - start_time
            print(f"End exec. duration {diff:.4f} seconds.")
            print(f"Run {len(results)} files in this chunk.")
            print(
                f"[parallelism batch size: {n_processors} - timeout per batch:{timeout} seconds.]"
            )
            print(f"Total success: {n_success}. Total failure (timeout): {n_failure}")
        except Exception as e:
            print(f"Error: {e}")
        # save coverage
        cov = coverage.Coverage(
            data_file=data_file, data_suffix=True, config_file=config_file
        )
        cov.load()
        cov.combine()
        cov.save()
        cov.load()
        # create report for the last n files
        start_val = i * save_coverage_every_n_files
        end_val = start_val + len(group) - 1
        xml_path = os.path.join(out_folder, f"coverage_{start_val}_{end_val}.xml")
        try:
            cov.xml_report(outfile=xml_path)
        except Exception as e:
            print(f"Error: {e}")
    return total_success, total_failure


def create_cumulative_coverage_csv(output_folder: str):
    """Collect the coverage from all the file and create a csv file.

    The files are:
    - coverage_0_9.xml
    - coverage_10_19.xml
    - coverage_20_29.xml
    ...
    Each xml contains the
    """
    all_records = []
    # use regex
    relevant_files = [
        os.path.join(output_folder, f)
        for f in os.listdir(output_folder)
        if re.match(r"coverage_\d+_\d+\.xml", f)
    ]
    for j, path_xml_file in enumerate(relevant_files):
        tree = ET.parse(path_xml_file)
        root = tree.getroot()
        total_coverage = float(root.attrib["line-rate"])
        interval_end = int(
            re.search(r"coverage_\d+_(\d+)\.xml", path_xml_file).group(1)
        )
        n_files = interval_end + 1
        all_records.append({"n_files": n_files, "perc_total_coverage": total_coverage})
    df = pd.DataFrame.from_records(all_records)
    output_csv = os.path.join(output_folder, "cumulative_coverage.csv")
    df.to_csv(output_csv, index=False)
    return output_csv


def main():
    """Collect the coverage info for all packages starting with "qiskit"."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str)
    parser.add_argument("--interval", type=int, required=True)
    args = parser.parse_args()

    if args.folder is None:
        print("No folder specified")
        exit()

    output_folder = args.folder + "/coverage"

    # create the output folder
    os.makedirs(output_folder, exist_ok=True)
    data_file = os.path.join(output_folder, ".mycoverage")
    abs_data_file = os.path.abspath(data_file)
    # get the site-packages directory
    site_packages = os.path.dirname(os.path.dirname(coverage.__file__))

    # track terra compiler
    packages_to_track = ["qiskit"]

    print(f"Packages to track: {packages_to_track}")
    if len(packages_to_track) == 0:
        print("expected qiskit packages.")
        # get all the folders starting with "qiskit"
        qiskit_folders = [
            os.path.join(site_packages, f)
            for f in os.listdir(site_packages)
            if f.startswith("qiskit")
        ]
        packages_to_track = qiskit_folders
    else:
        # add the site-packages folder prefix to the packages_to_track
        packages_to_track = [os.path.join(site_packages, f) for f in packages_to_track]
    list_of_packages = "\n    ".join(packages_to_track)
    print("Packages to track:")
    for f in packages_to_track:
        print(f)
    concatenated_packages = ",".join(packages_to_track)
    config_file_content = f"""
[run]
branch = True
concurrency = multiprocessing
parallel = True
source =
    {list_of_packages}

# {concatenated_packages}
"""
    # create the .coveragerc file
    config_file_path = os.path.join(output_folder, ".coveragerc")
    with open(config_file_path, "w") as f:
        f.write(config_file_content)
    abs_config_file_path = os.path.abspath(config_file_path)

    # set the two as environment variables
    os.environ["COVERAGE_FILE"] = abs_data_file
    os.environ["COVERAGE_RCFILE"] = abs_config_file_path

    # get all files starting with "to_run"
    files = [
        os.path.join(args.folder, f)
        for f in os.listdir(args.folder)
        if f.endswith(".fuzz")
    ]
    # filenames
    # 1.fuzz
    # 2.fuzz
    # 3.fuzz
    # ...
    # 10.fuzz
    sorted_files = sorted(
        files, key=lambda x: int(re.search(r"(\d+)\.fuzz", x).group(1))
    )

    # list of files to run
    for f in sorted_files:
        print(f)

    # run the files
    total_success, total_failure = run_files(
        sorted_files=sorted_files,
        data_file=abs_data_file,
        config_file=abs_config_file_path,
        save_coverage_every_n_files=args.interval,
        out_folder=output_folder,
        timeout=5,
        verbose=False,
    )
    print("-" * 80)

    cov = coverage.Coverage(
        data_file=abs_data_file, data_suffix=True, config_file=abs_config_file_path
    )
    cov.load()
    cov.combine()
    cov.save()
    cov.load()
    # save file as xml
    xml_path = os.path.join(output_folder, "coverage_final.xml")
    cov.xml_report(outfile=xml_path)

    path_csv = create_cumulative_coverage_csv(output_folder)

    print(f"Total success: {total_success}. Total failure (timeout): {total_failure}")

    valid_path = os.path.join(output_folder, "valid.txt")
    with open(valid_path, "w") as f:
        f.write(
            f"Total success: {total_success}. Total failure (timeout): {total_failure}"
        )


if __name__ == "__main__":
    main()
