import os   # Used to interact with the operating system, such as working with file paths and directories.
import json # Used to create and write a JSON metadata file. O QUE É JSON METADATA FILE?
import shutil   # Used to copy and delete directories and files.
from subprocess import PIPE, run    # Used to execute system commands (in this case, compiling Go code).
import sys  # Used to get command-line arguments.

GAME_DIR_PATTERN = "game"   # This variable will help the code find all folders with "game" in the name
GAME_CODE_EXTENSION = ".go" # Specifies that Go source files have a ".go" extension
GAME_COMPILE_COMMAND = ["go", "build"]  # The command used to compile Go code

def find_all_game_paths(source):    # find_all_game_paths(cwd + "data") -> Find directories that has "game" in the name
    game_paths = []

    for root, dirs, files in os.walk(source):   # os.walk() is used to generate the file names in a directory tree
                                                # by walking either top-down or bottom-up through the directory structure.
                                                # in this case: root = source = C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data
                                                # dirs = hello_world_game; rock_paper_scissors_game and simon_says_game
                                                # files = main.go; code.go and file.go
        for directory in dirs:  # running through all directories
            if GAME_DIR_PATTERN in directory.lower():   # only looking for directories with "game" in the name, a file with "game" won't be found
                path = os.path.join(source, directory)  # source+directory. Always use .join (respect the programming path format)
                game_paths.append(path) # append all the paths with game in the name

        break   # Only look at the first level (top-level) of directories.
                # If there was no break, the os.walk() function would have a 2nd iteration:
                # root = C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data\hello_world_game
                # dirs = [] -> no subdirectories inside hello_world_game
                # files = main.go
                # The 3rd iteration would be: root = C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data\rock_paper_scissors_game
                # and so on...

    return game_paths   # [C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data\hello_world_game ;...\rock_paper_scissors_game; ...\simon_says_game]


def get_name_from_paths(paths, to_strip):   # Removes "game" from directory names for better readability. We don't want _game in the new folder names inside target.
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)   # os.path.split -> splits a file path into two parts: Head (the directory path leading up to the file/folder)
                                            # and Tail (the last component of the path, which is usually the file or directory name)
                                            # In this case, the dir_name = Tail = hello_world_game; rock_paper_scissors_game and simson_says_game
        new_dir_name = dir_name.replace(to_strip, "") #Replace "game" with ""
        new_names.append(new_dir_name)  #Append the new names to the list

    return new_names    # # [hello_world ;rock_paper_scissors; simon_says]


def create_dir(path):   # create a new directory(folder) called "target" if it doesn't exists
    if not os.path.exists(path):
        os.mkdir(path)  # os.mkdir -> create the "target" folder


def copy_and_overwrite(source, dest):   # copy/overwrite the contents of src to the new directory:
                                        # C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data\hello_world_game ->
                                        # C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target\hello_world_
    if os.path.exists(dest):    # check if the path exists
        shutil.rmtree(dest)     # .rmtree -> delete an existing directory and all of its contents, including subdirectories and files.
    shutil.copytree(source, dest)   # copy the entire contents of the source directory into the dest directory.


def make_json_metadata_file(path, game_dirs):   # (C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target\metadata.json,
                                                # C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target)
    data = {                                    # data is a dictionary {}
        "gameNames": game_dirs,                 # store all the directories names to gameNames
        "numberOfGames": len(game_dirs)         # store the quantity of directories
    }
    with open(path, "w") as f:  # Opens the file at the given path for writing ("w" = writing mode).
        json.dump(data, f)      # Converts the data dictionary into JSON format and writes it to the file.


def compile_game_code(path):
    code_file_name = None   # When we use None, ware saying that the variable doesn't have any content or value yet, and you are waiting for it to be assigned one.
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):  # a different way to find for files that ends with a specific text.
                                                    # but in this case we want to find only the file that ends with the text,
                                                    # in the other case, the text could be located in another position
                code_file_name = file   # gives the name of the .go file to the variable code_file_name
                break   # if the if statement is True, it gets out

            #else:              # cannot add line 79 and 80, otherwise the function would exist as soon as it find a file without the .go extension
                #return None

        break   #Just run the for loop one time (top-level)

    if code_file_name is None:
        return

    command = GAME_COMPILE_COMMAND + [code_file_name]   # command = ["go", "build", "main.go"]
    run_command(command, path)  # run_command(["go", "build", "main.go"], dest_path = C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target\hello_world_)

def run_command(command, path):
    cwd = os.getcwd()   #cwd: currently working directory ...\Python Scripting, so we can return to it later
    os.chdir(path)  #change directory to dest_path (where the .go files are)

    result = run(command, stdout = PIPE, stdin = PIPE, universal_newlines = True)   # from subprocess library. stdout -> standard location where the command is giving the output.
                                                                                    # stdin -> standard location where the command is accepting the output.
                                                                                    # PIPE is the bridge that connects the Python code with the process
                                                                                    # that we're using to run the command
                                                                                    # go build "file_name" is a SYSTEM COMMAND to compile a file.
    print("compile result", result)
    os.chdir(cwd)


def main(source, target):   # main ("data", "target")
    cwd = os.getcwd()   #cwd: currently working directory ...\Python Scripting
    source_path = os.path.join(cwd, source) # always use join() function to create path -> source_path = cwd + "data"
    target_path = os.path.join(cwd, target) # target_path = cwd + "target"

    game_paths = find_all_game_paths(source_path)   # find all cwd + directories (cwd + folders) with "game" in the name
    new_game_dirs = get_name_from_paths(game_paths, "game") # If there's a directory (folder) with "game" in the name, it will store the same name, but without the "game"

    create_dir(target_path) # create a new folder in the cwd, named "target"

    for src, dest in zip(game_paths, new_game_dirs):    # zip function: Combine 2 or more lists --> [1, 2, 3] ["a", "b", "c"] --> [(1, "a"), (2, "b"), (3, "c")]
                                                        # in this case: [(C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data\hello_world_game, hello_world), ...]
                                                        # src = C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\data\hello_world_game
                                                        # dest = hello_world_
        dest_path = os.path.join(target_path, dest)     # dest_path = C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target + hello_world_
        copy_and_overwrite(src,dest_path) # copy/overwrite the contents of src to the new directory
        compile_game_code(dest_path)    # Identifies and compiles the Go source files in each game directory.

    json_path = os.path.join(target_path, "metadata.json")  # create a new path (not directory) and in consequence,
                                                            # create a blank .json file with the name: "metadata" in "target" directory
    make_json_metadata_file(json_path, new_game_dirs)       # make_json_metadata_file(C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target\metadata.json,
                                                            # C:\Users\lucas\PycharmProjects\TechWithTim - Python Scripting\target)


if __name__ == "__main__":  # The script only works if it's ran directly. If it's imported into another script, this block doesn't work
    args = sys.argv # sys.argv is a list that contains the command-line arguments passed when running the script.
                    # The first element (sys.argv[0]) is always the script filename ["Python_Scripting", "data", "target"]
    # print(args) #print the passed arguments when we call the function
    if len(args) != 3:  # Exactly 3 arguments: Script Name; Source Directory; Target Directory
        raise Exception("You must pass a source and target directory - only")   # To run: python Scripting.py data new_data in terminal, I need those 3 arguments:
                                                                                # file name: Python_Scripting.py; source: data; target directory: new_data
    source, target = args[1:]   # source = "data", target = "target"
    main(source, target)