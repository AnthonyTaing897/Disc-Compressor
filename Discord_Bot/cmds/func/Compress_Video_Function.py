#Testing compression function will add to commandGog when completed

import ffmpeg
from pathlib import Path

def compressVid (video_file:Path,processed_drct:Path,filename:Path, target_file_size: int) -> Path:
    #file size (mbs)
    file_size = target_file_size * 1000
    
    probed_vid = ffmpeg.probe(str(video_file))

    #Video duration (secs)
    vid_duration = float(probed_vid['format']['duration'])

    #Audio bitrate (bps)
    audio_bitrate = float(next((s for s in probed_vid['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    
    print(audio_bitrate)

    #Previous code
    '''
    process_path = f"{processed_drct}/{filename}_compressed.mp4"
    print(process_path)

    video = ffmpeg.input(video_file)
    audio = video.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
    video = video.video.hflip()
    output = ffmpeg.output(audio, video, process_path)
    
    ffmpeg.run(output, overwrite_output=True)
    return process_path'''


if __name__ == "__main__":
    compressVid("VID_20241008_165811182.mp4","Discord_Bot\cmds\Library\Processed_Videos","VID_20241008_165811182",8)