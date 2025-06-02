import os

from ruamel.yaml import YAML


def sort_allow_licenses_in_file(filepath):
    yaml = YAML()
    yaml.preserve_quotes = True
    with open(filepath, "r") as f:
        data = yaml.load(f)

    if "allow-licenses" in data and isinstance(data["allow-licenses"], list):
        data["allow-licenses"] = sorted(data["allow-licenses"], key=str.lower)

        with open(filepath, "w") as f:
            yaml.dump(data, f)


def main():
    for filename in os.listdir("."):
        if filename.endswith("-v2.yml"):
            sort_allow_licenses_in_file(filename)


if __name__ == "__main__":
    main()
