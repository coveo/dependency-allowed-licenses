import os
import yaml

def sort_allow_licenses_in_file(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)

    if 'allow-licenses' in data and isinstance(data['allow-licenses'], list):
        data['allow-licenses'] = sorted(data['allow-licenses'], key=str.lower)

        with open(filepath, 'w') as f:
            yaml.dump(data, f, sort_keys=False, width=1000)

def main():
    for filename in os.listdir('.'):
        if filename.endswith('-v2.yml'):
            sort_allow_licenses_in_file(filename)

if __name__ == '__main__':
    main()
