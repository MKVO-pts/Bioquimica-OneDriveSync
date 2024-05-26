"""
-Testar Linha 58/59 (Descomprimir e Checksum)

Algorithm	Speed (hours, minutes)	Number of Calculations	Total Size of Output (GB)
MD5	2 hours, 15 minutes	8 * 10^10	22 GB
SHA-256	4 hours, 30 minutes	1.6 * 10^11	44 GB
SHA-512	7 hours, 30 minutes	2.4 * 10^11	66 GB
"""
#TODO
#-Complete refresh hashmap DONE
#-Complete check newFiles DONE
#-Add more file extensions(.ZIP handling)  NOT TESTED
#-Add more hashing algorithms 
#- Bash Framework
#-Add more file sizes
import datetime, os, json, re
from dotenv import load_dotenv
import hashlib
import zipfile

#Load environment variables
load_dotenv()

OneDrive_DIR = os.environ.get('OneDrive_DIR')
NewFiles_PATH = os.environ.get('NewFiles_PATH')
Stored_PATH = os.environ.get('Stored_PATH')
Hashes_PATH = os.environ.get('Hashes_PATH')
Report_NAME = os.environ.get('Report_Name')



#Main Function
def main():
    #refresh_hashmap(OneDrive_DIR)
    check_newFiles(Stored_PATH,NewFiles_PATH,True)




def check_newFiles(Database, NewFiles, UpdateStored=False):
    report_hashmap = {'New': {}, 'Duplicated': {}}

    #Function Recursively goes through the directorys and compare with stored checksums  
    def create_new_hashmap(path, stored_hash_data):
        for entry in os.listdir(path):
            # Check if the path is a directory 
            if not os.path.isdir(path): 
                continue
            entry_path = os.path.join(path, entry)
            # If the entry is a directory, recursively call the function
            if os.path.isdir(entry_path):
                create_new_hashmap(entry_path, stored_hash_data)
                
            # If the entry is a file, update hash value
            else:
                if re.search(r'.zip',entry_path): #unzip files || Not Tested yet
                    unzip(entry_path, NewFiles)
                    create_new_hashmap(entry_path, stored_hash_data)
                
                #create hashvalue for new files
                hash_value = hashlib.md5(open(entry_path, 'rb').read()).hexdigest()
                #Duplicated            
                if hash_value in stored_hash_data['HashTable'].keys():
                    #report_hashmap['New'].append(entry = {'hash': hash_value,'New_file': entry_path ,'OneDrive_file': oldData['HashTable'][hash_value]}) #not working
                    report_hashmap['Duplicated'][entry] = {'hash': hash_value,'New_file': entry_path ,'OneDrive_file': stored_hash_data['HashTable'][hash_value]}
                    continue #skips to the next "new file"
                #New file
                else: #if there are no matches
                    report_hashmap['New'][entry] = {'hash': hash_value,'New_file': entry_path}

    
    #first updates stored hasmap, then verifys
    if UpdateStored == True:
        #refreshes stored hashmap
        refreshed_hashmap = refresh_hashmap(OneDrive_DIR,Database) 
        #Path exists and is not empty
        if os.path.exists(NewFiles) and os.listdir(NewFiles) != []:
            create_new_hashmap(NewFiles, refreshed_hashmap)
        
        #Exception handling
        else:
            print("[{}]  Pasta Vazia ou Inexistente! -> Verifica \".env\" ou se existem ficheiros\n".format(datetime.datetime.now()))
            raise BaseException.LookupError('Pasta Vazia ou Inexistente! -> Verifica \".env\" ou se existem ficheiros')
            

    #Check if the dir is correct
    if os.path.exists(NewFiles):
        #If there are new files
        if os.listdir(NewFiles) != []:
            #get stored hashes
            with open(os.path.join(Database,Hashes_PATH), 'r') as stored:
                oldData = json.load(stored)
            #iniciate recursively function
            create_new_hashmap(NewFiles, oldData) 

        #Exception handling
        elif os.listdir(NewFiles) == []:
            print("[{}]  Pasta Vazia! -> Nenhum ficheiro novo encontrado/submetido!".format(datetime.datetime.now()))
        else:
            print('[{}]  Pasta inexistente! \n Verifica se a configuração do arquivo .env esta correta.'.format(datetime.datetime.now()))
            raise ExceptionGroup.LookupError('Pasta inexistente! \n Verifica se a configuração do arquivo .env esta correta.')

    else: #Unexpected error
        print('[{}]  Erro inesperado! \n '.format(datetime.datetime.now()))
        raise Exception.ValueError('Erro inesperado! \n ')
        

    with open(os.path.join(Stored_PATH, Report_NAME), 'w') as stored:
        report_hashmap['LastUpdate'] = datetime.datetime.now()
        json.dump(report_hashmap, stored, indent=4, default=str)
    
    
    return report_hashmap


#Update Hashmap Function (database.json)
def refresh_hashmap(OneDrive,StoreHashes,name='database.json'):
    with open(os.path.join(StoreHashes,name), 'a+') as file:
        file.seek(0) #file pointer to the beginning
        datafile = json.load(file)

        #Recursively go through the directorys
        def update_file_hashmap(path):        
            for entry in os.listdir(path):
                    # Check if the path is a directory 
                if not os.path.isdir(path): 
                    break

                entry_path = os.path.join(path, entry)

                # If the entry is a directory, recursively call the function
                if os.path.isdir(entry_path):
                    update_file_hashmap(entry_path)

                # If the entry is a file, update hash value
                else:
                    hash_value = hashlib.md5(open(entry_path, 'rb').read()).hexdigest()
                    print(hash_value, entry_path)
                    datafile['HashTable'][hash_value] = str(entry_path)
                    
        update_file_hashmap(OneDrive) #Start the recursion

        #Update dictionary "HashTable" JSON file
        datafile['LastUpdate'] = datetime.datetime.now()
        file.seek(0)
        file.truncate()
        json.dump(datafile, file, indent=4, default=str) #https://stackoverflow.com/a/26195385
        print(datafile)
        return datafile



def onedrive_local_manager(onedrive,report_dir,report_name='report.json'):
    pass
















def unzip(source_filename, dest_dir = NewFiles_PATH):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)











def listdir(path):
    global counter_dir, counter_files
    counter_dir = counter_files = 0;
    for dirpath, dirnames, filenames in os.walk(path):
        print('Found directory: %s' % dirpath,filenames)
        counter_dir += 1
        print('Found files: %s' % filenames)
        for f in filenames:
           counter_files += 1
           print(os.path.join(dirpath, f))
    return counter_dir, counter_files



def DataIntegrityCheck(StoredHash,OneDrivePath):
    for dirpath, dirnames, filenames in os.walk(OneDrivePath): #dirpath=path, dirnames=directories in path, filenames=files in path
        print("DirPath",dirpath,"DirName",dirnames,"FileNames",filenames)
        for hashstored in StoredHash:
            pass
        #print("DirPath:",dirpath,"DirName:",dirnames)

#DataIntegrityCheck('C:\\Users\\tmric\\Code\\Checksum\\Stored','C:\\Users\\tmric\\OneDrive - FCT Nova\\FCT')




































#Starts Executing Script
if __name__ == "__main__":
    main()