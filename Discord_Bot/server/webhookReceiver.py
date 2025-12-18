import discord
from flask import Flask, request, abort
from waitress import serve
import threading

app = Flask(__name__)
_bot = None

@app.route('/webhook')
def index():
    return "Discord Bot Webhook Receiver."

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json() or {}
        print(data)
        urls = data.get('data')
        print(urls)
        '''
        user_id = data.get('payload').get('data').get('UserID')
        print(user_id)
        if int(user_id) == 1:
            abort(400)

        if _bot and user_id:
            
            async def send_message():
                thing = discord.File('Thing.png')
                try:
                    user = await _bot.fetch_user(int(user_id))
                    await user.send(file = thing)
                except Exception as e:
                    print(f"Error sending message to user {user_id}: {e}")
            
            _bot.loop.create_task(send_message())

        '''
        return 'success', 200
    
    else:
        abort(400)


def init_webhook_reciever(bot, host='0.0.0.0', port=8080, url = '/discCompress'):
    global _bot
    _bot = bot

    def _serve():
        serve(app, host=host, port=port, url_prefix=url)

    t = threading.Thread(target=_serve,daemon=True)
    t.start()

if __name__ == "__main__":
    init_webhook_reciever(None)
    while True:
        pass