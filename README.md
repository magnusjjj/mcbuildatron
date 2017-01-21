# mcbuildatron

A, for now, super simple proof of concept for a minecraft automatic mod builder.
It does the job of:
- Cloning a repository
- Possibly showing gradlew in there if its needed
- Compiling the mod

# Dependencies
- JDK, found here: http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
- Git for windows, found here: https://git-scm.com/download/win

# How to use
- Open a command line window in the directory
- Type 'builder ae2' to compile Applied Energistics 2 , and wait. If it looks like it does absolutely nothing, its probably downloading the source silently.
- If successfull, the built mod should exist in ae2/ae2/build/libs

# Known major problems

- Just flat out errors out if you don't have JDK or git with non-friendly messages.
- Does not 'pull' changes from repositories, it just clones it
- It does not handle changes to recipies gracefully, you have to delete the output directory
- Some of the recipies do not actually work. Looks like they might have external dependencies that might need downloading and put somewhere.
- There is no linux support tested. There is no reason why it shouldn't work with a few super tiny changes though. Patches are, as always, super welcome.

# How does it work

It has a bunch of 'recipies' in the packages/ directory.
For example, the recipie for Applied Energistics 2 is:
```
{
	"github": "https://github.com/AppliedEnergistics/Applied-Energistics-2",
	"commandrun": "gradlew setupCIWorkspace build"
}
```

Its a json encoded file, that as of now only has the repository parameter and what command to run to build it.
There is a sample directory you can copy, aptly named 'sample' :)

Contact me at magnusjjj on skype, magnusjjj@gmail.com for mail.

# How to contribute/licensing

Check the license file. This tool is licensed under the MIT license, but has other dependencies.

If you want to write recipies, go nuts, and if you want to, add a pull request.

Will only *merge* recipies for mods that are licensed under OSI-approved licenses (https://opensource.org/licenses), with the following exceptions that will be allowed:

- MMPL, all current versions
- CC0
- WTFPL

Be sure to send a pull request though! I welcome it, and we can leave a handy note in there, and we could probably eventually work it into a contrib repo with warnings, or just have it laying around if a mod author decides to play along :).
