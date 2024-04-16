from flask import Flask, render_template
from read_demo_data import get_demo_data
from read_democvc5_data import get_democvc5_data

app = Flask(__name__)

@app.route('/')
def outputs():
    directory = 'outputs/demo'
    data = get_demo_data(directory)

    return render_template('demo_outputs.html', demo_outputs=data)

@app.route('/democvc5_outputs')
def outputs_cvc5():
    directory = 'outputs/demo_coverage_cvc5'
    data = get_democvc5_data(directory)

    return render_template('democvc5_outputs.html', democvc5_outputs=data)

if __name__ == '__main__':
    app.run(debug=True)
