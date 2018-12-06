import yaml
import json
import os

############### TODO Fill these in w/ reasonable defaults.
exampleParams = {
    "${CASSANDRA_HOST}":"",
    # ...
}

# varReplace replaces input yaml with env vars in the params object.
def varReplace(input, map):
    def getSub(input):
        for key,value in map.items():
            # if not needed, but useful for debugging since i suck at python
            if input.find(key) >= 0:
                return input.replace(key,value)
        return input

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

# reads all yaml files in a directory, and substitutes them.  Returns
# corresponding yamls as a dictionary.
def getSubstitutedOrchestrationAsDict(dir, map):
    for f in os.listdir(dir):
        with open(dir+"/"+f, "r") as stream:
            try:
                yamls=list(yaml.load_all(stream))
                newyamls=[]
                for i in range(len(yamls)):
                    newyamls += varReplace(yamls[i])
                for i in range(len(newyamls)):
                    print (yaml.dump(yaml.load(json.dumps(substitutedYaml)), default_flow_style=False))
            except yaml.YAMLError as exc:
                print(exc)

#### EXAMPLE USAGE
# myKubeYAMLS = getSubstitutedOrchestrationAsDict("k8s-all",exampleParams)
# print(myKubeYamls | kubectl create -f )
