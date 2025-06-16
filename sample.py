from pathlib import Path

D = Path("/home/rajasjc/")

files = [ i for i in D.iterdir() if i.is_file()]

print(*files)


try:
    a = int(input("Enter your number:"))
    b = int(input("Enter your number:"))
    c = int(input("Enter your number:"))
except ValueError:
    print("the given value is not number")
    exit(1)

print(f'a:{a} b:{b} c:{c}')

from pathlib import Path
[*Path('/root').rglob('**/*.md')]


from itertools import count

days = ['Sun','Mon','Tues','Wed','Thu','Fri','Sat']

for i,j in zip(count(1),days):
    print(i,j)

S = input("Enter the String:")
L = len(S)
print(*S,sep='|')
print('=' *(L*2-1))
print(*range(L))

lang="Python"
print("="* 21)
print(*range(len(lang)), sep=' | ')
print("-"* 21)
print(*lang, sep=' | ')
print("-"* 21)
print(*range(-len(lang),0,1), sep='| ')
print("="* 21)

methods = [ i for i in dir(str) if i[0].islower()]
w = str(len(max(methods, key = len)) +2)

fmt = ('{:'+w+'s}')*4


for fn in zip(*[iter(methods + [' '] ) ] * 4):
    print(fmt.format(*fn))

list1 = [1,2,3,4,5]
list2 = ['a','b','c','d','e']

for i, j in zip(list1,list2):
    print(i,"==>",j)

import matplotlib.pyplot as p 
s = [ 40,30,10,10,10]
l = ["Python", "Java", "C++", "C", "JavaScript"]
p.pie(s,labels = l)
p.show()

from os import statvfs as svfs
from re import compile, search
from bisect import bisect
from pathlib import Path

class DiskUsage:
    def __init__(self, file):
        self.IO_Block = svfs(file).f_bsize
        self.f_blocks = svfs(file).f_blocks
        self.f_bfree = svfs(file).f_bfree

    def convert(self, bytes):
        size = [1, 2**10, 2**20, 2**30, 2**40]
        unit = ['B', 'K', 'M', 'G', 'T']
        index = bisect(size, bytes) - 1
        return f"{bytes / size[index]:.0f}{unit[index]}"

    def size(self):
        return self.convert(self.f_blocks * self.IO_Block)

    def free(self):
        return self.convert(self.f_bfree * self.IO_Block)

    def used(self):
        used = self.f_blocks - self.f_bfree
        return self.convert(used * self.IO_Block)

    def usep(self):
        if self.f_blocks == 0:  # Check for division by zero
            return "0.00%"  # Return 0% usage if total blocks are zero
        return f"{(self.f_blocks - self.f_bfree) / self.f_blocks:.2%}"


if __name__ == '__main__':
    comp = compile(r'^/dev/(?!.*(snap|boot|fuse))')
    mline = Path('/proc/mounts').read_text().splitlines()
    fs = [i.split()[:2] for i in mline if comp.search(i)]

    print(f'{"Filesystem":<15} {"Size":>10} {"Used":>10} {"Avail":>10} {"Used%":>7}  {"Mounted on"}')
    print('=' * 60)

    for x in fs:
        disk = DiskUsage(x[1])
        print(f'{x[0]:<15} {disk.size():>10} {disk.used():>10} {disk.free():>10} {disk.usep():>7}  {x[1]}')

# Custom Table

import logging
from os import statvfs as svfs
from re import compile
from bisect import bisect
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.ERROR,  # Log only errors and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='disk_usage.log',  # Log to a file
    filemode='a'  # Append to the log file
)

class DiskUsage:
    def __init__(self, file):
        try:
            stats = svfs(file)
            self.IO_Block = stats.f_bsize
            self.f_blocks = stats.f_blocks
            self.f_bfree = stats.f_bfree
        except FileNotFoundError:
            logging.error(f"File or path '{file}' not found.")
            raise ValueError(f"File or path '{file}' not found.")
        except PermissionError:
            logging.error(f"Permission denied for accessing '{file}'.")
            raise ValueError(f"Permission denied for accessing '{file}'.")
        except Exception as e:
            logging.exception(f"An unexpected error occurred while accessing '{file}': {e}")
            raise ValueError(f"An error occurred while accessing '{file}': {e}")

    def convert(self, bytes):
        try:
            size = [1, 2**10, 2**20, 2**30, 2**40]
            unit = ['B', 'K', 'M', 'G', 'T']
            index = bisect(size, bytes) - 1
            return f"{bytes / size[index]:.0f} {unit[index]}"
        except Exception as e:
            logging.exception(f"Error converting size: {e}")
            return "Error"

    def size(self):
        try:
            return self.convert(self.f_blocks * self.IO_Block)
        except Exception as e:
            logging.exception(f"Error calculating size: {e}")
            return "Error"

    def free(self):
        try:
            return self.convert(self.f_bfree * self.IO_Block)
        except Exception as e:
            logging.exception(f"Error calculating free space: {e}")
            return "Error"

    def used(self):
        try:
            used = self.f_blocks - self.f_bfree
            return self.convert(used * self.IO_Block)
        except Exception as e:
            logging.exception(f"Error calculating used space: {e}")
            return "Error"

    def usep(self):
        try:
            if self.f_blocks == 0:  # Avoid division by zero
                return "0.00%"
            return f"{(self.f_blocks - self.f_bfree) / self.f_blocks:.2%}"
        except Exception as e:
            logging.exception(f"Error calculating usage percentage: {e}")
            return "Error"

def main():
    try:
        # Compile a regex to filter out unwanted filesystems
        comp = compile(r'^/dev/(?!.*(snap|boot|fuse))')
        # Read mounted filesystems from /proc/mounts
        mline = Path('/proc/mounts').read_text().splitlines()
        fs = [i.split()[:2] for i in mline if comp.search(i)]

        # Print header
        print(f'{"Filesystem":<15} {"Size":>10} {"Used":>10} {"Avail":>10} {"Used%":>7}  {"Mounted on"}')
        print('=' * 60)

        # Iterate through filesystems and display disk usage
        for x in fs:
            try:
                disk = DiskUsage(x[1])
                print(f'{x[0]:<15} {disk.size():>10} {disk.used():>10} {disk.free():>10} {disk.usep():>7}  {x[1]}')
            except ValueError as e:
                logging.error(f"Error processing {x[1]}: {e}")
                print(f"{x[0]:<15} {'Error':>10} {'Error':>10} {'Error':>10} {'Error':>7}  {x[1]}")
    except FileNotFoundError:
        logging.error("The file '/proc/mounts' was not found.")
        print("Error: The file '/proc/mounts' was not found.")
    except PermissionError:
        logging.error("Permission denied while accessing '/proc/mounts'.")
        print("Error: Permission denied while accessing '/proc/mounts'.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()


# Using Pretty Table

import logging
from os import statvfs as svfs
from re import compile
from bisect import bisect
from pathlib import Path
from prettytable import PrettyTable  # Import PrettyTable

# Configure logging
logging.basicConfig(
    level=logging.ERROR,  # Log only errors and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='disk_usage.log',  # Log to a file
    filemode='a'  # Append to the log file
)

class DiskUsage:
    def __init__(self, file):
        try:
            stats = svfs(file)
            self.IO_Block = stats.f_bsize
            self.f_blocks = stats.f_blocks
            self.f_bfree = stats.f_bfree
        except FileNotFoundError:
            logging.error(f"File or path '{file}' not found.")
            raise ValueError(f"File or path '{file}' not found.")
        except PermissionError:
            logging.error(f"Permission denied for accessing '{file}'.")
            raise ValueError(f"Permission denied for accessing '{file}'.")
        except Exception as e:
            logging.exception(f"An unexpected error occurred while accessing '{file}': {e}")
            raise ValueError(f"An error occurred while accessing '{file}': {e}")

    def convert(self, bytes):
        try:
            size = [1, 2**10, 2**20, 2**30, 2**40]
            unit = ['B', 'K', 'M', 'G', 'T']
            index = bisect(size, bytes) - 1
            return f"{bytes / size[index]:.0f}{unit[index]}"
        except Exception as e:
            logging.exception(f"Error converting size: {e}")
            return "Error"

    def size(self):
        try:
            return self.convert(self.f_blocks * self.IO_Block)
        except Exception as e:
            logging.exception(f"Error calculating size: {e}")
            return "Error"

    def free(self):
        try:
            return self.convert(self.f_bfree * self.IO_Block)
        except Exception as e:
            logging.exception(f"Error calculating free space: {e}")
            return "Error"

    def used(self):
        try:
            used = self.f_blocks - self.f_bfree
            return self.convert(used * self.IO_Block)
        except Exception as e:
            logging.exception(f"Error calculating used space: {e}")
            return "Error"

    def usep(self):
        try:
            if self.f_blocks == 0:  # Avoid division by zero
                return "0.00%"
            return f"{(self.f_blocks - self.f_bfree) / self.f_blocks:.0%}"
        except Exception as e:
            logging.exception(f"Error calculating usage percentage: {e}")
            return "Error"

def main():
    try:
        # Compile a regex to filter out unwanted filesystems
        comp = compile(r'^/dev/(?!.*(snap|boot|fuse))')
        # Read mounted filesystems from /proc/mounts
        mline = Path('/proc/mounts').read_text().splitlines()
        fs = [i.split()[:2] for i in mline if comp.search(i)]

        # Create a PrettyTable instance
        table = PrettyTable()
        table.field_names = ["Filesystem", "Size", "Used", "Avail", "Used%", "Mounted on"]

        # Iterate through filesystems and display disk usage
        for x in fs:
            try:
                disk = DiskUsage(x[1])
                table.add_row([x[0], disk.size(), disk.used(), disk.free(), disk.usep(), x[1]])
            except ValueError as e:
                logging.error(f"Error processing {x[1]}: {e}")
                table.add_row([x[0], "Error", "Error", "Error", "Error", x[1]])

        # Print the table
        print(table)
    except FileNotFoundError:
        logging.error("The file '/proc/mounts' was not found.")
        print("Error: The file '/proc/mounts' was not found.")
    except PermissionError:
        logging.error("Permission denied while accessing '/proc/mounts'.")
        print("Error: Permission denied while accessing '/proc/mounts'.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()


