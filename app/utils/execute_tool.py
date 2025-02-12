from .a1 import format_file

def execute_tool(tool_name, arguments):
    if tool_name == "format_file":
        # return format_file(arguments)
        format_file(arguments["install_command"], arguments["execute_command"])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
    
        