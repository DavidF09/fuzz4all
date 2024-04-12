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


def write_back_file(code, write_back_name=""):
    if write_back_name != "":
        try:
            with open(write_back_name, "w", encoding="utf-8") as f:
                f.write(code)
        except:
            pass


def determine_file_name(folder, code):
    public_class_name = re.search("\s*public(\s)+class(\s)+([^\s\{]+)", code)

    # check if folder exists
    if not os.path.exists(f"/tmp/temp{folder}"):
        os.mkdir(f"/tmp/temp{folder}")

    if public_class_name is None:
        # No public class found, return standard write back file name
        return f"/tmp/temp{folder}/temp.java"

    # Public class is found, ensure that file name matches public class name
    return f"/tmp/temp{folder}/{public_class_name[0].split()[-1]}.java"


def baseline_coverage_loop(args):
    with open("java_whitelist") as f:
        whitelist = [l.strip() for l in f.readlines()]

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
            f'./java_test_suite.sh "{" ".join(folder_names)}" Results/{order}'
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

        for folder_names, order in zip(total_folders, orders):
            # combine all previous
            if i == 0:
                # just cp
                subprocess.run(
                    f"./combine.sh java Results/{order}/jacoco.exec Results/{order}/jacoco.exec Results/combined java-comb",
                    shell=True,
                    capture_output=True,
                    text=True,
                )
            else:
                # first move the previous combined folder
                subprocess.run(
                    f"mv Results/combined Results/combined_temp",
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                subprocess.run(
                    f"./combine.sh java Results/{order}/jacoco.exec Results/combined_temp/java-comb.exec Results/combined java-comb",
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                # delete combined folder
                subprocess.run(
                    f"rm -rf Results/combined_temp",
                    shell=True,
                    capture_output=True,
                    text=True,
                )

            # delete all folders
            for folder_name in folder_names:
                subprocess.run(
                    f"rm -rf {folder_name}", shell=True, capture_output=True, text=True
                )

            # remove current coverage folder
            subprocess.run(
                f"rm -rf Results/{order}", shell=True, capture_output=True, text=True
            )

        raw = read_csv("Results/combined/java-comb.csv", whitelist=whitelist)
        lines, missed = compute_raw(raw["total"], "line")
        print(i + args.interval, lines / (lines + missed))
        with open("Results/coverage.txt", "a") as f:
            f.write(f"{i+args.interval},{lines},0\n")


def coverage_loop(args):

    with open("java_whitelist") as f:
        whitelist = [l.strip() for l in f.readlines()]

    files = glob.glob(args.folder + "/*.fuzz")
    files.sort(key=natural_sort_key)
    # loop through files in interval
    for i in range(0, len(files), args.interval):
        folder_names = []
        for j in range(i, min(i + args.interval, len(files))):
            try:
                with open(files[j], "r", encoding="utf-8") as f:
                    code = f.read()
                    write_back_name = determine_file_name(j, code)
                    write_back_file(code, write_back_name=write_back_name)
                    folder_names.append(write_back_name)
            except:
                pass
        order = min(i + args.interval, len(files))
        subprocess.run(
            f'./java_test_suite.sh "{" ".join(folder_names)}" Results/{order}',
            shell=True,
            capture_output=True,
            text=True,
        )
        # combine all previous
        if i == 0:
            # just cp
            subprocess.run(
                f"./combine.sh java Results/{order}/jacoco.exec Results/{order}/jacoco.exec Results/combined java-comb",
                shell=True,
                capture_output=True,
                text=True,
            )
        else:
            # first move the previous combined folder
            subprocess.run(
                f"mv Results/combined Results/combined_temp",
                shell=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                f"./combine.sh java Results/{order}/jacoco.exec Results/combined_temp/java-comb.exec Results/combined java-comb",
                shell=True,
                capture_output=True,
                text=True,
            )
            # delete combined folder
            subprocess.run(
                f"rm -rf Results/combined_temp",
                shell=True,
                capture_output=True,
                text=True,
            )

        # remove current coverage folder
        subprocess.run(
            f"rm -rf Results/{order}", shell=True, capture_output=True, text=True
        )

        raw = read_csv("Results/combined/java-comb.csv", whitelist=whitelist)
        lines, missed = compute_raw(raw["total"], "line")
        print(order, lines / (lines + missed))
        with open("Results/coverage.txt", "a") as f:
            f.write(f"{order},{lines},0\n")

        # delete all folders
        for folder_name in folder_names:
            subprocess.run(
                f"rm -rf {folder_name}", shell=True, capture_output=True, text=True
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=str, default="Results/test")
    parser.add_argument("--interval", type=int, required=True)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--baseline", action="store_true")

    args = parser.parse_args()

    if args.baseline:
        baseline_coverage_loop(args)
    else:
        coverage_loop(args)


if __name__ == "__main__":
    main()
