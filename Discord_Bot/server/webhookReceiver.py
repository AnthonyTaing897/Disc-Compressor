import discord
import requests
from pathlib import Path
from flask import Flask, request, abort
from waitress import serve
from server.func.Compress_Video_Function import compressVid
import threading
import shutil

app = Flask(__name__)
_bot = None

def init_webhook_reciever(bot, host='0.0.0.0', port=8080, url = '/discCompress'):
    global _bot
    _bot = bot

    def _serve():
        serve(app, host=host, port=port, url_prefix=url)

    t = threading.Thread(target=_serve,daemon=True)
    t.start()

@app.route('/webhook')
def index():
    return "Discord Bot Webhook Receiver."

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json() or {}
        print(data)
        
        user_id = data.get('data').get('UserID')
        session_id = data.get('data').get('SessionID')
        urls = data.get('data').get('url', [])
        if _bot is not None:
            
            filename = f"Discord_Bot\cmds\Library\Temp_Videos\{session_id}.mp4" 
            

            # Currently only one file is ever given this might change in the future
            try:
                response = requests.get(urls)
                print(response)
                    #We need to change this to a unique file name each time to avoid overwriting
                with open(filename, 'wb') as f:
                    f.write(response.content)
                    f.close()
            except Exception as e:
                print(f"Error downloading file from {urls}: {e}")

            filepath = sendCompressedVideo(str(user_id),str(session_id),urls,filename)

            return {"status": "success"}
        else:
            abort(500)
    
    else:
        abort(400)


def sendCompressedVideo(user_id:str, session_id:str,file_paths,filename):
    if file_paths:
                
            processedVid = compressVid(video_file=filename,
                                    processed_drct="Discord_Bot\cmds\Library\Processed_Videos",
                                    filename=f"{session_id}.mp4",
                                    target_file_size=8,
                                    compressAudio=True)
            
            async def send_message(proc_file_path, user_id):
                    try:
                        user = await _bot.fetch_user(int(user_id))
                        await user.send("Here is your compressed video:",file=discord.File(proc_file_path))

                    except Exception as e:
                        print(f"Error sending message to user {user_id}: {e}")
            
            _bot.loop.create_task(send_message(processedVid, user_id))\
            
            return processedVid
    else:
        print("No file paths provided.")


if __name__ == "__main__":
    init_webhook_reciever(None)