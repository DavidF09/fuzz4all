def grab_csv_data(csv_file):
    import csv
    import statistics as st

    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    targets = ["GCC", "G++", "CVC5", "Go", "javac", "Qiskit"]
    count = 0

    ret_rows = [
        ["autoprompt", "no input", "no initial_prompt"],
        ["autoprompt", "raw prompt", "use user-provided input"],
        ["autoprompt", "autoprompt", "apply autoprompting"],
        ["fuzzing-loop", "w/o example", "generate-new w/o example"],
        ["fuzzing-loop", "w/ example", "generate-new w/ example"],
        ["fuzzing-loop", "Fuzz4All", "all strategies w/ example"],
    ]
    variant_to_row = {
        "no_input": [0],
        "documentation": [1],
        "ap": [2, 4],
        "ap_gen_strat": [5],
        "no_loop": [3],
    }
    # print each row
    for row in data[1:]:
        variant = row[0]
        c_coverage = st.mean([float(x) for x in row[1:5]])
        cpp_coverage = st.mean([float(x) for x in row[6:10]])
        smt_coverage = st.mean([float(x) for x in row[11:15]])
        go_coverage = st.mean([float(x) for x in row[16:20]])
        java_coverage = st.mean([float(x) for x in row[21:25]])
        qiskit_coverage = st.mean([float(x) for x in row[26:30]])

        for row_idx in variant_to_row[variant]:
            ret_rows[row_idx].extend(
                [
                    c_coverage,
                    cpp_coverage,
                    smt_coverage,
                    go_coverage,
                    java_coverage,
                    qiskit_coverage,
                ]
            )

    new_ret_rows = []
    for ret_row in ret_rows:
        new_ret_row = ret_row[:3]
        for cov, valid in zip(ret_row[3:9], ret_row[9:15]):
            new_ret_row.append(str(int(cov)))
            new_ret_row.append(str(round(valid, 2)))
        new_ret_rows.append(new_ret_row)
    return new_ret_rows


def rich_print(rows):
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(
        show_header=True, header_style="bold magenta", title="Effectiveness of variants"
    )

    table.add_column("", style="dim", no_wrap=True)
    table.add_column("Variants", justify="right", style="bold green")
    table.add_column("Description", justify="right", style="bold green")
    table.add_column("C-Cov.", justify="right", style="bold blue")
    table.add_column("C-% Valid", justify="right", style="bold blue")
    table.add_column("C++-Cov.", justify="right", style="bold blue")
    table.add_column("C++-% Valid", justify="right", style="bold blue")
    table.add_column("SMT-Cov.", justify="right", style="bold blue")
    table.add_column("SMT-% Valid", justify="right", style="bold blue")
    table.add_column("Go-Cov.", justify="right", style="bold blue")
    table.add_column("Go-% Valid", justify="right", style="bold blue")
    table.add_column("Java-Cov.", justify="right", style="bold blue")
    table.add_column("Java-% Valid", justify="right", style="bold blue")
    table.add_column("Qiskit-Cov.", justify="right", style="bold blue")
    table.add_column("Qiskit-% Valid", justify="right", style="bold blue")

    for row in rows:
        table.add_row(*row)

    console.print(table)


def main():
    rows = grab_csv_data("IntermediateResults/full_run/ablation_run.csv")
    rich_print(rows)


if __name__ == "__main__":
    main()
