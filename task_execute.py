from tasks.phaseA import format_readme
from tasks.phaseA import download_datagen
import json

def execute_task(name, args):
     
    print("------------------------------")
    print("name", name)
    print("arguments", args)

    if name == "data_generation_task":
        download_datagen(url=args["url"], email=args["email"])

    elif name == "format_readme":
        format_readme(path=args["path"], prettier_package=args["prettier_package"])

    else:
        print("Function not found")

