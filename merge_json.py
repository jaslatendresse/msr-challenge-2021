import json
import glob

def merge_json():
    glob_data = []
    for file in glob.glob('docs/travistorrent/*.json'):
        with open(file) as json_file:
            data = json.load(json_file)
            i = 0
            while i < len(data):
                glob_data.append(data[i])
                i += 1

    with open('docs/merged_travis.json', 'w') as f:
        json.dump(glob_data, f, indent=4)

def main():
    merge_json()

if __name__ == '__main__':
    main()
