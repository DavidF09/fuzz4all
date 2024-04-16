from flask import Flask, render_template
from read_outputs_data import get_outputs_data

app = Flask(__name__)

@app.route('/')
def outputs():
    demo_directory = 'outputs/demo'
    demo_data = get_outputs_data(demo_directory)
    
    cvc5_directory = 'outputs/demo_coverage_cvc5'
    cvc5_data = get_outputs_data(cvc5_directory)

    return render_template('outputs.html', 
                           demo_outputs=demo_data, 
                           democvc5_outputs=cvc5_data)

if __name__ == '__main__':
    app.run(debug=True)
