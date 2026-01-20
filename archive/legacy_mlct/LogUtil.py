import sys
import os
import Config

def crash(**args):
    line = "="*100
    content = "Crash error" + "\n" + line

    for key, val in args.items():
        if key != "crash_content":
            content = content + "\n\t> " + key.upper() + "=" + str(val)
    content = content + "\n" +line

    if args["crash_content"] is not None:
        content = content + "\n"*2 + "Crash other\n" + line
        for elem in args["crash_content"]:
            content = content + "\n\t> " + elem.__str__()
        content = content + "\n\t> HERE IS ERROR" + "\n" + line

    write("last_crash.txt", content)
    sys.exit()

def write(file, content):
    if not os.path.exists(f"{os.path.dirname(Config.path_project)}\logs"):
        os.makedirs(f"{os.path.dirname(Config.path_project)}\logs")
    file = "logs/" + file.replace(":", "_")
    with open(file, "w", encoding="UTF-8") as f:
        f.write(content)