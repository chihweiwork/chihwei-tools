#!/Users/chihwei/opt/anaconda3/bin/python3
import subprocess, re, json, argparse

def get_process_info():
    ps = subprocess.Popen(['ps', '-caxmwww', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()
    return ps, vm

def iterate_processes(ps):
    processLines = ps.split('\n')
    sep = re.compile('[\s]+')
    rssTotal = 0 # kB
    for row in range(1,len(processLines)):
        rowText = processLines[row].strip()
        rowElements = sep.split(rowText)
        try:
            rss = float(rowElements[0]) * 1024
        except:
            rss = 0 # ignore...
        rssTotal += rss
    return rssTotal

def process_vm_stat(vm):
    vmLines = vm.split('\n')
    sep = re.compile(':[\s]+')
    vmStats = {}
    for row in range(1,len(vmLines)-2):
        rowText = vmLines[row].strip()
        rowElements = sep.split(rowText)
        vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096
    return vmStats

def get_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--byte', '-b', action='store_true', help='--byte, -b : show byte')
    parser.add_argument('--kilobyte', '-kb', action='store_true', help='--kilobyte, -kb : show kilobyte')
    parser.add_argument('--megabyte', '-mb', action='store_true', help='--megabyte, -mb : show megabyte')
    parser.add_argument('--gigabyte', '-gb', action='store_true', help='--gigabyte, -gb : show gigabyte')
    return parser

class ACTION:
    def __init__(self, rssTotal, vmStats, parser):
        self.rssTotal = rssTotal
        self.vmStats = vmStats
        self.parser = parser
        args = self.parser.parse_args()
        if args.byte: self.unit = "Byte"
        elif args.kilobyte: self.unit = "KB"
        elif args.megabyte: self.unit = "MB"
        elif args.gigabyte: self.unit = "GB"
        else: self.unit = "Byte"
    def transform(self, target):
        args = self.parser.parse_args()
        if args.byte: return target
        elif args.kilobyte: return target/1024
        elif args.megabyte: return target/1024/1024
        elif args.gigabyte: return target/1024/1024/1024
        else: return target
    def show_data(self):
        total_memory = self.rssTotal + self.vmStats["Pages wired down"]
        print(f'Wired Memory:\t\t {self.transform(self.vmStats["Pages wired down"]):.3f} {self.unit} \t{self.vmStats["Pages wired down"]/total_memory:.3f}%')
        print(f'Active Memory:\t\t {self.transform(self.vmStats["Pages active"]):.3f} {self.unit} \t{self.vmStats["Pages active"]/total_memory:.3f}%')
        print(f'Inactive Memory:\t {self.transform(self.vmStats["Pages inactive"]):.3f} {self.unit} \t{self.vmStats["Pages inactive"]/total_memory:.3f}%')
        print(f'Free Memory:\t\t {self.transform(self.vmStats["Pages free"]):.3f} {self.unit} \t{self.vmStats["Pages free"]/total_memory:.3f}%')
        print('=======================================================')
        print('Real Mem Total (ps):\t {0:.3f} {1}'.format(self.transform(self.rssTotal), self.unit))
        print(f'Total Memory:\t\t {self.transform(total_memory):.3f} {self.unit}')
        
'''
{
    "Pages free": 41091072,
    "Pages active": 1858080768,
    "Pages inactive": 1593843712,
    "Pages speculative": 262246400,
    "Pages throttled": 0,
    "Pages wired down": 392912896,
    "Pages purgeable": 53542912,
    "\"Translation faults\"": 48329445376,
    "Pages copy-on-write": 1832992768,
    "Pages zero filled": 32011395072,
    "Pages reactivated": 22286336,
    "Pages purged": 65994752,
    "File-backed pages": 1599852544,
    "Anonymous pages": 2114318336,
    "Pages stored in compressor": 0,
    "Pages occupied by compressor": 0,
    "Decompressions": 0,
    "Compressions": 0,
    "Pageins": 1667919872,
    "Pageouts": 0,
    "Swapins": 0
}
'''
if __name__ == "__main__":
    
    parser = get_command()

    ps, vm = get_process_info()
    rssTotal = iterate_processes(ps)
    vmStats = process_vm_stat(vm)
    try: 
        action = ACTION(rssTotal, vmStats, parser)
        action.show_data()
    except Exception as e:
        parser.print_help()
        print(e)
