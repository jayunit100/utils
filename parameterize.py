params = {
    "${NAME}":"jay",
    "${NAME2}":"jaysus",
}

inputJson = {
    "id100":{
        "address":"123 j st","name":"${NAME}"
    },
    "id101":{
        "address":"123 j st","name":"${NAME}","otherName":"${NAME2}"
    }
}

def getSub(input):
    for key,value in subs.items():
        # if not needed, but useful for debugging since i suck at python
        if input.find(key) >= 0:
            return input.replace(key,value)
    return input

def varReplace(input):
    if type(input) is list:
        for i in range(len(input)):
            print("--")
            if type(value) is string:
                input[i] = getSub(d[i])
            else:
                input[i] = varReplace(d[i])

    if type(input) is dict:
        for key, value in input.items():
            if type(value) == str:
                input[key] = getSub(value)
            else:
                input[key] = varReplace(value)
    return input

parameterizedYaml=varReplace(a)
print(parameterizedYaml)
