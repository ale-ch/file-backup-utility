import os
import argparse
import shutil
import re
import logging
from pathlib import Path

##### LOGGER CONFIGURATION #####
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

#### Check that input path is absolute####
def check_path_abs(input_path):
    if not os.path.isabs(input_path):
        print('Invalid path input. Please specify absolute path.')
        quit()

#### Check that input backup directory is not inside target directory ####
def check_backup_dir_in_td(backup_path_input, target_dir):
    child_path = Path(backup_path_input)
    if child_path.is_relative_to(target_dir): 
        print('Backup directory cannot be inside td.')
        quit()

def check_td_empty(target_dir):
    if len(os.listdir(target_dir)) == 0:
        print('Target directory is empty.')
        quit()

#### Check that all specified items exist in target directory ####
def check_item_in_td(target_dir, item_list):
    target_listdir = os.listdir(target_dir)
    missing_items = [item for item in item_list if item not in target_listdir]
    if missing_items:
        print(f'Item(s) {missing_items} not in target directory.')
        quit()

#### Count existing backups, if any ####
def count_prev_backups(target_dir, backup_dir, item_list):
    if not os.path.exists(backup_dir):  
        backup_count = 0
    else:
        backup_listdir = os.listdir(backup_dir)
        if len(backup_listdir) == 0:
            backup_count = 0
        else:
            if len(item_list) > 1:
                target_item = [os.path.split(target_dir)[1]] # name of target directory
            else:
                target_item_path = os.path.join(target_dir, item_list[0])
                if os.path.isfile(target_item_path):
                    target_item = os.path.splitext(item_list[0])
                else:
                    target_item = [item_list[0]]

            backup_count = list()
            regex_match = None
            # look for previous backups of the target item inside of backup directory
            for i in range(len(backup_listdir)):
                # if target item is a folder check for pattern target_item(regex)
                if len(target_item) == 1:
                    regex_match = re.search(f'{target_item[0]}_backup_\\d+', backup_listdir[i])
                # otherwise look for target_item(regex).extension
                else:
                    regex_match = re.search(f'{target_item[0]}_backup_\\d+{target_item[1]}', backup_listdir[i])

                # if a match is found, get backup number from regex pattern
                if regex_match is not None:
                    regex_match = regex_match.group()
                    backup_count.append(int(re.search('\\d+', regex_match).group()))
                else:
                    backup_count.append(0)
                
            backup_count = max(backup_count)

    return backup_count

def make_item_list(target_dir, item_list_input):
    if len(item_list_input) == 0:
        item_list = os.listdir(target_dir)
    else:
        item_list = item_list_input.strip()
        item_list = item_list.split(':')
    
    item_list = [item.strip() for item in item_list]
    
    return item_list
    
def make_backup_path(target_dir, item_list, backup_dir, j):
    if len(item_list) > 1:
        target_dir_name = os.path.split(target_dir)[1]
        backup_subdir = f'{target_dir_name}_backup_{j}'
        backup_path = os.path.join(backup_dir, backup_subdir)        
    else:
        backup_path = backup_dir  

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    return backup_path

def backup(target_dir, backup_path, item_list, j):
    if len(item_list) > 1:
        for item in item_list:
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, backup_path)
            else:
                shutil.copytree(item_path, backup_path)

            logger.debug(f'Item backed up to: {backup_path}')
    else:
        item_path = os.path.join(target_dir, item_list[0])
        if os.path.isfile(item_path):
            file_name, ext = os.path.splitext(item_list[0])
            backed_up_file_name = f'{file_name}_backup_{j}{ext}'
            shutil.copy(item_path, os.path.join(backup_path, backed_up_file_name))
        else:
            backed_up_file_name = f'{item_list[0]}_backup_{j}'
            shutil.copytree(item_path, os.path.join(backup_path, backed_up_file_name))

    logger.debug(f'Number of backed up items: {len(item_list)}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-target_dir', type = str, help = "Directory containing the files to backup. Needs to be an absolute path.")
    parser.add_argument('-backup_dir', type = str, help = "Directory where files are backed up. Needs to be an absolute path.")
    parser.add_argument('-item_list', type = str, help = "List of files to backup. Input as <itemname.extension>, separated by a '|'.\
                                All items need to exist within target directory. Leave empty to backup all items in td")
    
    args = parser.parse_args()

    target_dir = args.target_dir
    check_path_abs(target_dir)
    check_td_empty(target_dir)

    backup_dir = args.backup_dir
    check_path_abs(backup_dir)
    check_backup_dir_in_td(backup_dir, target_dir)
    
    item_list_input = args.item_list
    item_list = make_item_list(target_dir, item_list_input)
    check_item_in_td(target_dir, item_list)

    # Backup counter
    j = count_prev_backups(target_dir, backup_dir, item_list) + 1

    backup_path = make_backup_path(target_dir, item_list, backup_dir, j)
    

    ##### LOGGER FILE HANDLER #####
    file_handler = logging.FileHandler(backup_dir + '//backup_log.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Log info
    logger.debug(f'Path to main backup directory: {backup_dir}')
    logger.debug(f'List of items to backup: {item_list}')

    backup(target_dir, backup_path, item_list, j)
    
if __name__ == '__main__':
    main()
