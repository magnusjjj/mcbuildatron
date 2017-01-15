import argparse
import json
from git import Repo
import os
import distutils.dir_util


parser = argparse.ArgumentParser(description='Build minecraft mods')
parser.add_argument('mod')

args = parser.parse_args()

f = open('packages/' + args.mod + '/recipe.json', 'r')
recipe = json.loads(f.read())
f.close()

moddir = 'packages/' + args.mod + '/' + args.mod

if not os.path.isdir(moddir):
	repo = Repo.clone_from(recipe["github"], moddir, recursive=True)
	if "addgradlew" in recipe and recipe["addgradlew"]:
		print("Adding gradlew")
		distutils.dir_util.copy_tree("libraries/gradlew",moddir)
os.chdir(moddir)
os.system(recipe["commandrun"])
