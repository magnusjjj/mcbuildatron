import argparse
import json
#from git import Repo, RemoteProgress
import os
import distutils.dir_util
import logging
from subprocess import call
#logging.basicConfig(level=logging.INFO)
#type(myrepo.git).GIT_PYTHON_TRACE='full'

parser = argparse.ArgumentParser(description='Build minecraft mods')
parser.add_argument('mod')

args = parser.parse_args()

f = open('recipes/' + args.mod + '/recipe.json', 'r')
recipe = json.loads(f.read())
f.close()

moddir = 'output/' + args.mod + '/'



if not os.path.isdir(moddir):
	#repo = Repo.clone_from(recipe["github"], moddir, recursive=True, with_extended_output=True)
	call(["git", "clone", "--recursive", recipe["github"], moddir])
	if "addgradlew" in recipe and recipe["addgradlew"]:
		print("Adding gradlew")
		distutils.dir_util.copy_tree("libraries/gradlew",moddir)

os.chdir(moddir)
os.system(recipe["commandrun"])
