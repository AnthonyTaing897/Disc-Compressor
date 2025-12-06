#Testing compression function will add to commandGog when completed

import ffmpeg
from pathlib import Path

def compressVid (video_file:Path,processed_drct:Path,filename:Path, target_file_size: int, compressAudio = False) -> Path:
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    # File size (in bytes)
    target_size = target_file_size * 1024 * 1024

    probed_vid = ffmpeg.probe(str(video_file))

    # Video duration (secs)
    vid_duration = float(probed_vid['format']['duration'])

    # Audio bitrate (bps)
    audio_bitrate = float(next((s for s in probed_vid['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])

    # Calculate target video bitrate (bps) 
    target_bitrate = ((target_size * 8) / (1.073741824 * vid_duration)) 

    # Calculate target audio bitrate (bps)
    if compressAudio and 10 * audio_bitrate > target_bitrate:
        audio_bitrate = target_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate

    # Video bitrate (bps)
    video_bitrate = target_bitrate - audio_bitrate

    video = ffmpeg.input(video_file)
    
    compressed_video_filepath = f"{processed_drct}/{Path(filename).stem}_compressed.mp4"


    
    ffmpeg.output(video, compressed_video_filepath,
                  vcodec = 'libx264',
                  video_bitrate = int(video_bitrate),
                  audio_bitrate = int(audio_bitrate),
                  format='mp4').run(overwrite_output=True)

    final_size = Path(compressed_video_filepath).stat().st_size

    print(f"-----------\nTarget size: {target_size} bytes")
    print(f"Final size: {final_size} bytes\n-----------") 

    return Path(compressed_video_filepath)

if __name__ == "__main__":
    compressVid(Path("Shotgun Wedding Trailer.mov"),"Discord_Bot\cmds\Library\Processed_Videos",Path("Shotgun Wedding Trailer.mov"),9,False)