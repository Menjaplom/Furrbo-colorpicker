from flask import Flask, render_template, request, redirect, jsonify
import serial

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route("/set_color", methods=['POST'])
def update():
    if request.method == "POST":
        try:
            color_data = request.get_json()
            print(color_data)
            print(color_data['r'])
            out_data = "S" + str(color_data['r']).zfill(3)+ str(color_data['g']).zfill(3)+ str(color_data['b']).zfill(3)+ str(int(255.0*color_data['a'])).zfill(3)
            print(out_data)
            ser.write(str(out_data).encode('ascii'))
            results = {'processed': 'true'}
            return jsonify(results)
        except Exception as err:
            print('update dia failed')
            results = {'processed': 'false'}
            return 'Operation not done (exception)', 500