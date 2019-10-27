import scraping
import os
import subprocess

MY_CHARTS = scraping.return_data(
    "https://github.com/helm/charts/tree/master/stable", 
    "js-navigation-open"
    )[1:]
WORKING_DIRECTORY = "/Users/hayley/mycode/scraping/charts/"
OUTPUT_DIRECTORY = "/Users/hayley/mycode/scraping/charts/output_files/"

def npm_start(chart_directory, output_file):
    return f"npm start -- {chart_directory} --output={output_file}"

def helm_fetch_cmd(chart):
    return f"helm fetch stable/{chart}"

def create_dir_for_chart_cmd(chart):
    return f"mkdir {chart}"

def tar_cmd(tgz):
    return f"tar xvzf {tgz}"

def helm_template_cmd():
    return f"helm template ."

def cd_in(chart):
    return f"cd {chart}"

def cd_out():
    return "cd ../"

def mv_file(tgz):
    return f"mv {tgz} ./{tgz[:-4]}"

def template():
    return f"helm template ." 

def list_items():
    os.system("ls")

def fetch_charts(charts):
    for chart in charts:
        command = helm_fetch_cmd(chart)
        print(command)
        os.system(command)

def get_tgz():
    output = subprocess.Popen( "ls", stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
    return output.split("\n")

def paths_for_snyk_helm():
    return [(WORKING_DIRECTORY + chart, 
            OUTPUT_DIRECTORY + chart + ".json",
            chart) for chart in MY_CHARTS]

def run_snyk_helm():
    paths = paths_for_snyk_helm()
    import pdb; pdb.set_trace()
    os.system("npm install")
    for each in paths:
        print(each[0], each[1])
        os.system(npm_start(each[0], each[1]))

def tar_file(tgz):
    command = tar_cmd(tgz)
    print(command)
    os.system(command)

def tar(tgzs):
    for tgz in tgzs:
        tar_file(tgz)

def template_yaml(charts):
    for chart in charts:
        cd_in(chart)
        template()
        cd_out()
