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

def html_print(table_rows):
    html_content = '<html>\n<head>\n<title>Targeted Campaign Results</title>\n'
    html_content += '<style>\n'
    html_content += '  table { margin-left: auto; margin-right: auto; border-collapse: collapse; }\n'  # Center tables
    html_content += '  th, td { border: 2px solid black; padding: 8px; }\n'
    html_content += '  h2 { font-style: italic; text-align: center; }\n'  # Italicize and center headings
    html_content += '</style>\n'
    html_content += '</head>\n<body>\n'

    for table_row in table_rows:
        html_content += f'<h2>{table_row[0]}</h2>\n'  # Italicized heading due to CSS
        html_content += '<table>\n<tr>\n'
        html_content += '\n'.join([f'<th>{header}</th>' for header in table_row[1]])
        html_content += '\n</tr>\n'

        for row in table_row[2:]:
            html_content += '<tr>\n' + '\n'.join([f'<td>{cell}</td>' for cell in row]) + '\n</tr>\n'

        html_content += '</table>\n<br/>\n'

    html_content += '</body>\n</html>\n'

    with open('WebView/web_targeted.html', 'w') as file:
        file.write(html_content)

def main():
    table_rows = grab_csv_data("IntermediateResults/full_run/targeted_run.csv")
    html_print(table_rows)

if __name__ == "__main__":
    main()
