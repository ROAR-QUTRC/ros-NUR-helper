#!/usr/bin/env python3

import tomllib
import sys
import os
import shutil
import git
import tempfile
from getopt import getopt
from time import sleep
from glob import glob

rosargs = "--output-as-nix-pkg-name --fetch --no-cache --package-only --overlay"

overlay_template = ["final: prev: prev.lib.composeManyExtensions [\n", "] final prev\n"]


def parse_toml(filepath: str):
    with open(filepath, "rb") as file:
        config_file = tomllib.load(file)
    print(config_file)
    return config_file


def parse_args(args: list[str]) -> dict[str, str | list[str]]:
    parsed_args = {"configs": [], "output_dir": "", "rosdistro": "jazzy"}
    opts, _ = getopt(args, "c:o:hd:", ["help"])
    for opt, arg in opts:
        if opt == "-c":
            parsed_args["configs"].append(arg)
        elif opt == "-o":
            parsed_args["output_dir"] = arg
        elif opt == "-h" or opt == "--help":
            # TODO: IMPLEMENT HELP MESSAGE
            print("help")
        elif opt == "-d":
            parsed_args["rosdistro"] = arg
        else:
            # Shouldn't get to here
            raise ValueError("Unknown argument {arg}")
    return parsed_args


if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])

    for file in parsed_args["configs"]:
        print(file)
        repos = parse_toml(file)
        if "output_dir" in repos:
            output_dir_for_file = repos["output_dir"]
        else:
            output_dir_for_file = parsed_args["output_dir"]

        overlay = ""
        if "overlay_prefix" in repos:
            overlay += repos["overlay_prefix"]
        overlay += overlay_template[0]

        for name, details in repos.items():
            if name == "output_dir" or name == "overlay_prefix":
                continue
            output_dir = os.path.join(output_dir_for_file, name)
            shutil.rmtree(output_dir, ignore_errors=True)
            os.makedirs(output_dir, exist_ok=True)
            overlay += f"  (import ./{name}/overlay.nix)\n"

            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Cloning repo {details["url"]}")
                repo = git.Repo.clone_from(details["url"], temp_dir)
                if "branch" in details:
                    repo.git.checkout(details["branch"])
                print("Cloned")

                if "paths" not in details:
                    packages = glob(
                        os.path.join(temp_dir, "**/package.xml"), recursive=True
                    )
                    print(packages)
                else:
                    packages = [
                        os.path.join(temp_dir, path) for path in details["paths"]
                    ]
                    print(packages)

                # TODO: Fork ros2nix and get the python module natively
                #       It's a python program, but the api is not exposed
                program = f"ros2nix {rosargs} --distro {parsed_args["rosdistro"]} --output-dir={output_dir} {" ".join(packages)}"
                print(program)
                os.system(program)

        overlay += overlay_template[1]
        print(overlay)
        with open(
            os.path.join(output_dir_for_file, "overlay.nix"), "w", encoding="utf-8"
        ) as overlay_file:
            overlay_file.write(overlay)
