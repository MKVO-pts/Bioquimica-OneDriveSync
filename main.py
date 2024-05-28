"""
TODO:
- Push to OneDrive
- Bash Framework(2 ficheiros novos)
"""
#TODO
#-Add more file extensions(.ZIP handling)  NOT TESTED
#- Bash Framework
#-Add more file sizes
import datetime, os, json, re
from dotenv import load_dotenv
import hashlib
import zipfile 
import shutil
import stat

#Load environment variables
load_dotenv()

OneDrive_DIR = os.environ.get('OneDrive_DIR')
NewFiles_PATH = os.environ.get('NewFiles_PATH')
Stored_PATH = os.environ.get('Stored_PATH')
Hashes_NAME = os.environ.get('Hashes_NAME')
Report_NAME = os.environ.get('Report_NAME')
RawStored_PATH =  os.environ.get('RawStored_PATH')



#Main Function
def main():
    time_start = datetime.datetime.now()
    logging() #Log open entry (optional)
        

    #refresh_hashmap(OneDrive_DIR) and compare new/old files
    check_newFiles(Stored_PATH,NewFiles_PATH,True)
    copytree(NewFiles_PATH,RawStored_PATH)
    logging("Finished!  RunTime: " + str(datetime.datetime.now() - time_start))




def check_newFiles(Database, NewFiles, UpdateStored=False):
    logging("Running \"check_newFiles()\"")
    report_hashmap = {'New': {}, 'Duplicated': {}}

    #Function Recursively goes through the directorys and compare with stored checksums
    #creates a report ("report.json") with the new and duplicated files
    def create_new_hashmap(path, stored_hash_data):
        for entry in os.listdir(path):
            # Check if the path is a directory (unsuseful?)
            if not os.path.isdir(path): 
                continue
            entry_path = os.path.join(path, entry) # path to subdir + filename
            # If the entry is a directory, recursively call the function
            if os.path.isdir(entry_path):
                logging(f"Recursing in {entry_path}")
                create_new_hashmap(entry_path, stored_hash_data) #recursion entry
            # If the entry is a file, update hash value
            else:
                #ZIP CODE
                if re.search(r'.zip',entry_path): #unzip files ||Kinda Tested
                    logging(f"Unzipping {entry}")
                    unzip(entry_path, NewFiles)
                    create_new_hashmap(entry_path[::-1].replace('piz.','')[::-1], stored_hash_data) #?recursion entry?
                    # Reverse, replace the first, reverse again => [::-1].replace('piz.','')[::-1]  

                hash_value = hashlib.md5(open(entry_path, 'rb').read()).hexdigest() #create hashvalue for new files
                #Duplicated/Already exists            
                if hash_value in stored_hash_data['HashTable'].keys():
                    #Uncomment for debugging
                    #logging(f"Duplicated: {entry} exists in {stored_hash_data['HashTable'][hash_value]}")
                    report_hashmap['Duplicated'][entry] = {'hash': hash_value,'New_file': entry_path ,'OneDrive_file': stored_hash_data['HashTable'][hash_value]}
                    continue #skips to the next "new file"
                #New file
                elif hash_value not in stored_hash_data['HashTable'].keys(): #if there are no matches
                    report_hashmap['New'][entry] = {'hash': hash_value,'New_file': entry_path}
                    #Uncomment for debugging
                    #logging(f'New file: {entry}')
                
                #Unknown case
                else:
                    logging(f"Unknown case in (create_new_hashmap()) with file: {entry_path}",error=True, e_type="Unknown Case")

    
    #Updates stored hasmap, before the comparison
    if UpdateStored == True: #no need to reopen the file (?)
        refreshed_hashmap = refresh_hashmap(OneDrive_DIR,Database) 
        #Path exists and is not empty
        if os.path.exists(NewFiles) and os.listdir(NewFiles) != []:
            #Creates the Report
            create_new_hashmap(NewFiles, refreshed_hashmap)

        #Folder is empty
        elif os.listdir(NewFiles) == []:
            logging(f" Empty ({NewFiles})Folder: There are no new files")
            print(f" Pasta ({NewFiles}) Vazia")
        #Folder does not exist
        elif not os.path.exists(NewFiles):
            logging(f" Folder ({NewFiles}) does not exist",e_type="NewFiles_PATH")
            print('[{}]  Pasta inexistente! \n Verifica se a configuração do arquivo .env esta correta.'.format(datetime.datetime.now()))
        #Exception handling
        else:
            logging(f" Erro desconhecido ({NewFiles})! \n  Verificar \".env\" e Ficheiros", error=True)
            print("[{}]  Pasta Vazia ou Inexistente! -> Verifica \".env\" ou se existem ficheiros\n".format(datetime.datetime.now()))
            raise BaseException.LookupError('Pasta Vazia ou Inexistente! -> Verifica \".env\" ou se existem ficheiros')
            
    
    #Compare new files with stored checksums(hashmap)
    #DEFAULT: UpdateStored = False
    elif os.path.exists(NewFiles):
        #If there are new files
        if os.listdir(NewFiles) != []:
            #get stored hashes
            with open(os.path.join(Database,Hashes_NAME), 'r') as stored:
                oldData = json.load(stored)
            #iniciate recursively function
            create_new_hashmap(NewFiles, oldData) 

        #Other cases handling
        elif os.listdir(NewFiles) == []:
            logging(f" Empty ({NewFiles})Folder: There are no new files")
            print("[{}]  Pasta Vazia! -> Nenhum ficheiro novo encontrado/submetido!".format(datetime.datetime.now()))
        elif not os.path.exists(NewFiles):
            logging(f" Folder ({NewFiles}) does not exist",e_type="NewFiles_PATH")
            print('[{}]  Pasta inexistente! \n Verifica se a configuração do arquivo .env esta correta.'.format(datetime.datetime.now()))
            raise ExceptionGroup.LookupError('Pasta inexistente! \n Verifica se a configuração do arquivo .env esta correta.')

        else: #Unexpected error
            print('[{}]  Erro inesperado! \n '.format(datetime.datetime.now()))
            logging(f" Erro desconhecido ({NewFiles})!", error=True)
            raise Exception.ValueError('Erro inesperado! \n ')
        

    with open(os.path.join(Stored_PATH, Report_NAME), 'w', encoding='utf-8') as stored:
        report_hashmap['LastUpdate'] = datetime.datetime.now()
        json.dump(report_hashmap, stored, indent=4, default=str)
    
    logging("Finishing \"check_newFiles()\"")
    logging(f'New Files: {len(report_hashmap["New"])}   Duplicated Files: {len(report_hashmap["Duplicated"])}\n')
    return report_hashmap


#Update(rewrite) Hashmap Function (database.json)
def refresh_hashmap(OneDrive,StoreHashes,name='database.json'):
    logging("Running \"refresh_hashmap()\"")
    #Open JSON file
    #open(os.path.join(StoreHashes,name), 'w').close()
    os.makedirs(StoreHashes, exist_ok=True)
    with open(os.path.join(StoreHashes,name), 'a+') as file:
        file.seek(0) #file pointer to the beginning
        #datafile = json.load(file)
        datafile = {'HashTable': {}}
        #Recursively go through the directorys
        def update_file_hashmap(path):        
            for entry in os.listdir(path):
                    # Check if the path is a directory 
                if not os.path.isdir(path): 
                    pass
                entry_path = os.path.join(path, entry)
                # If the entry is a directory, recursively call the function
                if os.path.isdir(entry_path):
                    update_file_hashmap(entry_path)
                # If the entry is a file, update hash value
                else:
                    hash_value = hashlib.md5(open(entry_path, 'rb').read()).hexdigest()
                    datafile['HashTable'][hash_value] = str(entry_path)
                    
        update_file_hashmap(OneDrive) #Start the recursion

        #Update dictionary "HashTable" JSON file
        
        datafile['LastUpdate'] = datetime.datetime.now()
        file.seek(0)
        file.truncate()
        logging(f"Overwriting \"{name}\"")
        json.dump(datafile, file, indent=4, default=str) #https://stackoverflow.com/a/26195385
        #print(datafile)
        return datafile


def unzip(source_filename, dest_dir = NewFiles_PATH):
    logging(f"Extracting files from {source_filename} to {dest_dir}")
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)


"""Como saber para aonde mover os ficheiros na Drive?
def push_to_onedrive():
    logging("Running \"push_to_onedrive()\"")
    #Push to OneDrive
    with open(os.path.join(Stored_PATH, Report_NAME)) as report:
        #report = json.load(report)
        for entry in json.load(report)['New'].values():
            copytree(entry['New_file'],entry ????? )
            print(entry)"""        

def splited_backup():
    logging("Running \"raw_backup()\"")
    #Push to OneDrive
    with open(os.path.join(Stored_PATH, Report_NAME)) as report:
        #report = json.load(report)
        for entry in json.load(report)['New'].values():
            copytree(entry['New_file'],os.path.join(RawStored_PATH,"NewSubmited"))
        for entry in json.load(report)['Duplicated'].values():
            copytree(entry['New_file'],os.path.join(RawStored_PATH,"DuplicatedSubmited"))         



def full_backup(dest_dir=Stored_PATH, src_dir=OneDrive_DIR):
    logging(f"Running \"full_backup()\" \n From {src_dir} to {dest_dir}")
    copytree(src_dir, dest_dir)
    logging("Full Backup Finished")


##Logging Code Execution
def logging(text="", error=False, e_type="Unknown"):
    #write to log file
    with open('logfile.txt', 'a', encoding='utf-8') as log_file: #
        #Error Logging
        if error: 
            log_file.write(f"[{timestamp()}]    Error: ({e_type})\n  File: {__file__}\n  Information: {text}\n  time:{timestamp()}\n")
            #Error File Isolation
            with open('ERROR.txt', 'a') as error_file:
                error_file.write(f"\n[{timestamp()}]    Error: ({e_type})\n  File: {__file__}\n  Information: {text}\n  time:{timestamp()}\n\n")
        #Start New Log entry
        elif text == "": #(Optional)
            log_file.write(f'\nRunning {__file__} [{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]\n')
        #Normal Log entry
        else: 
            log_file.write(f"[{timestamp()}]    {text}\n")

#Get Current Time (Only Use for Logs(?))
def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")


#Copy entire folder Function
#https://stackoverflow.com/a/22331852
def copytree(src, dst, symlinks = False, ignore = None):
      logging(f"Copying files From {src} to {dst}")
      if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
      lst = os.listdir(src)
      if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
      for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
          if os.path.lexists(d):
            os.remove(d)
          os.symlink(os.readlink(s), d)
          try:
            st = os.lstat(s)
            mode = stat.S_IMODE(st.st_mode)
            os.lchmod(d, mode)
          except:
            pass # lchmod not available
        elif os.path.isdir(s):
          copytree(s, d, symlinks, ignore)
        else:
          shutil.copy2(s, d)



#Starts Executing Script
if __name__ == "__main__":
    #create folders if it does not exist
    for directory_path in [NewFiles_PATH,Stored_PATH,RawStored_PATH,OneDrive_DIR]:
        if not os.path.exists(directory_path):
            try:
                original_umask = os.umask(0)
                os.makedirs(directory_path, 0o0777)
                os.umask(original_umask)
            finally:
                os.umask(original_umask)
    main()