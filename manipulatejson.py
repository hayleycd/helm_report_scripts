import os
import json
import subprocess
import csv

MASTER_CSV = ""
SUMMARY_CSV = ""

def get_json_files():
    output = subprocess.Popen("ls", stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    return output.split("\n")

def convert_from_json(json_files):
    row_list = []
    json_files = [json_file for json_file in json_files if json_file[-4:] == "json"]
    for json_file in json_files:
        with open(json_file) as json_file:
            data = json.load(json_file)
            helm_chart = data["helmChart"]
            for each in data["images"]:
                image_name = each["imageName"]
                if each["results"].get("vulnerabilities"):
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

def convert_from_json_summary(json_files):
    row_list = []
    json_files = [json_file for json_file in json_files if json_file[-4:] == "json"]
    for json_file in json_files:
        with open(json_file) as json_file:
            data = json.load(json_file)
            helm_chart = data["helmChart"]
            for each in data["images"]:
                image_name = each["imageName"]
                dependencies = each["results"].get("dependencyCount")
                summary = each["results"].get("summary")
                unique = each["results"].get("uniqueCount")
                row_dict = {"helm_chart": helm_chart,
                        "image_name": image_name,
                        "dependencies": dependencies,
                        "summary": summary,
                        "unique": unique,
                        }
                row_list.append(row_dict)
    return row_list

        
def write_summary_csv(csv_file):
    json_files = get_json_files()
    row_list = convert_from_json_summary(json_files)
    with open(csv_file, mode='w', newline='') as helm_chart_summary:
        writer = csv.writer(helm_chart_summary, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for each in row_list:
            writer.writerow([each["helm_chart"], 
                            each["image_name"],
                            each["dependencies"],
                            each["summary"],
                            each["unique"]])

def write_master_csv(csv_file):
    json_files = get_json_files()
    row_list = convert_from_json(json_files)
    with open(csv_file, mode='w', newline='') as helm_chart_master:
        writer = csv.writer(helm_chart_master, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for each in row_list:
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
