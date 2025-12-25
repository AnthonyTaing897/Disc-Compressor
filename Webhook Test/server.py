from flask import Flask, request, abort
from waitress import serve

app = Flask(__name__)

@app.route('/webhook')
def index():
    return "Hello, world."

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    
    else:
        abort(400)





if __name__ == "__main__":
    
    serve(app,host = '0.0.0.0', port=8080,url_prefix="/discCompress")