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

def html_print(rows):
    html_content = '<html>\n<head>\n<title>Effectiveness of Variants</title>\n'
    html_content += '<style>\n'
    html_content += '  table { width: 75%; border-collapse: collapse; margin-left: auto; margin-right: auto;}\n'
    html_content += '  th, td { border: 2px solid black; padding: 8px; text-align: center; }\n'
    html_content += '  h1 { text-align: center; font-style: italic;}\n'
    html_content += '</style>\n'
    html_content += '</head>\n<body>\n'
    html_content += '<h1>Effectiveness of Variants</h1>\n'
    html_content += '<table>\n'
    html_content += '<tr><th>\n'
    html_content += '<th>Variants</th><th>Description</th>\n'
    html_content += '<th>C-Cov.</th><th>C-% Valid</th>\n'
    html_content += '<th>C++-Cov.</th><th>C++-% Valid</th>\n'
    html_content += '<th>SMT-Cov.</th><th>SMT-% Valid</th>\n'
    html_content += '<th>Go-Cov.</th><th>Go-% Valid</th>\n'
    html_content += '<th>Java-Cov.</th><th>Java-% Valid</th>\n'
    html_content += '<th>Qiskit-Cov.</th><th>Qiskit-% Valid</th>\n'
    html_content += '</tr>\n'

    for row in rows:
        html_content += '<tr>\n' + '\n'.join([f'    <td>{cell}</td>' for cell in row]) + '\n</tr>\n'
    
    html_content += '</table>\n</body>\n</html>\n'
    
    with open('WebView/web_ablation.html', 'w') as file:
        file.write(html_content)

def main():
    rows = grab_csv_data("IntermediateResults/full_run/ablation_run.csv")
    html_print(rows)

if __name__ == "__main__":
    main()
