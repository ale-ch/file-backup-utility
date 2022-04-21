from utils import *

import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

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

    file_handler = logging.FileHandler(backup_dir + '//backup_log.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.debug(f'Path to main backup directory: {backup_dir}')
    logger.debug(f'List of items to backup: {item_list}')

    backup(target_dir, backup_path, item_list, j, logger)
    
if __name__ == '__main__':
    main()
