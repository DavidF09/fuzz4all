def grab_csv_data(csv_file):
    import csv
    import statistics as st

    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    targets = ["GCC", "G++", "CVC5", "Go", "javac", "Qiskit"]
    count = 0

    ret_rows = []
    # print each row
    for row in data[1:]:
        tool_name = row[0]
        if tool_name == "\\tech":
            tool_name = "Fuzz4All"
        avg_progs = str(int(st.mean([float(x) for x in row[1:6]])))
        avg_cov = str(int(st.mean([float(x) for x in row[6:11]])))
        avg_valid = str(round(st.mean([float(x) for x in row[11:16]]), 2)) + "%"
        ret_rows.append([targets[count], tool_name, avg_progs, avg_valid, avg_cov])
        if row[0] == "\\tech":
            count += 1

    return ret_rows


def rich_print(rows):
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(
        show_header=True,
        header_style="bold magenta",
        title="Fuzz4All against state-of-the-art fuzzers",
    )

    table.add_column("Target", style="dim", no_wrap=True)
    table.add_column("Fuzzer", justify="right", style="bold green")
    table.add_column("# programs", justify="right", style="bold blue")
    table.add_column("% valid", justify="right", style="bold blue")
    table.add_column("Coverage", justify="right", style="bold blue")

    for row in rows:
        table.add_row(*row)

    console.print(table)


def main():
    rows = grab_csv_data("IntermediateResults/full_run/full_run_coverage.csv")
    rich_print(rows)


if __name__ == "__main__":
    main()
