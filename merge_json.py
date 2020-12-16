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

    with open('docs/selected_merged_travis.json', 'w') as f:
        json.dump(glob_data, f, indent=4)

def select_sstubs():
    project_list = ['Graylog2.graylog2-server', 'apache.flink', 'apache.storm', 'checkstyle.checkstyle', 
    'druid-io.druid', 'facebook.presto', 'google.closure-compiler', 'xetorthio.jedis']
    input_dict = []
    output_dict = []
    with open('docs/sstubs.json') as f:
        input_dict = json.load(f)
        output_dict = [d for d in input_dict if (d['projectName'] in project_list)]

    with open('docs/selected_sstubs_projects.json', 'w') as outfile:
        json.dump(output_dict, outfile, indent = 4)
    

def main():
    #merge_json()
    select_sstubs()

if __name__ == '__main__':
    main()
