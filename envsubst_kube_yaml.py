import yaml
import json
import os

### USAGE
# - Make a dir called k8s-all/
# - Inside that dir: put kube (or any type of) yaml files, with env substitions as needed. ie. 
# image: ${IMAGE}
# name: ${MYNAME}
# i.e. parameterize like your doing envsubst all day long.
# - Output: A stream of parameterized yaml.
# - Result: You can throw helm/short/envsubst whatever other complex program your using to sed replace away.
# - Make sure you update params below to have your parameters that you want to substitute.
params = {
    "${IMAGE}":"nginx:1.0", # b/c every kube example needs to have nginx somewhere
    "${B}":"b, look, a substitution",
    "${C}":"another substituted value"
}

def getSub(input):
    for key,value in params.items():
        # if not needed, but useful for debugging since i suck at python
        if input.find(key) >= 0:
            return input.replace(key,value)
    return input

def varReplace(input):
    if type(input) is list:
        for i in range(len(input)):
            if type(input[i]) is str:
                input[i] = getSub(input[i])
            else:
                input[i] = varReplace(input[i])

    if type(input) is dict:
        for key, value in input.items():
            if type(value) == str:
                input[key] = getSub(value)
            else:
                input[key] = varReplace(value)
    return input

for f in os.listdir("k8s-all"):
    with open("k8s-all/"+f, "r") as stream:
        try:
            yamls=list(yaml.load_all(stream))
            for i in range(len(yamls)):
                substitutedYaml=varReplace(yamls[i])
                print (yaml.dump(yaml.load(json.dumps(substitutedYaml)), default_flow_style=False))
        except yaml.YAMLError as exc:
            print(exc)
