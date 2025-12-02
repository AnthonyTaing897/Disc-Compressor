import ffmpeg

def alterVideo (video_file,filename):
    process_path = f"Discord_Bot\Commands\Processed_Videos\{filename}_compressed.mp4"

    video = ffmpeg.input(video_file)
    audio = video.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
    video = video.video.hflip()
    output = ffmpeg.output(audio, video, process_path)
    
    ffmpeg.run(output, overwrite_output=True)
    return process_path