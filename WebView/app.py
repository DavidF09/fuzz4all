from flask import Flask, render_template
from read_bugs_csv import get_bug_cvs_data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', data=get_bug_cvs_data('bugs/clang.csv'), second_file=get_bug_cvs_data('bugs/cvc5.csv'))

if __name__ == '__main__':
    app.run(debug=True)