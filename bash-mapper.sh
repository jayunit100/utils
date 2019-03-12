# bashmapper is a python script that outputs either graphviz
# or environment variable <-> file mappings.
# run it from a directory that has a maze of shell scripts and env vars, 
# and you'll be able to tease out the way the environment variables
# are referenced and plumbed through the codebase

import os
import glob

files = {}
envs = {}

def checkAndWriteEnvs(filename):
    global envs
    global files
    global files_using_envs
    global envs_in_files

    valid = False
    try:
        fh = open(filename, 'r')
        valid = True
    except:
        pass

    if valid:
        with open(filename, 'r') as sourcecode:
            for line in sourcecode:
                if "export" in line:
                    line=line.split(" ")[1]
                splitchars=["if [ ", "if [[","local ","$","[`$","const"]
                for s in splitchars:
                    if s in line:
                        line=line.split(s)[1]

                line=line.replace("\"","_")
                if "=" in line:
                    env_key = line.split("=")[0]
                    env_key=env_key.strip()
                    # env_value = line.split("=")[1]
                    if env_key not in envs:
                        envs[env_key]=[]
                    if filename not in files:
                        files[filename]=[]
                    if env_key[0].isupper():
                        envs[env_key].append(filename)
                        files[filename].append(env_key)

srcfiles=[]
for filename in glob.iglob('./**/*.sh', recursive=True):
    srcfiles.append(filename)
for filename in glob.iglob('./**/*.env', recursive=True):
    srcfiles.append(filename)
for filename in srcfiles:
    skipIt = ["test","authbs","node"]
    parseIt = True
    for k in skipIt:
        if k in filename:
            parseIt=False
    if parseIt:
        checkAndWriteEnvs(filename)

graphviz=0
hierarchy=1
if graphviz==1:
    print("digraph {")
    for e in envs:
        print('"',e,'"', "->", '"',filename,'"', ';')
    print("}")

if hierarchy==1:
    for e in files:
        if len(files[e]) > 0:
            print(e, " -> ", files[e])
    print("envs: ",len(envs))
    print("files: ",len(files))
