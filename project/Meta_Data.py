import subprocess
import shlex


def execute_ffprobe():
    cmd = "ffprobe  -i /home/doge/chun.mkv -hide_banner -print_format json -v quiet -show_streams"
    test = subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout = subprocess.check_output(shlex.split(cmd)).decode('utf-8')
    output = stdout
    print(output)
    #print(test.communicate()[0].decode('utf-8'))

def execute_ffmpeg():
    cmd = "ffmpeg -i /home/doge/chun.mkv -f ffmetadata"
    stdout = subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = stdout.communicate()[0].decode('utf-8')
    res=output.split("\n")
    for r in res:
        if ("ARTIST") in r:
            print(r)
        if "DATE" in r:
            print(r)
        if "title" in r:
            print(r)


execute_ffprobe()
execute_ffmpeg()
