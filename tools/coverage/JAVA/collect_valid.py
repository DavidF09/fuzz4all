import argparse
import csv
import glob
import os
import re
import shutil
import subprocess
from collections import defaultdict


def natural_sort_key(s):
    _nsre = re.compile("([0-9]+)")
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def check(pkg, cls, whitelist):
    def check_pkg(pattern):
        if "*" in pattern and pkg.startswith(pattern[:-1]):
            return True
        if pkg == pattern:
            return True
        return False

    for pattern in whitelist:
        if "," not in pattern and check_pkg(pattern):
            return True
        elif "," in pattern:
            pkg2 = pattern.split(",")[0]
            cls2 = pattern.split(",")[1]
            if check_pkg(pkg2) and cls.startswith(cls2):
                return True
    return False


def compute_raw(res, metric):
    covered = metric + "_covered"
    covered = res[covered]
    missed = metric + "_missed"
    missed = res[missed]
    if covered == 0 and missed == 0:
        return 0
    return covered, missed


def read_csv(name, whitelist):
    def add_coverage(res, pkg, key, value):
        segs = pkg.split(".")
        while segs:
            pkg = ".".join(segs)
            res[pkg][key] += value
            segs = segs[:-1]

    res = defaultdict(lambda: defaultdict(lambda: 0))
    with open(name, "r") as f:
        csvreader = csv.reader(f)
        next(csvreader)
        # Header
        # (0) GROUP,(1) PACKAGE,(2) CLASS,
        # (3)INSTRUCTION_MISSED, (4)INSTRUCTION_COVERED,
        # (5)BRANCH_MISSED, (6)BRANCH_COVERED,
        # (7)LINE_MISSED, (8)LINE_COVERED,
        # (9)COMPLEXITY_MISSED, (10)COMPLEXITY_COVERED,
        # (11)METHOD_MISSED, (12)METHOD_COVERED

        for row in csvreader:
            pkg = row[1]
            cls = row[2].split(".")[0]
            if check(pkg, cls, whitelist):
                branch_missed = row[3]
                branch_covered = row[4]
                line_missed = row[7]
                line_covered = row[8]
                function_missed = row[11]
                function_covered = row[12]
                add_coverage(res, pkg, "branch_missed", int(branch_missed))
                add_coverage(res, pkg, "branch_covered", int(branch_covered))
                add_coverage(res, pkg, "line_missed", int(line_missed))
                add_coverage(res, pkg, "line_covered", int(line_covered))
                add_coverage(res, pkg, "function_missed", int(function_missed))
                add_coverage(res, pkg, "function_covered", int(function_covered))
                res[(pkg, cls)]["branch_missed"] += int(branch_missed)
                res[(pkg, cls)]["branch_covered"] += int(branch_covered)
                res[(pkg, cls)]["line_missed"] += int(line_missed)
                res[(pkg, cls)]["line_covered"] += int(line_covered)
                res[(pkg, cls)]["function_missed"] += int(function_missed)
                res[(pkg, cls)]["function_covered"] += int(function_covered)
                res["total"]["branch_missed"] += int(branch_missed)
                res["total"]["branch_covered"] += int(branch_covered)
                res["total"]["line_missed"] += int(line_missed)
                res["total"]["line_covered"] += int(line_covered)
                res["total"]["function_missed"] += int(function_missed)
                res["total"]["function_covered"] += int(function_covered)

    return res


def baseline(args):

    folders = glob.glob(args.folder + "/*/")
    folders.sort(key=natural_sort_key)

    for i in range(0, len(folders), args.interval):
        total_folders = []
        orders = []
        for j in range(i, min(i + args.interval, len(folders)), args.parallel):
            folder_names = []
            # parallel processing
            for k in range(j, min(j + args.parallel, len(folders))):

                # cp folder to temp folder
                try:
                    shutil.copytree(folders[j], f"/tmp/temp{k}")
                    folder_names.append(f"/tmp/temp{k}")

                except:
                    pass
            total_folders.append(folder_names)
            order = min(j, len(folders))
            orders.append(order)

        commands = [
            f'./java_valid.sh "{" ".join(folder_names)}" Results/{order}'
            for folder_names, order in zip(total_folders, orders)
        ]

        procs = [
            subprocess.Popen(
                i,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
            )
            for i in commands
        ]

        exit_codes = [p.wait() for p in procs]


def count(args):
    results = glob.glob("Results/*/*.txt")
    valid, invalid, total = 0, 0, 0
    for result in results:
        with open(result, "r") as f:
            x = f.read()
        if "0" == x.strip():
            valid += 1
        elif "1" == x.strip():
            invalid += 1
        total += 1

    print(f"Valid: {valid}, Invalid: {invalid}, Total: {total}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--interval", type=int, required=True)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--count", action="store_true")

    args = parser.parse_args()
    if args.count:
        count(args)
    else:
        baseline(args)


if __name__ == "__main__":
    main()
