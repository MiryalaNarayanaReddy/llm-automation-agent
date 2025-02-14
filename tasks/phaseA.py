import subprocess

def format_readme(path, prettier_package="prettier@3.4.2"):
    '''
    Formats the given file using the given prettier package.

    Args:
        path (str): The path to the file to format.
        prettier_package (str): The name of the prettier package to use like prettier@3.4.2.

    Returns:    
        int: 200 if the formatting was successful, 400 otherwise.
    '''

    print("path", path)
    print("prettier_package", prettier_package)
    
    try:
        # subprocess.run(["npx", prettier_package, "--write", path])
        # format and write the file
        subprocess.run(["npx", prettier_package, "--write", path], check=True)
        return 200
    except subprocess.CalledProcessError as e:
        print(e)
        return 400
    