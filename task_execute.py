from tasks.phaseA import format_readme
import json

def execute_task(name, arguments):
    print("name", name)
    print("arguments", arguments)
    if name == "format_readme":
        # arguments['path'] = "." + arguments['path']
        args = json.loads(arguments)
      
        format_readme(path=args["path"], prettier_package=args["prettier_package"])
    else:
        print("Function not found")

