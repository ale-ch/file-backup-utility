#####################################################
#### PERIODICALLY BACK UP MULTIPLE FILES AT ONCE ####
#####################################################

print('''
#########################################
########## FILE BACKUP UTILITY ##########
#########################################
''')

import shutil, os, time, copy, logging

def main():
    ######## FUNCTIONS ########
    
    #### CHECK THAT INPUT PATH IS ABSOLUTE ####
    def check_path_validity(input_path):
        try:
            if not os.path.isabs(input_path):
                raise Exception
        except Exception:
            print('Invalid path input. Please specify absolute path.')
            time.sleep(5)
            quit()

    #### CHECK THAT INPUT BACKUP DIRECTORY IS NOT INSIDE TARGET DIRECTORY ####
    def check_backupdir_in_td(backup_path_input, backup_dir_name, target_dir):
        try:
            if backup_path_input == os.path.join(target_dir, backup_dir_name).replace('\\', '//'):
                raise Exception
        except Exception:
            print('Backup directory cannot be inside td.')
            time.sleep(5)
            quit()

    #### RETURN NAME OF BACKUP DIRECTORY ####
    def get_backup_dir_name(backup_path_input):
        backup_dir_name = backup_path_input.split('//')
        backup_dir_name = backup_dir_name[-1]

        return backup_dir_name

    #### MAKE A FILE LIST WITH THE INPUT FILE NAMES ####
    def make_file_list(target_dir, file_list_input):
        # if no file is specified select all files inside of td
        if len(file_list_input) == 0:
            file_list = os.listdir(target_dir)
        # otherwise make a list with input file names
        else:
            file_list = file_list_input.strip()
            file_list = file_list.replace(' ', '')
            file_list = file_list.split(',')

        return file_list

    #### CREATE BACKUP DIRECTORY TREE ####
    def make_backup_path(target_dir, file_list, backup_path_input, backup_dir_name):
        # if file list consists of one element don't create a subfolder
        if len(file_list) == 1:
            backup_path = copy.deepcopy(backup_path_input)
        # if file list is all the content of td (except for backup folder if it's inside td)
        elif len(file_list) == len(os.listdir(target_dir)):
            target_dir_name = target_dir.split('//')
            # name backup subfolder as td_backup_j
            backup_subdir = target_dir_name[-1] + '_' + 'backup' + '_' + str(j)
            # full path to j-th backup subfolder
            backup_path = os.path.join(backup_path_input, backup_subdir).replace('\\', '//')
        # if file list is not one element and is not all content of td
        else:
            # backup subfolder for j-th backup --- i.e. backups_1, backups_2, etc.
            backup_subdir = backup_dir_name + "_" + str(j)
            # full path to j-th backup subfolder
            backup_path = os.path.join(backup_path_input, backup_subdir).replace('\\', '//')

        # if the path to backup directory does not exist create the directory tree
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        return backup_path

    #### BACKUP FILES IN FILE LIST TO BACKUP PATH ####
    def backup(backup_path, file_list, j):
        # create empty lists
        file_list_mod = [None] * len(file_list) # modified file names
        dest_path = [None] * len(file_list) # i-th backup of file list

        # iterate over all input file names
        for i in range(len(file_list)):
            # if i-th file is a folder use shutil.copytree()
            if len(file_list[i].split('.')) == 1:
                if len(file_list) == 1:
                    file_list_mod[i] = file_list[i].split('.')[0] + "_" + str(j)
                else:
                    file_list_mod[i] = file_list[i]

                # destination path
                dest_path[i] = os.path.join(backup_path, file_list_mod[i]).replace('\\', '//')
                # copy file
                shutil.copytree(file_list[i], dest_path[i])
            # otherwise use shutil.copy()
            else:
                if len(file_list) == 1:
                    # modify filename.extension to filename_j.extension
                    file_list_mod[i] = file_list[i].split('.')[0] + "_" + str(j) + '.' \
                    + file_list[i].split('.')[1]
                else:
                    file_list_mod[i] = file_list[i]

                # destination path
                dest_path[i] = os.path.join(backup_path, file_list_mod[i]).replace('\\', '//')
                # copy file
                shutil.copy(file_list[i], dest_path[i])

            logger.debug('File backed up to: {}'.format(dest_path[i]))
        logger.debug('Number of backed up files: {}'.format(len(file_list)))

    ######################
    
    #### INPUTS ####
    target_dir = input('Enter full path to target directory (td): ').replace('\\', '//')
    check_path_validity(target_dir)

    print('Content of td:')
    print(os.listdir(target_dir))

    file_list_input = input("Enter file name(s) as <filename.extension> (separated by a ',').\
    Files need to exist within td. Leave empty to backup all files in td: ")
    file_list = make_file_list(target_dir, file_list_input)

    backup_path_input = input("Enter full path to backup folder: ").replace('\\', '//')
    backup_dir_name = get_backup_dir_name(backup_path_input)
    check_path_validity(backup_path_input)
    check_backupdir_in_td(backup_path_input, backup_dir_name, target_dir)

    sleep_time = int(input("Enter frequency of backup (seconds): "))
    ######################

    ##### LOGGER CONFIGURATION #####
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    file_handler = logging.FileHandler(backup_path_input + '//backup_log.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    #######################

    logger.debug('Path to main backup directory: {}'.format(backup_path_input))
    logger.debug('List of files to backup: {}'.format(file_list))

    j = 1 # index for backup subfolder
    while True: # run script until execution is aborted
        backup_path = make_backup_path(target_dir, file_list, backup_path_input,
                                        backup_dir_name)
        backup(backup_path, file_list, j)
        j = j + 1 # increase index at each backup

        time.sleep(sleep_time) # pause execution for sleep_time seconds

if __name__ == '__main__':
    main()
