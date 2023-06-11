import subprocess
from pytube import YouTube
from pytube import exceptions
from pytube.cli import on_progress
from moviepy.editor import VideoFileClip


def convert_to_mp3():
    global file_name
    for symbol in '\\/:*?"<>|':
        file_name = file_name.replace(symbol, '')
    video = VideoFileClip(get_video())
    audio = video.audio
    audio.write_audiofile(f'{path}\\{file_name}.mp3')
    video.close()
    audio.close()


def get_audio():
    itag = [18, 22, 134, 135, 243, 244]
    for i in itag:
        audio_file = yt.streams.get_by_itag(i)
        audio_file.download(output_path=path, filename=f'{file_name}.mp3')
        break


def get_video():
    video_file = yt.streams.get_highest_resolution()
    return video_file.download(output_path=path)


output = subprocess.check_output(r'powershell -command "[Environment]::GetFolderPath(\"Desktop\")"')
path = output.decode().strip()

while True:
    try:
        yt = YouTube(input('link: '), on_progress_callback=on_progress)
        file_name = yt.title
        mode_selection = input('Choose one and press 1-2-3:\n'
                               '1. Download audio\n'
                               '2. Download video\n'
                               '3. Download video and audio')
        match mode_selection:
            case '1':
                get_audio()
            case '2':
                get_video()
            case '3':
                convert_to_mp3()
            case _:
                print('Wrong choice, try again')
                continue

        print('Starting process...')
        break
    except exceptions.RegexMatchError:
        print('Unknown link, try again')
    except exceptions.AgeRestrictedError:
        print("This video is age restricted, and can't be accessed without logging in.")
    except exceptions.VideoPrivate:
        print("This is a private video, and unable to access")
    except exceptions.VideoUnavailable:
        print('This video is unavalable')
