###############################################
# PERIODICALLY BACK UP MULTIPLE FILES AT ONCE #
###############################################

print('''
#########################################
########## FILE BACKUP UTILITY ##########
#########################################
''')

import numpy, shutil, os, time

path = input('Enter full path to working directory: ').replace('\\', '//')
print('File list\n', os.listdir(path))

file_list_input = input("Enter file name(s) <filename.extension> (separated by a ',')  \
(they need to exist within wd). Leave empty to save all files in wd: ")

backup_path_input = input("Enter full path to backup folder or name of backup folder. \
Leave empty to create a default new folder inside wd): ").replace('\\', '//')

sleep_time = int(input("Enter backup frequency (seconds): "))

# set working directory
os.chdir(path)

if len(backup_path_input) == 0:
    # if no backup path specified, create a 'backups' folder in working directory
    backup_dir = 'backups'
    backup_path_input = './/backups'
elif len(backup_path_input) > 1:
    # else just take input backup path
    backup_dir = backup_path_input.split('//')
    backup_dir = backup_dir[len(backup_dir)-1]
    backup_path_input = backup_path_input.replace('\\', '//')
else:
    # case input backup path consists of just backup folder name
    backup_dir = copy.deepcopy(backup_path_input)
    backup_path_input = './/' + backup_path_input

# if the path to backup directory does not exist, create the directory tree
if not os.path.exists(backup_path_input):
    os.makedirs(backup_path_input)

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


################# backup function #################
def backup(file_list, file_list_input, backup_path_input, j):
    # if input file list is left empty
    if len(file_list_input) == 0:
        path_list = path.split('//')
        backup_subdir = path_list[len(path_list)-1] + '_' + 'backup' + '_' + str(j)
        # full path to j-th backup subfolder
        backup_path = os.path.join(backup_path_input, backup_subdir).replace('\\', '//')
    else:
        # backup subfolder for j-th backup --- i.e. backups_1, backups_2, etc.
        backup_subdir = backup_dir + "_" + str(j)
        # full path to j-th backup subfolder
        backup_path = os.path.join(backup_path_input, backup_subdir).replace('\\', '//')

    os.makedirs(backup_path)

    # create empty lists
    backup_file = [None] * len(file_list) # i-th backup of file list
    file_list_mod = [None] * len(file_list) # modified file names

    # iterate over all input file names
    for i in range(len(file_list)):
        # conver filename.extension to filename_j.extension
        file_list_mod[i] = file_list[i].split('.')[0] + "_" + str(j) + '.' \
        + file_list[i].split('.')[1]
        # destination path
        backup_file[i] = os.path.join(backup_path, file_list_mod[i]).replace('\\', '//')
        # copy file
        shutil.copy(file_list[i], backup_file[i])
###################################################

j = 1 # index for backup subfolder
while(True): # run script until execution is aborted
    backup(file_list, file_list_input, backup_path_input, j)
    j = j + 1 # increase index at each backup
    time.sleep(sleep_time) # pause execution for sleep_time seconds
