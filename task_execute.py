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
# from tasks.phaseB import compress_image
from tasks.phaseB import scrape_website
from tasks.phaseB import transcribe_audio
from utils.execute_tool import execute_all
import json

def execute_task(name, args, llm=None, llm_for_phaseB=None):
     
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
            return extract_credit_card_number(llm=llm, system_prompt=args["system_prompt"], user_prompt=args["user_prompt"], input_path=args["input_path"], output_path=args["output_path"])
    
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
        
    # elif name == "compress_image":
    #     if checkIsSafe(args["input_path"]) and checkIsSafe(args["output_path"]):
    #         return compress_image(input_path=args["input_path"], output_path=args["output_path"])
    #     else:
    #         # resource not allowed status code 403            
    #         return 403, f"Resource not allowed: {args['input_path']} or {args['output_path']}"

    elif name == "scrape_website":
        if checkIsSafe(args["url"]) :
            return scrape_website(llm=llm, url=args["url"], system_prompt=args["system_prompt"], output_path=args["output_path"])
        else:
            # resource not allowed status code 403      
            return 403, f"Resource not allowed: {args['url']}"
        
    elif name == "transcribe_audio":
        if checkIsSafe(args["input_path"]):
            return transcribe_audio(llm=llm, input_path=args["input_path"], output_path=args["output_path"])
        else:
            # resource not allowed status code 403            
            return 403, f"Resource not allowed: {args['input_path']}"   
    
    elif name == "phaseB_task":
        print("phaseB_task")

         # result = execute_task(task)
        result = llm_for_phaseB.parseTask(args["task"])
        print(result)
        function_call = result["choices"][0]["message"]["function_call"]

        print(function_call)

        if function_call:
            function_name = function_call["name"]
            if function_name == "execute_code_task":
                arguments = json.loads(function_call["arguments"])  
                # print(arguments)
                status_code, details = execute_all(llm_for_phaseB,arguments['commands'])

                return status_code, details
                
            else:
                return 400, f"Function not found: {function_name}"
        else:
            return 400, f"Function call not found"
    
    else:
        # print("Function not found")
        return 400, f"Function not found: {name}"

