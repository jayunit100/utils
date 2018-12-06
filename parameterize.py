import yaml
import os

params = {
    "${MY_IMAGE_NAME}":"nginx:1.0.0",
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
            print("--")
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

for f in os.listdir("my-kube-yamls"):
    with open("my-kube-yamls/"+f, "r") as stream:
        try:
            yamls=list(yaml.load_all(stream))
            for i in range(len(yamls)):
                print(varReplace(yamls[i]))
        except yaml.YAMLError as exc:
            print(exc)
