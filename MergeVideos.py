from moviepy.editor import VideoFileClip, concatenate_videoclips
from TextVideo import AddTextVideo
import os

def convert_sec_duration_to_hms(duration: float):
    """
    Conversion of duration in seconds into Hours:minutes:seconds format.

    Return a string of Hours:minutes:seconds.

    Parameters
    -----------
    duration (float)
      The amount of time in seconds only. For example: 1 hour will be passed as 3600 sec.
    """
    # Condition step is done to always get in "00:00:00" this format
    hours = int(round(duration // 3600, 2))
    hours = f"{hours}" if (hours >= 10) else f"0{hours}"

    minutes = int(round((duration % 3600) // 60, 2))
    minutes = f"{minutes}" if (minutes >= 10) else f"0{minutes}"

    seconds = int(round(duration % 60, 2))
    seconds = f"{seconds}" if (seconds >= 10) else f"0{seconds}"

    # return f"{hours}:{minutes}:{seconds}"
    return hours+":"+minutes+":"+seconds



def merge_videos(video_files: str, output_path: str, output_filename: str, text_clip_duration: int=4):
    """
    merges the videos and creates a timestamp text files
    """
    clips = []
    merge_times = []
    titles = []
    prev_clip_duration = 0


    for i,file in enumerate(video_files):
        clip = VideoFileClip(file)
        title = os.path.splitext(os.path.basename(file))[0]
        text = f"Chapter {i+1}\n{title}"
        titles.append(title)
        title_clip = AddTextVideo(Text=text, duration=text_clip_duration, windowsize=clip.size, fsize=60, bgcolor=(54, 69, 79))

        merge_times.append(convert_sec_duration_to_hms(prev_clip_duration))
        clips.append(title_clip)
        clips.append(clip)
        prev_clip_duration += clip.duration + text_clip_duration

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_path+output_filename+".mp4", codec='h264_nvenc', fps=clips[0].fps)

    final_video.close()

    # Write merge times to a text file
    with open(output_path+output_filename+".txt", "w") as f:
        for i, time in enumerate(merge_times):
            f.write(f"{time} {titles[i]}\n")






if __name__ == "__main__":
    OutputVideo_name = input("Enter the Output Video file name : ")
    text_name = input("Enter the Output Timestamp file name(Default=Video name) : ")
    Outputtimestamp_name = text_name if text_name != '' else OutputVideo_name
    folder_path = "D:/MOOCS/New/Unity Android  Build 3D ZigZag Racing Game with Unity & C#/03 Creating The Basic Game Play/"
    Output_path = "D:/MOOCS/New/Unity Android  Build 3D ZigZag Racing Game with Unity & C#/Combine_Output/"

    # Get a list of all video files in the folder
    video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(('.mp4', '.avi', '.mov'))]

    # folder_path = "test/"
    # video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]  # Add your video files here
    video_files = [os.path.join(folder_path+v) for v in video_files]
    print(len(video_files))
    # merge_videos(video_files, [OutputVideo_name, Outputtimestamp_name], Output_path)
    merge_videos(video_files, Output_path, OutputVideo_name)
