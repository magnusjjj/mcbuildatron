import urllib.request
from subprocess import call
import zipfile
import os
import shutil

interpretername="libraries/python-3.6.0-embed-win32/python"
interpreterzip="libraries/python-3.6.0-embed-win32/python36.zip"
extractedpath="libraries/python-3.6.0-embed-win32/extracted"

print("Welcome! Before we get started, make sure that you have both the JDK, that you can find here:")
print("http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html")
print("And git-windows, found here:")
print("https://git-for-windows.github.io/")

input('Press enter to go further:')

#if shutil.which("javac") is None:
#	print("For this program to work, you are going to need the JDK, Java Development Kit. You can download it from here:")
#	print("http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html")
#	exit()

if shutil.which("git") is None:
	print("The last external dependency we need is Git. You can find it on:")
	print("https://git-for-windows.github.io/")
	print("Make sure not to uncheck the option to add it on your path.")
	exit()

print("Hi! We are going to download some dependencies.")
if not os.path.exists("getpip.py"):
	print("First up, a downloader script for pip, the python package manager. Don't worry, this will all be contained in the build directory. Super sanitary <3")
	urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "getpip.py")
else:
	print("Looks like we already downloaded pip")

print("Next up, we run the installer for pip")
call([interpretername, "getpip.py"])

if not os.path.exists(extractedpath):
	print("Now we need to extract the python library zip, to fix some standing issues with pip.")
	zip_ref = zipfile.ZipFile(interpreterzip, 'r')
	zip_ref.extractall(extractedpath)
	zip_ref.close()
else:
	print("Looks like we already extracted the python library")
if os.path.exists(interpreterzip):
	print("Time to remove the old python zip")
	os.remove(interpreterzip)

print("Finally, we should be good to go. Time to download the python packages we need.")
call([interpretername, "-m", "pip", "install", "--requirement", "requirements.txt"])

print("All done! You can close this window now :)")