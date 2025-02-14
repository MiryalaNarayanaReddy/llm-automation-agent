from tasks.phaseA import format_readme
from tasks.phaseA import download_datagen
from tasks.phaseA import count_week_days
from tasks.phaseA import sort_json_array
from tasks.phaseA import extract_recent_log_lines

import json

def execute_task(name, args):
     
    print("------------------------------")
    print("name", name)
    print("arguments", args)

    if name == "data_generation_task":
        download_datagen(url=args["url"], email=args["email"])

    elif name == "format_readme":
        format_readme(path=args["path"], prettier_package=args["prettier_package"])
    
    elif name == "count_week_days":
        count_week_days(file_path=args["file_path"], day=args["day"], output_path=args["output_path"])
    
    elif name == "sort_json_array":
        sort_json_array(input_path=args["input_path"], output_path=args["output_path"], sort_keys=args["sort_keys"])

    elif name == "extract_recent_log_lines":    
        extract_recent_log_lines(logs_directory=args["logs_directory"], output_path=args["output_path"], num_files=args["num_files"], line_number=args["line_number"])  

    else:
        print("Function not found")

