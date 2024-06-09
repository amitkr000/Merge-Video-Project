from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

def AddTextVideo(windowsize=(1920,1080), Text="Hello", font='Arial', fsize=60, textcolor='white', textpos=('center','center'), duration=2, bgcolor=(0, 0, 0)):
    """
    Create a video clip with given text in center

    Return the Video clip

    Parameters
    -----------
    windowsize (Default = (1920,1080))
      The frame size of video clip. For example - 1920x1080.
    
    Text (Default = "Hello")
      The text which will displayed in the video clip.
    
    font (Default = "Arial")
      font style

    textcolor (Default = "white")
      font color
    
    textpos (Default = ('center','center'))
      font position on screen

    duration (Default = 2 sec)
      clip duration

    bgcolor (Default = (0, 0, 0))
      clip background color
      
    """
    # Create a blank clip with white background
    background_clip = ColorClip(windowsize, color=bgcolor).set_duration(duration)

    # Create a TextClip with "Hello" text
    text_clip = TextClip(Text, fontsize=fsize, color=textcolor, font=font, size=windowsize)

    # Position the text clip in the center
    text_clip = text_clip.set_position(textpos).set_duration(duration)

    # Composite the text clip on top of the background clip
    final_clip = CompositeVideoClip([background_clip, text_clip])

    return final_clip

    # Write the final clip to a file
    # final_clip.write_videofile("hello_clip.mp4", fps=24)

if __name__ == "__main__":
    AddTextVideo()