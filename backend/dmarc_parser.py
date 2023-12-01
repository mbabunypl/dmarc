import parsedmarc
import os
import json
from multiprocessing import Pool

def write_to_json(xml_file):
    parent = os.path.abspath('reports')
    if xml_file.endswith('.xml'):
        to_json = f"{parent}/jsonreports/{xml_file}.json"
        dmarc_report = parsedmarc.parse_report_file(f"{parent}/{xml_file}")
        with open(to_json, 'w', encoding='utf-8') as json_file:
            json.dump(dmarc_report, json_file, ensure_ascii=False, indent=4)

def parse_reports(xml_file):
    write_to_json(xml_file)

if __name__ == "__main__":
    folder_name = 'reports'
    dmarcs = os.listdir(os.path.abspath(folder_name))

    # You can adjust the number of processes based on your system's capabilities
    num_processes = 4
    with Pool(num_processes) as pool:
        pool.map(parse_reports, dmarcs)
