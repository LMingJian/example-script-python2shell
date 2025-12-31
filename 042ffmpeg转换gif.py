import os.path
import shutil
import subprocess
import time


class C2Gif:

    def __init__(self):
        if shutil.which('ffmpeg') is None:
            raise 'Error: Please set ffmpeg in the path'

    @staticmethod
    def check():
        command = "ffmpeg -version"
        ffmpeger = subprocess.Popen(command,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='UTF-8')
        output, error = ffmpeger.communicate()
        print(output)
        print(error)

    @staticmethod
    def cfile2gif(file_path, fps=30, scale=1080):
        """
        ffmpeg -i input.webm -vf "fps=15,scale=600:-1:flags=lanczos,palettegen" -y palettegen.png
        ffmpeg -i input.webm -i palettegen.png -lavfi "fps=15,scale=600:-1:flags=lanczos[x];[x][1:v]paletteuse" -gifflags -transdiff -y output.gif
        param '-ss 00:00:01' to set the start
        ffmpeg -i input.mp4 -vf "scale=480:-1:flags=lanczos,fps=15" -gifflags -transdiff -y output.gif
        """
        command_paletteuse = f'ffmpeg -i {file_path} -vf "fps={fps},scale={scale}:-1:flags=lanczos,palettegen" -y paletteuse.png'
        command_gif = f'ffmpeg -i {file_path} -i paletteuse.png -lavfi "fps={fps},scale={scale}:-1:flags=lanczos[x];[x][1:v]paletteuse" -gifflags -transdiff -y {file_path}.gif'
        ffmpeger = subprocess.Popen(command_paletteuse, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    encoding='UTF-8')
        output, error = ffmpeger.communicate()
        print(output)
        print(error)
        time.sleep(2)
        ffmpeger = subprocess.Popen(command_gif, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    encoding='UTF-8')
        output, error = ffmpeger.communicate()
        print(output)
        print(error)
        time.sleep(2)
        os.remove('paletteuse.png')
        print('Complete')

    @staticmethod
    def cfile2mp3(file_path):
        """
        ffmpeg -i input.mp4 -vn -c:a copy output.mp3
        """
        command_voice = f'ffmpeg -i {file_path} -f mp3 -vn {file_path}.mp3'
        ffmpeger = subprocess.Popen(command_voice,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='UTF-8')
        output, error = ffmpeger.communicate()
        print(output)
        print(error)
        print('Complete')


if __name__ == '__main__':
    C2Gif().check()
