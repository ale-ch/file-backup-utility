#####################################################
#### PERIODICALLY BACK UP MULTIPLE FILES AT ONCE ####
#####################################################

print('''
#########################################
########## FILE BACKUP UTILITY ##########
#########################################
''')

import shutil, os, time, copy

path = input('Enter full path to working directory (wd): ').replace('\\', '//')
print('File list\n', os.listdir(path))

file_list_input = input("Enter file name(s) <filename.extension> (separated by a ',')  \
(they need to exist within wd). Leave empty to save all files in wd: ")

backup_path_input = input("Enter full path to backup folder or name of backup folder. \
Leave empty to create a new folder inside wd (default): ").replace('\\', '//')

sleep_time = int(input("Enter frequency of backup (seconds): "))

# set working directory
os.chdir(path)

# if no backup path specified, create a 'backups' folder in working directory
if len(backup_path_input) == 0:
    backup_dir = 'backups'
    backup_path_input = './/backups'
# case full path is specified
elif len(backup_path_input) > 1:
    backup_dir = backup_path_input.split('//')
    backup_dir = backup_dir[len(backup_dir)-1]
    backup_path_input = backup_path_input.replace('\\', '//')
# case input backup path consists of just backup folder name
else:
    backup_dir = copy.deepcopy(backup_path_input)
    backup_path_input = './/' + backup_path_input

# if the path to backup directory does not exist create the directory tree
if not os.path.exists(backup_path_input):
    os.makedirs(backup_path_input)

# if no file is specified select all files inside of wd
# except for backup folder if it's inside wd
if len(file_list_input) == 0:
    if os.path.exists(os.path.join(path, backup_dir)) == True:
        file_list = os.listdir(path)
        file_list.remove(backup_dir)
    else:
        file_list = os.listdir(path)
else:
    file_list = file_list_input.strip()
    file_list = file_list.replace(' ', '')
    file_list = file_list.split(',')

print(file_list)

################# backup function #################
def backup(path, file_list, file_list_input, backup_path_input, j):
    # if file list consists of one element don't create a subfolder
    if len(file_list) == 1:
        backup_path = copy.deepcopy(backup_path_input)
    # if file list is all the content of wd (except for backup folder if it's inside wd)
    elif len(file_list) == len(os.listdir(path)) or len(file_list) == len(os.listdir(path))-1:
        path_list = path.split('//')
        # name backup subfolder as wd_backup_j
        backup_subdir = path_list[len(path_list)-1] + '_' + 'backup' + '_' + str(j)
        # full path to j-th backup subfolder
        backup_path = os.path.join(backup_path_input, backup_subdir).replace('\\', '//')
        os.makedirs(backup_path)
    # if file list is not one element and is not all content of wd
    else:
        # backup subfolder for j-th backup --- i.e. backups_1, backups_2, etc.
        backup_subdir = backup_dir + "_" + str(j)
        # full path to j-th backup subfolder
        backup_path = os.path.join(backup_path_input, backup_subdir).replace('\\', '//')
        os.makedirs(backup_path)

    # create empty lists
    file_list_mod = [None] * len(file_list) # modified file names
    backup_file = [None] * len(file_list) # i-th backup of file list

    # iterate over all input file names
    for i in range(len(file_list)):
        # if i-th file is a folder use shutil.copytree()
        if len(file_list[i].split('.')) == 1:
            if len(file_list) == 1:
                file_list_mod[i] = file_list[i].split('.')[0] + "_" + str(j)
            else:
                file_list_mod[i] = file_list[i]
            # destination path
            backup_file[i] = os.path.join(backup_path, file_list_mod[i]).replace('\\', '//')
            # copy file
            shutil.copytree(file_list[i], backup_file[i])
        # otherwise use shutil.copy()
        else:
            if len(file_list) == 1:
                # modify filename.extension to filename_j.extension
                file_list_mod[i] = file_list[i].split('.')[0] + "_" + str(j) + '.' \
                + file_list[i].split('.')[1]
            else:
                file_list_mod[i] = file_list[i]
            # destination path
            backup_file[i] = os.path.join(backup_path, file_list_mod[i]).replace('\\', '//')
            # copy file
            shutil.copy(file_list[i], backup_file[i])

        print(backup_file[i])
    print(backup_path)

###################################################

j = 1 # index for backup subfolder
while(True): # run script until execution is aborted
    backup(path, file_list, file_list_input, backup_path_input, j)
    print(backup_path_input)
    print(len(file_list))
    j = j + 1 # increase index at each backup
    time.sleep(sleep_time) # pause execution for sleep_time seconds
    
