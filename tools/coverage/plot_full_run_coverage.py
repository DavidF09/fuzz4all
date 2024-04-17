import os

import matplotlib as mpl
from matplotlib import pyplot as plt

# set plot to use latex fonts

plt.style.use(
    "https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle"
)
plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.weight"] = "bold"
plt.rcParams.update({"font.size": 14})

plt.rcParams["axes.facecolor"] = "#f3f7ff"
plt.rcParams["axes.edgecolor"] = "black"
mpl.rcParams["grid.color"] = "#cad4e5"
mpl.rcParams["grid.linewidth"] = 1.2

# dark blue
mpl.rcParams["axes.edgecolor"] = "#0b2457"
mpl.rcParams["axes.linewidth"] = 1.2

BASE_DIR = "IntermediateResults/"


def grab_line_cov(lines, change_time=False, increase_index=True):
    line_cov = []
    func_cov = []
    intervals = []
    time = []
    for index, line in enumerate(lines):
        intervals.append(int(line.split(",")[0]))
        line_cov.append(float(line.split(",")[1]) / 1000)
        # func_cov.append(int(line.split(",")[2]))
        if change_time:
            if increase_index:
                time.append((index + 1) * 24 / len(lines))
            else:
                time.append((index) * 24 / len(lines))
        else:
            time.append(float(line.split(",")[3]) / (60 * 60))

    return line_cov, time, intervals


def extrapolate_points(points, original_time, new_times):
    # linearly extrapolate new points at the new_times
    # based on the points at the original_time
    new_points = []
    for new_time in new_times:
        # find the two points that the new_time is between
        for i in range(len(original_time) - 1):
            if original_time[i] <= new_time < original_time[i + 1]:
                # linearly extrapolate
                new_points.append(
                    points[i]
                    + (points[i + 1] - points[i])
                    * (new_time - original_time[i])
                    / (original_time[i + 1] - original_time[i])
                )
                break

    while len(new_points) != len(new_times):
        new_points.append(points[-1])

    return new_points


def grab_max_min_average(points):
    # points is a list of lists
    # each list is a list of points

    max_points = []
    min_points = []
    average_points = []
    for i in range(len(points[0])):
        max_points.append(max([point[i] for point in points]))
        min_points.append(min([point[i] for point in points]))
        average_points.append(sum([point[i] for point in points]) / len(points))

    return max_points, min_points, average_points


def plot_c_full_run():
    # figure size
    plt.figure(figsize=(6, 4))

    folders = [
        f"{BASE_DIR}full_run/GrayC/fuzzer-output-directory-prev/",
        f"{BASE_DIR}full_run/GrayC/fuzzer-output-directory-prev-2/",
        f"{BASE_DIR}full_run/GrayC/fuzzer-output-directory-prev-3/",
        f"{BASE_DIR}full_run/GrayC/fuzzer-output-directory-prev-4/",
        f"{BASE_DIR}full_run/GrayC/fuzzer-output-directory-prev-5/",
    ]

    points = []
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()
        if "4" in folder:
            line_cov, time, _ = grab_line_cov(
                lines, change_time=True, increase_index=False
            )
        else:
            line_cov, time, _ = grab_line_cov(lines)
        line_cov = extrapolate_points(line_cov, time, [i for i in range(0, 25)])
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        [i for i in range(0, 25)],
        average_points,
        label="GrayC",
        linewidth=2,
        marker="v",
        markersize=4,
    )
    plt.fill_between(
        [i for i in range(0, 25)], min_points, max_points, alpha=0.2, color="blue"
    )

    # horizontal line
    plt.axhline(
        y=155765 / 1000, color="#5A5B9F", linestyle="--", label="seed", linewidth=2
    )

    folders = [
        f"{BASE_DIR}full_run/c/std",
        f"{BASE_DIR}full_run/c/std_2",
        f"{BASE_DIR}full_run/c/std_3",
        f"{BASE_DIR}full_run/c/std_4",
        f"{BASE_DIR}full_run/c/std_5",
    ]

    points = []
    new_time = [i for i in range(1, 25)]
    # insert 0.5 at the beginning
    new_time.insert(0, 0.5)
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()
        # add zero, zero at the beginning of lines
        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)

        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Fuzz4All",
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="salmon")

    folders = [
        f"{BASE_DIR}full_run/csmith/run-24-c/",
        f"{BASE_DIR}full_run/csmith/run-24-c-2/",
        f"{BASE_DIR}full_run/csmith/run-24-c-3/",
        f"{BASE_DIR}full_run/csmith/run-24-c-4/",
        f"{BASE_DIR}full_run/csmith/run-24-c-5/",
    ]
    points = []

    for folder in folders:
        with open(f"{folder}coverage.csv", "r") as f:
            lines = f.readlines()

        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time, average_points, label="Csmith", linewidth=2, marker="^", markersize=4
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="green")

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    # plt.title(title)
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)
    # x ticks every 2 hours
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right", ncol=2)
    plt.savefig("fig/coverage-gcc.pdf")


def plot_cpp_full_run():
    # figure size
    plt.figure(figsize=(6, 4))

    new_time = [i for i in range(1, 25)]
    # insert 0.5 at the beginning
    new_time.insert(0, 0.5)
    points = []
    folders = [
        f"{BASE_DIR}full_run/yarpgen/run_24_2/",
        f"{BASE_DIR}full_run/yarpgen/run_24_3/",
        f"{BASE_DIR}full_run/yarpgen/run_24_4/",
        f"{BASE_DIR}full_run/yarpgen/run_24_5/",
    ]
    for folder in folders:
        with open(f"{folder}coverage.csv", "r") as f:
            lines = f.readlines()

        lines.insert(0, "0,0,0,0\n")
        if "_3" in folder or "_4" in folder:
            line_cov, time, _ = grab_line_cov(
                lines, change_time=True, increase_index=False
            )
        else:
            line_cov, time, _ = grab_line_cov(lines)

        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time, average_points, label="YarpGen", linewidth=2, marker="v", markersize=4
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="blue")

    folders = [
        f"{BASE_DIR}full_run/cpp/cpp_23",
        f"{BASE_DIR}full_run/cpp/cpp_23_2",
        f"{BASE_DIR}full_run/cpp/cpp_23_3",
        f"{BASE_DIR}full_run/cpp/cpp_23_4",
        f"{BASE_DIR}full_run/cpp/cpp_23_5",
    ]

    points = []

    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()

        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)

        # increment of half an hour up to 24 hours
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Fuzz4All",
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="salmon")

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    # plt.title(title)
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)
    # x ticks every 2 hours
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right")
    plt.savefig("fig/coverage-g++.pdf")


def plot_smt_full_run():
    # figure size
    plt.figure(figsize=(6, 4))
    folders = [
        f"{BASE_DIR}full_run/typefuzz/run",
        f"{BASE_DIR}full_run/typefuzz/run_2",
        f"{BASE_DIR}full_run/typefuzz/run_3",
        f"{BASE_DIR}full_run/typefuzz/run_4",
        f"{BASE_DIR}full_run/typefuzz/run_5",
    ]
    points = []
    for folder in folders:
        with open(f"{folder}/coverage.txt", "r") as f:
            lines = f.readlines()
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        line_cov = extrapolate_points(line_cov, time, [i for i in range(0, 25)])
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        [i for i in range(0, 25)],
        average_points,
        label="TypeFuzz",
        linewidth=2,
        marker="v",
        markersize=4,
    )
    plt.fill_between(
        [i for i in range(0, 25)], min_points, max_points, alpha=0.2, color="blue"
    )

    folders = [
        f"{BASE_DIR}full_run/smt2/general_strategy",
        f"{BASE_DIR}full_run/smt2/general_strategy_2",
        f"{BASE_DIR}full_run/smt2/general_strategy_3",
        f"{BASE_DIR}full_run/smt2/general_strategy_4",
        f"{BASE_DIR}full_run/smt2/general_strategy_5",
    ]

    points = []
    new_time = [i for i in range(1, 25)]
    new_time.insert(0, 0.5)
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()

        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        # increment of half an hour up to 24 hours
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Fuzz4All",
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="salmon")

    # horizontal line
    plt.axhline(
        y=44113 / 1000, color="#5A5B9F", linestyle="--", label="seed", linewidth=2
    )

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    # plt.title(title)
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)
    # x ticks every 2 hours
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right", ncol=2)
    plt.savefig("fig/coverage-cvc5.pdf")


def plot_go_full_run():
    # figure size
    plt.figure(figsize=(6, 4))
    points = []
    folders = [
        f"{BASE_DIR}full_run/go-fuzz/run_1",
        f"{BASE_DIR}full_run/go-fuzz/run_2",
        f"{BASE_DIR}full_run/go-fuzz/run_3",
        f"{BASE_DIR}full_run/go-fuzz/run_4",
        f"{BASE_DIR}full_run/go-fuzz/run_5",
    ]
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        line_cov = extrapolate_points(line_cov, time, [i for i in range(0, 25)])
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        [i for i in range(0, 25)],
        average_points,
        label="go-fuzz",
        linewidth=2,
        marker="v",
        markersize=4,
    )
    plt.fill_between(
        [i for i in range(0, 25)], min_points, max_points, alpha=0.2, color="blue"
    )

    folders = [
        f"{BASE_DIR}full_run/go/run",
        f"{BASE_DIR}full_run/go/run_2",
        f"{BASE_DIR}full_run/go/run_3",
        f"{BASE_DIR}full_run/go/run_4",
        f"{BASE_DIR}full_run/go/run_5",
    ]
    points = []
    new_time = [i for i in range(1, 25)]
    new_time.insert(0, 0.5)
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()

        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        # increment of half an hour up to 24 hours
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Fuzz4All",
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="salmon")

    # horizontal line
    plt.axhline(
        y=36166 / 1000, color="#5A5B9F", linestyle="--", label="seed", linewidth=2
    )

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    # plt.title(title)
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)
    # x ticks every 2 hours
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right", ncol=2)
    plt.savefig("fig/coverage-go.pdf")


def plot_java_full_run():
    # figure size
    plt.figure(figsize=(6, 4))
    new_time = [i for i in range(1, 25)]
    # insert 0.5 at the beginning
    new_time.insert(0, 0.5)
    points = []
    folders = [
        f"{BASE_DIR}full_run/hephaestus/run_1",
        f"{BASE_DIR}full_run/hephaestus/run_2",
        f"{BASE_DIR}full_run/hephaestus/run_3",
        f"{BASE_DIR}full_run/hephaestus/run_4",
        f"{BASE_DIR}full_run/hephaestus/run_5",
    ]

    for folder in folders:
        with open(f"{folder}/coverage.txt", "r") as f:
            lines = f.readlines()
        lines.insert(0, "0,0,0,0\n")

        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Hephaestus",
        linewidth=2,
        marker="v",
        markersize=4,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="blue")

    folders = [
        f"{BASE_DIR}full_run/java/run",
        f"{BASE_DIR}full_run/java/run_2",
        f"{BASE_DIR}full_run/java/run_3",
        f"{BASE_DIR}full_run/java/run_4",
        f"{BASE_DIR}full_run/java/run_5",
    ]

    points = []

    for folder in folders:
        with open(f"{folder}/coverage.txt", "r") as f:
            lines = f.readlines()

        lines.insert(0, "0,0,0,0\n")
        line_cov, time, _ = grab_line_cov(lines, change_time=True, increase_index=False)
        # increment of half an hour up to 24 hours
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Fuzz4All",
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="salmon")

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    # plt.title(title)
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)
    # x ticks every 2 hours
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right")
    plt.savefig("fig/coverage-javac.pdf")


def plot_qiskit_full_run():
    plt.figure(figsize=(6, 4))
    new_time = [i for i in range(1, 25)]
    points = []
    new_time.insert(0, 0.5)
    folders = [
        f"{BASE_DIR}full_run/morphq/run_1",
        f"{BASE_DIR}full_run/morphq/run_2",
        f"{BASE_DIR}full_run/morphq/run_3",
        f"{BASE_DIR}full_run/morphq/run_4",
        f"{BASE_DIR}full_run/morphq/run_5",
    ]
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()
        lines.insert(0, "0,0,0,0\n")
        line_cov, _, time = grab_line_cov(lines, change_time=True, increase_index=False)
        # sort line_cov based on time
        line_cov = [x * 90417 for _, x in sorted(zip(time, line_cov))]
        # time is just
        time = [(index + 1) * 24 / len(lines) for index in range(len(lines))]
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time, average_points, label="MorphQ", linewidth=2, marker="v", markersize=4
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="blue")

    folders = [
        f"{BASE_DIR}/full_run/qiskit/run_opt_and_qasm",
        f"{BASE_DIR}/full_run/qiskit/run_opt_and_qasm",
        f"{BASE_DIR}/full_run/qiskit/run_opt_and_qasm_2",
        f"{BASE_DIR}/full_run/qiskit/run_opt_and_qasm_4",
        f"{BASE_DIR}/full_run/qiskit/run_opt_and_qasm_5",
    ]

    points = []
    for folder in folders:
        with open(f"{folder}/coverage.csv", "r") as f:
            lines = f.readlines()
        lines.insert(0, "0,0,0,0\n")
        line_cov, _, time = grab_line_cov(lines, change_time=True)
        # sort line_cov based on time
        line_cov = [x * 90417 for _, x in sorted(zip(time, line_cov))]
        # time is just
        time = [(index + 1) * 24 / len(lines) for index in range(len(lines))]
        # increment of half an hour up to 24 hours
        line_cov = extrapolate_points(line_cov, time, new_time)
        points.append(line_cov)

    max_points, min_points, average_points = grab_max_min_average(points)
    plt.plot(
        new_time,
        average_points,
        label="Fuzz4All",
        linewidth=2,
        marker="*",
        markersize=8,
    )
    plt.fill_between(new_time, min_points, max_points, alpha=0.2, color="salmon")

    plt.xlabel("Hours")
    plt.ylabel("Coverage (#K lines)")
    plt.tight_layout()
    # xlimit
    plt.xlim(0, 24)
    plt.xticks([i * 2 for i in range(13)])
    plt.legend(loc="lower right")
    plt.savefig("fig/coverage-qiskit.pdf")


if __name__ == "__main__":
    print("Plotting CPP coverage full run ...")
    plot_cpp_full_run()
    print("Plotting SMT2 coverage full run ...")
    plot_smt_full_run()
    print("Plotting GO coverage full run ...")
    plot_go_full_run()
    print("Plotting C coverage full run ...")
    plot_c_full_run()
    print("Plotting JAVAC coverage full run ...")
    plot_java_full_run()
    print("Plotting QISKIT coverage full run ...")
    plot_qiskit_full_run()
