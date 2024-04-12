# check the target hit rate of the generated fuzzing inputs

import glob

from Fuzz4All.util.util import comment_remover, natural_sort_key


def filter(code, begin, target, lang="c") -> bool:
    clean_code = comment_remover(code, lang=lang).replace(begin, "").strip()
    if target not in clean_code:
        return False
    return True


def check_go():
    folder_target = {
        "atomic": {
            "folder": "",
            "begin": 'package main\nimport (\n\t"sync/atomic"\n)\n',
        },
        "big": {
            "folder": "",
            "begin": 'package main\nimport (\n\t"math/big"\n)\n',
        },
        "heap": {
            "folder": "",
            "begin": 'package main\nimport (\n\t"container/heap"\n)\n',
        },
        "std": {
            "folder": "",
            "begin": 'package main\nimport (\n\t"fmt"\n)\n',
        },
    }

    for target, _ in folder_target.items():
        if target == "std":
            continue
        for campaign, item in folder_target.items():
            files = glob.glob(f"{item['folder']}/*.fuzz")
            count = 0
            for file in files[:10000]:
                with open(file, "r", encoding="utf-8") as f:
                    fo = f.read()

                if filter(fo, item["begin"], target):
                    count += 1

            print(f"{target} {campaign} {count*100 / 10000}")


def check_smt():
    folder_target = {
        "Array": {
            "folder": "",
            "begin": "",
        },
        "BitVec": {
            "folder": "",
            "begin": "",
        },
        "Real": {
            "folder": "",
            "begin": "",
        },
        "std": {
            "folder": "",
            "begin": "",
        },
    }

    for target, _ in folder_target.items():
        if target == "std":
            continue
        for campaign, item in folder_target.items():
            files = glob.glob(f"{item['folder']}/*.fuzz")
            count = 0
            for file in files[:10000]:
                with open(file, "r", encoding="utf-8") as f:
                    fo = f.read()

                if filter(fo, item["begin"], target, lang="smt2"):
                    count += 1

            print(f"{target} {campaign} {count * 100 / 10000}%")


def check_java():
    folder_target = {
        " instanceof ": {
            "folder": "",
            "begin": "",
        },
        " synchronized ": {
            "folder": "",
            "begin": "",
        },
        " finally ": {
            "folder": "",
            "begin": "",
        },
        "std": {
            "folder": "",
            "begin": "",
        },
    }

    for target, _ in folder_target.items():
        if target == "std":
            continue
        for campaign, item in folder_target.items():
            files = glob.glob(f"{item['folder']}/*.fuzz")
            count = 0
            for file in files[:10000]:
                with open(file, "r", encoding="utf-8") as f:
                    fo = f.read()

                if filter(fo, item["begin"], target, lang="java"):
                    count += 1
                    # if campaign == "std":
                    #     print(file)

            print(f"{target} {campaign} {count * 100 / 10000}%")


def check_c():
    folder_target = {
        "typedef": {
            "folder": "",
            "begin": "",
        },
        "union": {
            "folder": "",
            "begin": "",
        },
        "goto": {
            "folder": "",
            "begin": "",
        },
        "std": {
            "folder": "",
            "begin": "",
        },
    }

    for target, _ in folder_target.items():
        if target == "std":
            continue
        for campaign, item in folder_target.items():
            files = glob.glob(f"{item['folder']}/*.fuzz")
            count = 0
            for file in files[:10000]:
                with open(file, "r", encoding="utf-8") as f:
                    fo = f.read()

                if filter(fo, item["begin"], target, lang="cpp"):
                    count += 1

            print(f"{target} {campaign} {count * 100 / 10000}%")


def check_qiskit():
    folder_target = {
        ".switch(": {
            "folder": "",
            "begin": "",
        },
        ".for_loop(": {
            "folder": "",
            "begin": "",
        },
        "LinearFunction(": {
            "folder": "",
            "begin": "",
        },
        "std": {
            "folder": "",
            "begin": "",
        },
    }

    for target, _ in folder_target.items():
        if target == "std":
            continue
        for campaign, item in folder_target.items():
            files = glob.glob(f"{item['folder']}/*.fuzz")
            count = 0
            for file in files[:10000]:
                with open(file, "r", encoding="utf-8") as f:
                    fo = f.read()

                if filter(fo, item["begin"], target, lang=""):
                    count += 1

            print(f"{target} {campaign} {count * 100 / 10000}%")


def check_cpp():
    folder_target = {
        "apply": {
            "folder": "",
            "begin": "#include <tuple>",
        },
        "expected": {
            "folder": "",
            "begin": "#include <expected>",
        },
        "variant": {
            "folder": "",
            "begin": "#include <variant>",
        },
        "std": {
            "folder": "",
            "begin": "",
        },
    }

    for target, _ in folder_target.items():
        if target == "std":
            continue
        for campaign, item in folder_target.items():
            files = glob.glob(f"{item['folder']}/*.fuzz")
            count = 0
            for file in files[:10000]:
                with open(file, "r", encoding="utf-8") as f:
                    fo = f.read()

                if filter(fo, item["begin"], target, lang="cpp"):
                    count += 1

            print(f"{target} {campaign} {count * 100 / 10000}%")


if __name__ == "__main__":
    # main()
    check_go()
    check_smt()
    check_java()
    check_c()
    check_qiskit()
    check_cpp()
