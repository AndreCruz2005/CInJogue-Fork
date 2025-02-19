import json, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from main import MainWindow, QApplication
app = Flask(__name__)
CORS(app)

@app.route('/submit-message', methods=['POST'])

def submit_message():
    try:
        data = request.get_json()
        print("Received data:", data)
        message = data.get('message')
        if not message:
            return jsonify({'error':'Nenhuma mensagem encontrada'}), 400
        App = QApplication(sys.argv)
        window = MainWindow()
        window.ai_response(message)
        return jsonify({'status':'sucesso', 'message':'Mensagem recebida'}),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route ('/send-library', methods=['GET'])

def send_library():
    with open ("./user_data.json", 'r') as file:
        if not file:
            return jsonify({'status':'erro', 'message':'Json não aberto'})
        user_data = json.load(file)
    return jsonify(user_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    