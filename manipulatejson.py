import os
import json
import subprocess
import csv

MASTER_CSV = ""
SUMMARY_CSV = ""

def get_json_files():
    output = subprocess.Popen("ls", stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    return output.split("\n")

def convert_from_json(json_file, csv_file):
    with open(json_file) as json_file:
        row_list = []
        data = json.load(json_file)
        helm_chart = data["helmChart"]
        for each in data["images"]:
            image_name = each["imageName"]
            for vuln in each["results"]["vulnerabilities"]:
                row_dict = {"helm_chart": helm_chart,
                            "image_name": image_name,}
                row_dict['identify'] = vuln['id']
                row_dict['vulnerability_title'] = vuln['title']            
                row_dict['severity_level'] = vuln['severity']
                row_dict['severity_score'] = vuln['cvssScore']
                row_dict['package_manager'] = vuln['packageManager']
                row_dict['package_name'] = vuln['packageName']
                row_dict['upgradable'] = vuln['isUpgradable']
                row_dict['patchable'] = vuln['isPatchable']
                row_list.append(row_dict)
    return row_list
        
def write_master_row(row_list, csv_file):
    with open(csv_file, mode='a', newline='') as helm_chart_master:
        for each in row_list:
            writer = csv.writer(helm_chart_master, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([each["helm_chart"], 
                            each["image_name"], 
                            each["identify"],
                            each["vulnerability_title"], 
                            each["severity_level"], 
                            each["severity_score"], 
                            each["package_manager"], 
                            each["package_name"], 
                            each["upgradable"], 
                            each["patchable"]])