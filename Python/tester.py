import datetime, os, json, re
from dotenv import load_dotenv
import hashlib
import zipfile 
import shutil
import stat

#Load environment variables
load_dotenv()
#for x in [OneDrive_DIR,NewFiles_PATH,Stored_PATH,Hashes_NAME,Report_NAME,RawStored_PATH]: print(x)
def format_bytes(size):
    power = 2**10 # 2**10 = 1024
    n = 0
    power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return "{:.1f} {}".format(size, power_labels[n])
def timer(path,Function,repetitions=1):
    #print(f"Running {Function}() {repetitions} times")
    start = datetime.datetime.now()
    for x in range(repetitions):
        Function(path)
        #print(f"{x} : {datetime.datetime.now() - start}")
    print(f"{Function}:     Total: {(datetime.datetime.now() - start)}   Average: {(datetime.datetime.now() - start)/repetitions}")

path = r'C:\\Users\\tmric\\Documents\\OneDrive'

t_file = 0 ; t_dir = 0 ; size = 0
for root, dir, file in os.walk(path,topdown=True, onerror=print(""), followlinks=False):
    for x in file:
        size += os.path.getsize(os.path.join(root,x))
    t_file += len(file)
    t_dir += len(dir)
t_size = format_bytes(size)
print(f'Ficheiros: {t_file}   Pastas:{t_dir}   Espaco: {t_size}')



def faster_md5(path): #489 MB/s
    datafile = {'HashTable': {}}; t_files = 0 ; t_dirs = 0 ; sizes = 0; counter = 0
    for roots, dirs, files in os.walk(path,topdown=True, onerror=print(), followlinks=False):
        for file in files:
            hash_value = hashlib.md5(open(os.path.join(roots,file), 'rb').read()).hexdigest()
            datafile['HashTable'][hash_value] = str(os.path.join(roots,file))
        t_files += len(files)
        t_dirs += len(dirs)
    #t_sizes = format_bytes(sizes)
def faster_sha1(path): # 940 MB/s
    datafile = {'HashTable': {}}; t_files = 0 ; t_dirs = 0 ; sizes = 0; counter = 0
    for roots, dirs, files in os.walk(path,topdown=True, onerror=print(), followlinks=False):
        for file in files:
            hash_value = hashlib.sha1(open(os.path.join(roots,file), 'rb').read()).hexdigest()
            datafile['HashTable'][hash_value] = str(os.path.join(roots,file))
        t_files += len(files)
        t_dirs += len(dirs)
def faster_sha256(path): #924 MB/s
    datafile = {'HashTable': {}}; t_file = 0 ; t_dir = 0 ; size = 0; counter = 0
    for roots, dirs, files in os.walk(path,topdown=True, onerror=print(), followlinks=False):
        for file in files:
            hash_value = hashlib.sha256(open(os.path.join(roots,file), 'rb').read()).hexdigest()
            datafile['HashTable'][hash_value] = str(os.path.join(roots,file))
        t_file += len(files)
        t_dir += len(dirs)
    t_size = format_bytes(size)
    print(len(datafile['HashTable']))
def faster_sha512(path): #509 MB/s
    datafile = {'HashTable': {}}; t_files = 0 ; t_dirs = 0 ; sizes = 0; counter = 0
    for roots, dirs, files in os.walk(path,topdown=True, onerror=print(), followlinks=False):
        for file in files:
            hash_value = hashlib.sha512(open(os.path.join(roots,file), 'rb').read()).hexdigest()
            datafile['HashTable'][hash_value] = str(os.path.join(roots,file))
        t_files += len(files)
        t_dirs += len(dirs)
    


        

#timer(r'C:\Users\tmric\Documents\OneDrive\3º ano\Outros\3º Ano\2º Semestre',faster_md5,1)
#timer(r'C:\Users\tmric\Documents\OneDrive',faster_sha1,1)
timer(r'C:\\Users\\tmric\\Documents\\OneDrive',faster_sha256,1)
#timer(r'C:\Users\tmric\Documents\OneDrive',faster_sha512,10)
#timer(r'C:\Users\tmric\Documents\OneDrive',faster_blake2b,3)



"""
OneDrive_DIR = os.environ.get('OneDrive_DIR')
NewFiles_PATH = os.environ.get('NewFiles_PATH')
Stored_PATH = os.environ.get('Stored_PATH')
Hashes_NAME = os.environ.get('Hashes_NAME')
Report_NAME = os.environ.get('Report_NAME')
RawStored_PATH =  os.environ.get('RawStored_PATH')"""
"""
start = datetime.datetime.now()
def main(caminho):
    continues = 0 
    outcounter = 0
    def create_new_hashmap(path):
        global continues
        global hashvalue
        global outcounter
        hashvalue = []
        for entry in os.listdir(path):
            # Check if the path is a directory (unsuseful?)
            if not os.path.isdir(path): 
                #continues =+ 1
                continue
            entry_path = os.path.join(path, entry) # path to subdir + filename
            # If the entry is a directory, recursively call the function
            if os.path.isdir(entry_path):
               create_new_hashmap(entry_path) #recursion entry
            # If the entry is a file, update hash value
            else:
                #outcounter += + 1
                hashvaluev2.append(hashlib.md5(open(entry_path, 'rb').read()).hexdigest())
                hash_value += hashlib.md5(open(entry_path, 'rb').read()).hexdigest() #create hashvalue for new files
    create_new_hashmap(caminho)
main(path)
print("Skips:",continues)
"""
"""
def files_tree(path):
    TotalFiles = os.walk(path,topdown=True, onerror=print(), followlinks=False)
    t_files = 0 ; t_dirs = 0 ; size = 0
    for root, dirs, files in TotalFiles:
        for x in files:
            size += os.path.getsize(os.path.join(root,x))
        t_files += len(files)
        t_dirs += len(dirs)
    t_size = format_bytes(size)
    print(t_files,t_dirs, t_size)
#files_tree(r'C:\\')*5
print(f'Runtime: {(datetime.datetime.now() - start)}')"""
"""
pythonFiles = [file for dirs in os.walk('.', topdown=True)
                   for file in dirs[2] if file.endswith(".py")]
print('python files in the directory tree are ')
for r in pythonFiles:
    print(r)
def timer(path,Function,repetitions=1):
    start = datetime.datetime.now()
    for x in range(repetitions):
        Function(path)
    print(f"Runtime: {(datetime.datetime.now() - start)}")
def printt(path):
    print(path)
timer(path,printt)"""