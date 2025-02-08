import subprocess
from datetime import date
from tts_azure import text_to_speech
from select_design import pick_design
import os
from database import retrieve_random_joke
import json

# ----------------- Read joke and clean joke format ----------------- 
with open("./design.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mydate = date.today()
datum = str(mydate)

# ----------------- Design picker ----------------- 
designNr = pick_design(mydate)

design = next((item for item in data if item["designNr"] == designNr), None)

# ----------------- Get random joke ----------------- 
joke_text_orig = retrieve_random_joke()

if joke_text_orig is None:
    print(f"Joke not found.")
else:
    joke_text = joke_text_orig.replace('\"\"', '\\\"')
    joke_text = joke_text.replace(':', '\\:')

# ----------------- Turn joke into multiple lines ----------------- 
def wrap_text(text, max_length):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)

# ----------------- Variables for ffmpeg filters and command ----------------- 

witz = 'Witz'
des_tages = 'des Tages'
credit = 'Designed by Freepik'
joke_text_wrapped = wrap_text(joke_text, 20)

bg_white = "color=color=white:size=1920x1080:rate=50"
bg_blue = f"color=color={design['bg_color']}:size=1920x1080:rate=50"

font_size_title = 95
font_size_date = 50

# Text: Witz (in title)
witz_location = 'H/2-text_h-50'

text_in_witz = f'max({witz_location},(t*({witz_location}-2*H)+2*H))'
text_out_witz = f'max({witz_location},((t-4)*(2*H-{witz_location})+{witz_location}))'

shadow_in_witz = f'max({witz_location}+10,(t*({witz_location}-2*H)+2*H))'
shadow_out_witz = f'max({witz_location},((t-4)*(2*H-{witz_location})+{witz_location}))'


# Text: des Tages
desTages_loc = 'H/2-20'

text_in_des_tages = f'max({desTages_loc},((t-0.5)*({desTages_loc}-2*H+10)+2*H-10))'
text_out_des_tages = f'max({desTages_loc},((t-3.5)*(2*H-{desTages_loc})+{desTages_loc}))'

shadow_in_des_tages = f'max({desTages_loc},((t-0.5)*({desTages_loc}-2*H+10)+2*H-10))'
shadow_out_des_tages = f'max({desTages_loc},((t-3.5)*(2*H-{desTages_loc})+{desTages_loc}))'


# Text: date
date_loc = 'H/2+120'

text_in_date = f'max({date_loc},((t-1)*({date_loc}-2*H+10)+2*H-10))'
text_out_date = f'max({date_loc},((t-3)*(2*H-{date_loc})+{date_loc}))'

shadow_in_date = f'max({date_loc}+5,((t-1)*({date_loc}-2*H+10)+2*H-10))'
shadow_out_date = f'max({date_loc},((t-3)*(2*H-{date_loc})+{date_loc}))'


# Text: the joke itself
joke_size = 95
in_joke = f'((t-7)*{joke_size})'
out_joke = f'((-1)*{joke_size}*(t-12)+{joke_size})'

text_to_speech(joke_text_orig, "audio_output.wav")

# ----------------- Ffmpeg filters ----------------- 
filter_complex = " ".join((
    "[0:v]trim=duration=7,setpts=PTS-STARTPTS[white];",
    "[1:v]trim=duration=17,setpts=PTS-STARTPTS[blue];",
    f"[2:v]trim=duration=5,setpts=PTS-STARTPTS,scale={design['scale']}[bgpicture];",
    "[white][blue]overlay=x=0:y='if(gte(t,6),max(0,H-(t-6)*H/0.5),H)'[bg];",
    "[bg][bgpicture]overlay=x=(W-w)/2:y=0:enable='between(t,0,5)'[final];",
    "[final]format=yuv420p,",


    #-- Title --
    #Drop shadow title
    f"drawtext=text={witz}:x=(w/2-text_w/2)+12:y='",
        f"if(lte(t,1),{shadow_in_witz}+10,",
        f"if(lte(t,4),H/2-text_h-40,",
        f"if(lte(t,5),{shadow_out_witz}+10,H)))':",
    f"fontcolor=black:fontsize={font_size_title}:fontfile={design['title_font']},",
    
    f"drawtext=text={des_tages}:x=(w/2-text_w/2)+12:y='",
        f"if(lte(t,0.5),2*H+10,",
        f"if(lte(t,1.5),{text_in_des_tages}+10,",
        f"if(lte(t,3.5),H/2-10,",
        f"if(lte(t,5),{text_out_des_tages}+10,H))))':",
    f"fontcolor=black:fontsize={font_size_title}:fontfile={design['title_font']},",

    f"drawtext=text={datum}:x=(w/2-text_w/2)+6:y='",
        f"if(lte(t,1),2*H,",
        f"if(lte(t,2),{shadow_in_date}+5,",
        f"if(lte(t,3),{date_loc}+5,",
        f"if(lte(t,5),{shadow_out_date}+5,H))))':",
    f"fontcolor=black:fontsize={font_size_date}:fontfile={design['title_font']},",

    #Title
    f"drawtext=text={witz}:x=(w/2-text_w/2):y='",
        f"if(lte(t,1),{text_in_witz},",
        f"if(lte(t,4),H/2-text_h-50,",
        f"if(lte(t,5),{text_out_witz},H)))':",
    f"fontcolor={design['title_color']}:fontsize={font_size_title}:",
    f"fontfile={design['title_font']},",
    
    f"drawtext=text={des_tages}:x=(w/2-text_w/2):y='",
        f"if(lte(t,0.5),2*H,",
        f"if(lte(t,1.5),{text_in_des_tages},",
        f"if(lte(t,3.5),H/2-20,",
        f"if(lte(t,5),{text_out_des_tages},H))))':",
    f"fontcolor={design['title_color']}:fontsize={font_size_title}:",
    f"fontfile={design['title_font']},",

    f"drawtext=text={datum}:x=(w/2-text_w/2):y='",
        f"if(lte(t,1),2*H,",
        f"if(lte(t,2),{text_in_date},",
        f"if(lte(t,3),{date_loc},",
        f"if(lte(t,5),{text_out_date},H))))':",
    f"fontcolor={design['title_color']}:fontsize={font_size_date}:",
    f"fontfile={design['title_font']},",


    #-- Joke --
    #Drop Shadow main text
    f"drawtext=text='{joke_text_wrapped}':x=(w/2-text_w/2)+10:y=(h/2-text_h/2)+7:fontcolor=black:fontsize='",
        f"if(lte(t,7),0,",
        f"if(lte(t,8),{in_joke},95))':",
    f"alpha='if(gte(t,7), if(lte(t,17), 0.25, 0), 0)':fontfile={design['joke_font']},",

    #Main Text
    f"drawtext=text='{joke_text_wrapped}':x=(w/2-text_w/2):y=(h/2-text_h/2):",
    f"fontcolor={design['joke_color']}:fontsize='",
        f"if(lte(t,7),'0',",
        f"if(lte(t,8),{in_joke},95))':",
    f"alpha='if(gte(t,7), if(lte(t,17), 1, 0), 0)':fontfile={design['joke_font']},",


)) 

filter_complex_audio = " ".join((
    "[2:a][1:a]concat=n=2:v=0:a=1[a0];",
    "[a0]apad[audio];",
))

output_file = f"./witz_in_between.avi"

# ----------------- ffmpeg Command ----------------- 
command = [
    "ffmpeg",
    "-f", "lavfi",
    "-i", bg_white,
    "-f", "lavfi",
    "-i", bg_blue,
    "-loop", "1",
    "-i", design['bg_input'],
    "-t", "17",
    "-filter_complex", filter_complex,
    "-c:v", "libx264",
    output_file
]

# final_video = f"./daten/videos/Autogen1/10assembly/final_video.mp4"
final_video = f"./final_video.mp4"

if os.path.exists(final_video):
  os.remove(final_video)
else:
  print("The file does not exist")



command_audio = [
    "ffmpeg",
    "-i", output_file,
    "-i", "audio_output.wav",
    "-f", "lavfi",
    "-t", "8",
    "-i", "anullsrc",
    "-filter_complex", filter_complex_audio,
    "-map", "0:v",
    "-map", "[audio]",
    "-shortest",
    "-c:v", "libx264",
    final_video
]

try:
    subprocess.run(command, check=True)
    subprocess.run(command_audio, check=True)
    print("Conversion successful!")
except subprocess.CalledProcessError as e:
    print("An error occurred:", e)

if os.path.exists(output_file):
  os.remove(output_file)
else:
  print("The file does not exist")
