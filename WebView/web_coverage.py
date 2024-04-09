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

def html_print(rows):
    html_content = '<html>\n<head>\n<title>Fuzz4All against state-of-the-art fuzzers</title>\n</head>\n<body>\n'
    html_content += '<style>\n'
    html_content += '  table { width: 25%; border-collapse: collapse; margin-left: auto; margin-right: auto;}\n'
    html_content += '  th, td { border: 2px solid black; padding: 8px; text-align: center; }\n' 
    html_content += '  h1 { text-align: center; font-style: italic;}\n'
    html_content += '</style>\n'
    html_content += '</head>\n<body>\n'
    html_content += '<h1>Fuzz4All against state-of-the-art fuzzers</h1>\n'
    html_content += '<table>\n'
    html_content += '<tr>\n<th>Target</th>\n'
    html_content += '<th>Fuzzer</th>\n'
    html_content += '<th># programs</th>\n'
    html_content += '<th>% valid</th>\n'
    html_content += '<th>Coverage</th>\n</tr>\n'

    for row in rows:
        html_content += '<tr>\n' + '\n'.join([f'    <td>{cell}</td>' for cell in row]) + '\n</tr>\n'
    
    html_content += '</table>\n</body>\n</html>\n'
    
    with open('WebView/web_coverage.html', 'w') as file:
        file.write(html_content)

def main():
    rows = grab_csv_data("IntermediateResults/full_run/full_run_coverage.csv")
    html_print(rows)

if __name__ == "__main__":
    main()