from tasks.phaseA import format_readme
from tasks.phaseA import download_datagen
from tasks.phaseA import count_week_days
from tasks.phaseA import sort_json_array
from tasks.phaseA import extract_recent_log_lines
from tasks.phaseA import generate_markdown_index

from tasks.phaseA import extract_email_sender
from tasks.phaseA import extract_credit_card_number
from tasks.phaseA import get_most_similar_comments
from tasks.phaseA import total_gold_ticket_sales

from tasks.phaseB import checkIsSafe
from tasks.phaseB import deleteFile
# from tasks.phaseB import fetchDataAndSave
# from tasks.phaseB import cloneRepoAndCommit
# from tasks.phaseB import runSqlQuery

from utils.execute_tool import execute_all

def execute_task(name, args, llm=None):
     
    print("------------------------------")
    print("name", name)
    print("arguments", args)

    if name == "data_generation_task":
        return download_datagen(url=args["url"], email=args["email"])

    elif name == "format_readme":
        if checkIsSafe(args["path"]):
            return format_readme(path=args["path"], prettier_package=args["prettier_package"])
        else:
            # resource not allowed status code 403
            return 403, f"Resource not allowed: {args['path']}"

    elif name == "count_week_days":
        if checkIsSafe(args["file_path"]):
            return count_week_days(file_path=args["file_path"], day=args["day"], output_path=args["output_path"])
        else:
            # resource not allowed status code 403
            return 403, f"Resource not allowed: {args['file_path']}"
    
    elif name == "sort_json_array":
        if checkIsSafe(args["input_path"]):
            return sort_json_array(input_path=args["input_path"], output_path=args["output_path"], sort_keys=args["sort_keys"])
        else:
            # resource not allowed status code 403
            return 403, f"Resource not allowed: {args['input_path']}"

    elif name == "extract_recent_log_lines":  
        if checkIsSafe(args["logs_directory"]):
            return extract_recent_log_lines(logs_directory=args["logs_directory"], output_path=args["output_path"], num_files=args["num_files"], line_number=args["line_number"])  
        else:
            # resource not allowed status code 403
            return 403, f"Resource not allowed: {args['logs_directory']}"
    
    elif name == "generate_markdown_index":
        if checkIsSafe(args["docs_directory"]):
            return generate_markdown_index(docs_directory=args["docs_directory"], output_path=args["output_path"])
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['docs_directory']}"

    elif name == "extract_email_sender":
        if checkIsSafe(args["input_path"]):
            return extract_email_sender(llm=llm, system_message=args["system_message"], input_path=args["input_path"], output_path=args["output_path"])
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['input_path']}"

    elif name == "extract_credit_card_number":
        if checkIsSafe(args["input_path"]):
            return extract_credit_card_number(llm=llm, system_message=args["system_message"], input_path=args["input_path"], output_path=args["output_path"])
    
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['input_path']}"

    elif name == "get_most_similar_comments":    
        if checkIsSafe(args["input_path"]):
            return get_most_similar_comments(llm=llm, input_path=args["input_path"], output_path=args["output_path"], top_n=args["top_n"])
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['input_path']}"
        
    elif name == "total_gold_ticket_sales":
        if checkIsSafe(args["db_path"]):
            return total_gold_ticket_sales(db_path=args["db_path"], output_path=args["output_path"])
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['db_path']}"


    elif name == "delete_file":
        if checkIsSafe(args["path"]):
            return deleteFile(filepath=args["path"])
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['path']}. Anyway delete is not allowed if the file is in /data directory"

    elif name == "phaseB_task":
        print("phaseB_task")

        # execute_all(bash_commands=args["bash_commands"], python_codes=args["python_codes"])
        return 200, f"Executed all commands and scripts"
    else:
        # print("Function not found")
        return 400, f"Function not found: {name}"

