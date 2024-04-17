from flask import Flask, render_template
from read_bugs_csv import get_bug_cvs_data
from web_coverage import grab_csv_data as grab_coverage_csv_data
from read_outputs_data import get_outputs_data
from web_ablation import grab_csv_data as grab_ablation_csv_data
from web_targeted import grab_csv_data as grab_targeted_csv_data

app = Flask(__name__)

@app.route('/')
@app.route('/bugs')
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
                           data=grab_coverage_csv_data('IntermediateResults/full_run/full_run_coverage.csv'))

@app.route('/outputs')
def outputs():
    demo_directory = 'outputs/demo'
    demo_data = get_outputs_data(demo_directory)

    cvc5_directory = 'outputs/demo_coverage_cvc5'
    cvc5_data = get_outputs_data(cvc5_directory)

    return render_template('outputs.html', 
                           demo_outputs=demo_data, 
                           democvc5_outputs=cvc5_data)

@app.route('/ablation')
def ablation():
    return render_template('ablation.html', 
                           data=grab_ablation_csv_data('IntermediateResults/full_run/ablation_run.csv'))

@app.route('/targeted')
def targeted():
    return render_template('targeted.html', 
                           data=grab_targeted_csv_data('IntermediateResults/full_run/targeted_run.csv'))

if __name__ == '__main__':
    app.run(debug=True)
