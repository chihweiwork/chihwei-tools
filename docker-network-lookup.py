#!/Users/chihwei/opt/anaconda3/bin/python3
import json, sys
import pdb
import pandas as pd
from tabulate import tabulate

def get_container_network_info(data):
    def _data_gen(data):
        for _, container in data[0]['Containers'].items():
            del container['EndpointID']
            yield container

    results = pd.DataFrame(_data_gen(data)).sort_values(by=['Name'], ignore_index=True)
    print(tabulate(results, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    
    data = json.load(sys.stdin)
    get_container_network_info(data)
