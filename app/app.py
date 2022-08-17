#Consulted https://github.com/memudualimatou/INSURANCE-CHARGES-WEB-APPLICATION/blob/main for categorical inputs

import numpy as np
import pickle
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')
model = pickle.load(open("model.pkl", 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template(
        'index.html',
        # Dictionaries for categorical data
        data1=[{'ccr': 'During the treatment, has the patient been screened for cancer?'}, {'ccr': 'Yes'}, {'ccr': 'No'}],
        data2=[{'imm': 'During the treatment, has the patient received any immunizations?'}, {'imm': 'Yes'}, {'imm': 'No'}],
        data3=[{'lt': 'During the treatment, has the patient received any other long-term drug therapies?'}, {'lt': 'Yes'}, {'lt': 'No'}],
    )

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    input_data = list(request.form.values())

    input_data[0] = int(input_data[0])**1/2
    input_data[5] = int(input_data[5]) ** 1/2

    if input_data[1] == 'No':
        input_data[1] = 0
    elif input_data[1] == 'Yes':
        input_data[1] = 1
    else:
        print(ValueError)

    if input_data[2] == 'No':
        input_data[2] = 0
    elif input_data[2] == 'Yes':
        input_data[2] = 1
    else:
        print(ValueError)

    if input_data[3] == 'No':
        input_data[3] = 0
    elif input_data[3] == 'Yes':
        input_data[3] = 1
    else:
        print(ValueError)

    input_values = [x for x in input_data]
    arr_val = [np.array(input_values, dtype='float')]
    prediction = model.predict(arr_val)

    output = prediction[0]
    if output == 0:
        output = 'NON-PERSISTENT'
    elif output == 1:
        output = 'PERSISTENT'

    return render_template('index.html',
                        data1=[{'ccr': 'During the treatment, has the patient been screened for cancer?'}, {'ccr': 'Yes'}, {'ccr': 'No'}],
                        data2=[{'imm': 'During the treatment, has the patient received any immunizations?'}, {'imm': 'Yes'}, {'imm': 'No'}],
                        data3=[{'lt': 'During the treatment, has the patient received any other long-term drug therapies?'}, {'lt': 'Yes'}, {'lt': 'No'}],
                        prediction_text=" The patient is predicted to be {}".format(output),
                           )

if __name__ == '__main__':
    app.run(debug=True)
