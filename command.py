import pdb
import json
import subprocess
from tabulate import tabulate

def _print(data):

    for row in data.read().splitlines():
        print(row)

def run_cmd(cmd, show=True, debug=False):
    res = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
    res.wait(10)

    if show:
        _print(res.stdout)
        if debug:
            _print(res.stderr)
    else:
        return res

def dataframe_pretty_print(data):
    print(tabulate(data, headers='keys', tablefmt='psql'))


if __name__ == "__main__":

    run_cmd('ls -rtl')
