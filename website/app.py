from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'  # Make sure this path is correct
    
    # Print the absolute file path for debugging
    print(f"Model file path: {os.path.abspath(filename)}")
    
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        pred_value = model.predict([lst])
        print(f"Predicted value: {pred_value}")  # Debugging prediction value
        return pred_value
    except FileNotFoundError:
        print(f"Model file not found: {filename}")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

@app.route('/', methods=['POST', 'GET'])
def index():
    print(f"Received request method: {request.method}")  # Debugging line
    pred_value = 0

    if request.method == 'POST':
        print("POST request received")  # Debugging line

        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        print(f"Form Data: RAM={ram}, Weight={weight}, Company={company}, Type={typename}, OS={opsys}, CPU={cpu}, GPU={gpu}, Touchscreen={touchscreen}, IPS={ips}")

        feature_list = [
            int(ram),
            float(weight),
            len(touchscreen),
            len(ips)
        ]

        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'other', 'windows']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        def traverse_list(lst, value):
            for item in lst:
                feature_list.append(1 if item == value else 0)

        traverse_list(company_list, company)
        traverse_list(typename_list, typename)
        traverse_list(opsys_list, opsys)
        traverse_list(cpu_list, cpu)
        traverse_list(gpu_list, gpu)

        print(f"Feature List: {feature_list}")  # Debugging feature list

        pred_value = prediction(feature_list)
        
        if pred_value is not None:
            pred_value = round(np.round(pred_value[0], 2) * 221, 3)
        else:
            pred_value = "Error in prediction"

    return render_template('index.html', pred_value=pred_value)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
