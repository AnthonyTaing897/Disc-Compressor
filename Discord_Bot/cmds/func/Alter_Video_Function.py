import ffmpeg
from pathlib import Path

def alterVideo (video_file:Path,processed_drct:Path,filename:Path) -> Path:
    process_path = f"{processed_drct}/{filename}_compressed.mp4"
    print(process_path)

    video = ffmpeg.input(video_file)
    audio = video.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
    video = video.video.hflip()
    output = ffmpeg.output(audio, video, process_path)
    
    ffmpeg.run(output, overwrite_output=True)
    return process_path


if __name__ == "__main__":
    alterVideo("VID_20241008_165811182.mp4","Discord_Bot\cmds\Library\Processed_Videos","VID_20241008_165811182")