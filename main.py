from PIL import Image
from pathlib import Path
from os import walk
from os import mkdir
import re

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def convert_file(path: Path, to: Path | str = "near"):
    print(f"Converting {path}")
    im = Image.open(path)
    rgb_im = im.convert('RGB')
    filename = path.name
    filename = filename.split('.png')[0]+'.jpg'
    if to == "near":
        rgb_im.save(path.parent.joinpath(filename))
    elif to == "return":
        return rgb_im
    elif to.__module__ == 'pathlib':
        rgb_im.save(Path(to, filename))


def get_dir_subdir_pngs(path: Path):
    files = []

    filenames = next(walk(path), (None, None, []))[2]
    for filename in filenames:
        if filename.endswith('.png'):
            files.append(path.joinpath(filename))

    dirnames = next(walk(path), (None, [], None))[1]
    for dirname in dirnames:
        ffiles = get_dir_subdir_pngs(path.joinpath(dirname))

        files = files + ffiles

    return files


print("What do you want to do")
print("[1] Convert single file")
print("[2] Convert files from directory")
print("[3] Convert files from directory and subdirectories")

match input():
    case "1":
        print("Enter path to file: ")
        path = Path(input())
        print(f"Absolute path to file is {path.absolute()}")
        q = input("Is it right [Y/n] ")
        if q == "Y" or q == "y" or q == "":
            convert_file(path)
    case "2":
        print("Enter path to directory: ")
        path = Path(input())
        print(f"Absolute path to directory is {path.absolute()}")
        q = input("Is it right [Y/n] ")
        if q == "Y" or q == "y" or q == "":
            if path.exists() and path.is_dir():
                filenames = next(walk(path), (None, None, []))[2]
                for filename in filenames:
                    if filename.endswith('.png'):
                        convert_file(path.joinpath(filename))
            else:
                print("Directory is not exist")

    case "3":
        print("Enter path to directory: ")
        path = Path(input())
        print("Choose save mode")
        print("[1] Near old element")
        print("[2] In specified destination dir with save subdirs tree")
        q1 = input("Please select a number [default=1] ")
        match q1:
            case "1":
                pass
            case "2":
                print("Enter path:")
                spath = input()
                print(f"All images will save in {spath} directory")

        print(f"Absolute path to directory with images is {path.absolute()}")
        q = input("Is it right? [Y/n] ")
        if q == "Y" or q == "y" or q == "":
            if path.exists() and path.is_dir():
                print(f"Processing files and dir and subdirs")
                files = get_dir_subdir_pngs(path)
                print(f"Found {files.__len__()} files")
                for fpath in files:
                    if q1 == "2":
                        img = convert_file(fpath, "return")

                        rpattern = "[\\\\,/]"  # Linux support

                        lpath = re.split(rpattern, fpath.absolute().__str__().split(
                            path.absolute().__str__())[1])

                        old_filename = lpath[-1]
                        filename = old_filename.replace(".png", ".jpg")

                        lpath = "/".join(lpath[0:lpath.__len__()-1])

                        dpath = Path(spath+lpath, filename)

                        sls = re.split(rpattern, lpath)
                        for i in range(sls.__len__()):

                            sl = "/".join(sls[0:i+1])

                            slpath = Path(spath+sl)

                            if not slpath.exists():
                                mkdir(slpath)

                        img.save(dpath)
                    else:
                        convert_file(fpath)
            else:
                print("Directory is not exist")
    case _:
        print("Incorrect number")
