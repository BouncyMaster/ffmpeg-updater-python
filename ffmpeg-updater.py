from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
from os import listdir, remove, rename
from shutil import rmtree
from sys import path
import zipfile

ffmpeg_system = "win64-static" #you can change this to win32-static or macos64-static depending on your system

class MyOpener(FancyURLopener): #ffmpeg site needs an User Agent to allow retrieving
	version = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
myopener = MyOpener()

def check_new_ver():
	global new_ver
	
	url = "https://ffmpeg.zeranoe.com/builds/"
	html = myopener.open(url).read()
	soup = BeautifulSoup(html, "html5lib")
	
	# kill all script and style elements
	for script in soup(["script", "style"]):
		script.extract() # rip it out
	
	# get text
	text = soup.get_text()
	
	ver_find = text.find("Version")
	new_ver = text[ver_find+59:ver_find+75]

def check_curr_ver():
	global curr_ver
	
	dir_list = str(listdir("./ffmpeg"))
	ffmpeg_folder = dir_list.find("ffmpeg")
	curr_ver = dir_list[ffmpeg_folder+7:ffmpeg_folder+23]

def new_ver_install():
	if new_ver != curr_ver:
		myopener.retrieve("https://ffmpeg.zeranoe.com/builds/" + ffmpeg_system[:5] + "/" + ffmpeg_system[6:] + "/ffmpeg-" + new_ver + "-" + ffmpeg_system + ".zip", "ffmpeg-" + new_ver + "-" + ffmpeg_system + ".zip")
		with zipfile.ZipFile("ffmpeg-" + new_ver + "-" + ffmpeg_system +".zip","r") as zip_ref:
			zip_ref.extractall("./")
		remove("ffmpeg-" + new_ver + "-" + ffmpeg_system + ".zip")
		rmtree("ffmpeg")
		rename("ffmpeg-" + new_ver + "-" + ffmpeg_system, "ffmpeg")
		open("./ffmpeg/ffmpeg-" + new_ver + "-" + ffmpeg_system, "w+")

if __name__ == "__main__":
	check_new_ver()
	check_curr_ver()
	new_ver_install()
