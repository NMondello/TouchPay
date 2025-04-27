from flask import Flask, request, jsonify, Response
import json

app = Flask(__name__)

@app.route('/make_payment', methods=['GET'])
def make_payment():
    return jsonify({
        'status': 'arch',
        'message': 'Payment processed successfully'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)