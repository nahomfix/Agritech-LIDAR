from pathlib import Path

root_dir = Path().cwd().parent
data_dir = root_dir / "data"
files = data_dir / "raw_file_folders.txt"

with open(files, "r") as f:
    lines = f.readlines()

# remove spaces, "PRE" and trailing "/"
filenames = [
    line.replace(" ", "").replace("PRE", "").replace("/", "") for line in lines
]

# write filenames in the file
with open(data_dir / "filenames.txt", "w") as f:
    f.writelines(filenames)
