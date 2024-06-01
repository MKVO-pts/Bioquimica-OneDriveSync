
import main
import os, dotenv
dotenv.load_dotenv()

def opcao_0():
    #path = main.OneDrive_DIR
    path = os.environ.get('OneDrive_DIR')
    print(f"Path: {path}")
    t_files = 0 ; t_dirs = 0 ; size = 0
    for root, dirs, files in os.walk(path):
        for x in files:
            size += os.path.getsize(os.path.join(root,x))
        t_files += len(files)
        t_dirs += len(dirs)
        #print(os.stat(path))
        t_size = format_bytes(size)
    print(t_files,t_dirs, t_size)
#    print(len(main.os.walk(main.OneDrive_DIR)))

def opcao_1():
    main.check_newFiles(main.Stored_PATH,main.NewFiles_PATH,True)

def opcao_2():
    main.full_backup(dest_dir=main.Stored_PATH,src_dir=main.OneDrive_DIR)

def opcao_3():
    main.splited_backup(main.RawStored_PATH)


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return "{:.1f} {}".format(size, power_labels[n])

opcao_0()