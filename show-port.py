#!/Users/chihwei/opt/anaconda3/bin/python3/
import pdb
import subprocess
import sys
import pandas as pd
from tabulate import tabulate
from command import run_cmd
from command import dataframe_pretty_print

#Proto Recv-Q Send-Q  Local Address          Foreign Address        (state


def short_port():

    def _parser(target):
        return [x for x in target.split(' ') if x != '']

    res = run_cmd('netstat -an | grep "LISTEN"', show=False)
    if res.returncode != 0: sys.exit(2)

    columns = ['Proto', 'Recv-Q', 'Send-Q', 'Local Address', 'Foreign Address', 'state']

    data_generator = lambda targets: (dict(zip(columns, _parser(t))) for t in targets)
    output = pd.DataFrame(data_generator(res.stdout.read().splitlines()))
    dataframe_pretty_print(output)
    


if __name__ == "__main__":
    
    short_port()
