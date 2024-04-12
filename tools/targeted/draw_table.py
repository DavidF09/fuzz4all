import numpy as np


def grab_csv_data(csv_file):
    import csv

    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    tables = [
        "C targeted campaign (keywords)",
        "C++ targeted campaign (built-in functions)",
        "SMT targeted campaign (theories)",
        "Go targeted campaign (built-in libraries)",
        "Java targeted campaign (keywords)",
        "Qiskit targeted campaign (APIs)",
    ]
    count = -1

    ret_rows = []
    table_rows = []
    for row in data[:]:
        if row[0] == "":
            count += 1
            if count != 0:
                table_rows.append(ret_rows)
            ret_rows = [tables[count]]

        ret_rows.append([x.replace("\\CodeIn{", "").replace("}", "") for x in row[0:5]])

    table_rows.append(ret_rows)
    return table_rows


def rich_print(table_rows):
    from rich.console import Console
    from rich.table import Table

    for table_row in table_rows:
        console = Console()
        table = Table(show_header=True, header_style="bold magenta", title=table_row[0])

        table.add_column(table_row[1][0], style="dim", no_wrap=True)
        table.add_column(table_row[1][1], justify="right", style="bold blue")
        table.add_column(table_row[1][2], justify="right", style="bold blue")
        table.add_column(table_row[1][3], justify="right", style="bold blue")
        table.add_column(table_row[1][4], justify="right", style="bold blue")

        for row in table_row[2:]:
            table.add_row(*row)

        console.print(table)


def main():
    table_rows = grab_csv_data("IntermediateResults/full_run/targeted_run.csv")
    rich_print(table_rows)


if __name__ == "__main__":
    main()
