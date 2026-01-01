import discord
import requests
from flask import Flask, request, abort
from waitress import serve
from server.func.Compress_Video_Function import compressVid
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
        
        
        user_id = data.get('data').get('UserID')
        session_id = data.get('data').get('SessionID')
        urls = data.get('data').get('url', [])

        sendCompressedVideo(user_id,session_id,urls)
        return {"status": "success"}
    
    else:
        abort(400)

def sendCompressedVideo(user_id, session_id,file_paths):
    if file_paths and _bot:
            filename = session_id + ".mp4"

            # Currently only one file is ever given this might change in the future
            for url in file_paths:
                try:
                    x = url.get('url')
                    response = requests.get(x)
                    #We need to change this to a unique file name each time to avoid overwriting
                    with open(f"Discord_Bot/cmds/Library/Temp Videos/{filename}", 'wb') as f:
                        f.write(response.content)
                        f.close()
                except Exception as e:
                    print(f"Error downloading file from {url}: {e}")
                
            processedVid = compressVid(video_file="Temp Videos/testfile.mp4",
                                    processed_drct="Discord_Bot/cmds/Library/Processed_Videos",
                                    filename="testfile.mp4",
                                    target_file_size=8,
                                    compressAudio=True)
            
            async def send_message(file_path, user_id):
                    try:
                        user = await _bot.fetch_user(int(user_id))
                        await user.send("Here is your compressed video:")  
                        await user.send(file=discord.File(file_path))
                    except Exception as e:
                        print(f"Error sending message to user {user_id}: {e}")
            
            _bot.loop.create_task(send_message(processedVid, user_id))

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