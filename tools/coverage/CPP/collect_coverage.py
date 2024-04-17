import argparse
import glob
import os
import subprocess
import time

from rich.traceback import install

from Fuzz4All.util.util import natural_sort_key

install()
CURRENT_TIME = time.time()

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

COMPILER = "/home/coverage/GCC-13-COVERAGE/bin/g++"
COV_FOLDER = "/home/coverage/gcc-coverage-build/gcc"
GCOV = "/home/coverage/GCC-13-COVERAGE/bin/gcov"


def run_compile(compiler: str, source: str, pre_flags: str, post_flags: str):
    try:
        exit_code = subprocess.run(
            f"{compiler} {pre_flags} {source} {post_flags}",
            shell=True,
            capture_output=True,
            encoding="utf-8",
            timeout=5,
            text=True,
        )
    except subprocess.TimeoutExpired as te:
        pname = f"'{source}'"
        subprocess.run(
            ["ps -ef | grep " + pname + " | grep -v grep | awk '{print $2}'"],
            shell=True,
        )
        subprocess.run(
            [
                "ps -ef | grep "
                + pname
                + " | grep -v grep | awk '{print $2}' | xargs -r kill -9"
            ],
            shell=True,
        )  # kill all tests thank you
        return -1
    except UnicodeDecodeError:
        return -1

    if exit_code.returncode == 0:
        # rm .out file
        subprocess.run(
            f"rm /tmp/out{CURRENT_TIME}",
            shell=True,
            encoding="utf-8",
        )

    return exit_code.returncode


def get_coverage(args):
    subprocess.run(
        f"cd {COV_FOLDER}; lcov --capture --directory . --output-file coverage.info --gcov-tool {GCOV}",
        shell=True,
        encoding="utf-8",
        text=True,
        capture_output=True,
    )
    exit_code = subprocess.run(
        f"cd {COV_FOLDER}; lcov --summary coverage.info",
        shell=True,
        encoding="utf-8",
        text=True,
        capture_output=True,
    )
    line_cov, func_cov = 0, 0
    for line in exit_code.stdout.splitlines():
        if line.strip().startswith("lines......:"):
            line_cov = int(line.strip().split("(")[1].split(" ")[0])
        elif line.strip().startswith("functions..:"):
            func_cov = int(line.strip().split("(")[1].split(" ")[0])
    print(line_cov, func_cov)
    return line_cov, func_cov


def clean_coverage(args):
    subprocess.run(
        f"cd {COV_FOLDER}; lcov --zerocounters --directory .",
        shell=True,
        encoding="utf-8",
    )


def coverage_loop(args):
    with Progress(
        TextColumn("Fuzzing • [progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
    ) as p:
        # clean coverage
        clean_coverage(args)

        # loop through all files in folder in alphanumeric order
        files = glob.glob(args.folder + "/*.fuzz")
        files.sort(key=os.path.getmtime)
        start_time = os.path.getmtime(files[0])
        initial_time = start_time

        files = glob.glob(args.folder + "/*.fuzz")
        files.sort(key=natural_sort_key)
        index = 0
        num_valid = 0
        for file in p.track(files):

            # skip until start
            if index + 1 < args.start:
                index += 1
                continue

            # compile the file
            ret_code = run_compile(
                COMPILER,
                file,
                f"-x c++ -std=c++23 ",
                f"-o /tmp/out{CURRENT_TIME}",
            )
            if ret_code == 0:
                num_valid += 1

            time_seconds = os.path.getmtime(file) - start_time
            if (index + 1) % args.interval == 0 and index + 1 >= args.start:
                line_cov, func_cov = get_coverage(args)
                # append to csv file
                with open(args.folder + "/coverage.csv", "a") as f:
                    f.write(f"{index + 1},{line_cov},{func_cov},{time_seconds}\n")
                start_time = os.path.getmtime(file)

            if index + 1 >= args.end:
                break
            index += 1

        print(f"Total valid: {num_valid}")
        with open(args.folder + "/valid.txt", "w") as f:
            f.write(str(num_valid) + "\n")
            f.write(str(num_valid / index))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str)
    parser.add_argument("--interval", type=int, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=1000000000)
    args = parser.parse_args()

    if args.folder is not None:
        coverage_loop(args)
    else:
        print("No folder specified")


if __name__ == "__main__":
    main()
