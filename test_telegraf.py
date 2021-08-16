from flask import Flask, request

app = Flask(__name__)

@app.route('/telegraf', methods=['POST'])
def get_metrics():
    if not request.is_json:
        return '', 404
    info = request.get_json()
    print(info)
    return '', 200


if __name__ == '__main__':
    #serve(app, host='192.168.15.103', port=5000)
    app.run(host='127.0.0.1', port=8080)