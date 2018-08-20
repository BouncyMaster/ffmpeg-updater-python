from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
from os import listdir, remove
from shutil import rmtree
from sys import path
import zipfile

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
		script.extract()    # rip it out
	
	# get text
	text = soup.get_text()
	
	ver_find = text.find("Version")
	new_ver = text[ver_find+59:ver_find+75]

def check_curr_ver():
	global curr_ver
	
	dir_list = str(listdir("./"))
	ffmpeg_folder = dir_list.find("ffmpeg")
	curr_ver = dir_list[ffmpeg_folder+7:ffmpeg_folder+23]

def new_ver_install():
	if new_ver != curr_ver:
		myopener.retrieve("https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-" + new_ver + "-win64-static.zip", "ffmpeg-" + new_ver + "-win64-static.zip") #You need to change win64-static to win32-static or macos64-static depending on your system
		with zipfile.ZipFile("ffmpeg-" + new_ver + "-win64-static.zip","r") as zip_ref: #this also
			zip_ref.extractall("./")
		remove("ffmpeg-" + new_ver + "-win64-static.zip") #this also
		rmtree("ffmpeg-" + curr_ver + "-win64-static") #this also

if __name__ == "__main__":
	check_new_ver()
	check_curr_ver()
	new_ver_install()