import scraping
import os
import subprocess

MY_CHARTS = scraping.return_data(
    "https://github.com/helm/charts/tree/master/stable", 
    "js-navigation-open"
    )[1:]

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

def mk_dirs(chart):
    command = create_dir_for_chart_cmd(chart)
    print(command)
    os.system(command)

def move_for_tar(tgz):
    command = mv_file(tgz)
    print(command)
    os.system(command)

def tar_file(tgz):
    command = tar_cmd(tgz)
    print(command)
    os.system(command)

def organize_and_tar(tgzs):
    for tgz in tgzs:
        directory_name = tgz[:-4]
        mk_dirs(directory_name)
        move_for_tar(tgz)
        os.system(cd_in(directory_name))
        tar_file(tgz)
        os.system(template())
        os.system(cd_out())
