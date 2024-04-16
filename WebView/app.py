from flask import Flask, render_template
from read_bugs_csv import get_bug_cvs_data
from web_coverage import grab_csv_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                            clang_data=get_bug_cvs_data('bugs/clang.csv'), 
                            cvc5_data=get_bug_cvs_data('bugs/cvc5.csv'), 
                            gcc_data=get_bug_cvs_data('bugs/gcc.csv'),
                            go_data=get_bug_cvs_data('bugs/go.csv'),
                            java_data=get_bug_cvs_data('bugs/java.csv'),
                            qiskit_data=get_bug_cvs_data('bugs/qiskit.csv'),
                            z3_data=get_bug_cvs_data('bugs/z3.csv'))

@app.route('/coverage')
def coverage():
    return render_template('coverage.html', 
                           data=grab_csv_data('IntermediateResults/full_run/full_run_coverage.csv'))

if __name__ == '__main__':
    app.run(debug=True)