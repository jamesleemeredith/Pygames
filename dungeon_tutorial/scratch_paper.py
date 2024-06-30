from pathlib import Path
import constants as const

file_path = f"{const.IMAGE_FILEPATH}player/idle"
file_glob = file_path.glob("*.png")

for thing in file_glob:
    print(thing)