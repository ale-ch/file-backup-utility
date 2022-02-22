# File backup utility.
# To backup periodically, schedule script execution with preferred scheduler app.

print('''
#########################################
########## FILE BACKUP UTILITY ##########
#########################################
''')

import shutil, os, time, copy, logging, re

#### Check that input path is absolute####
def check_path_validity(input_path):
    try:
        if not os.path.isabs(input_path):
            raise Exception
    except Exception:
        print('Invalid path input. Please specify absolute path.')
        time.sleep(5)
        quit()

#### Check that input backup directory is not inside target directory ####
def check_backup_dir_in_td(backup_path_input, target_dir):
    backup_dir_name = os.path.split(backup_path_input)[1]
    try:
        if backup_path_input == os.path.join(target_dir, backup_dir_name):
            raise Exception
    except Exception:
        print('Backup directory cannot be inside td.')
        time.sleep(5)
        quit()

#### Check that all specified items exist in target directory ####
def check_item_in_td(target_dir, item_list):
    target_listdir = os.listdir(target_dir)
    bad_items = [None] * len(item_list)
    try:
        for i in range(len(item_list)):
            if item_list[i] not in target_listdir:
                bad_items[i] = item_list[i]

        bad_items = list(filter(None, bad_items))
        if len(bad_items) != 0:
            raise Exception
    except Exception:
        print('Item(s) {} not in target directory.'.format(bad_items))
        time.sleep(5)
        quit()

#### Count previous backups of the same file or folder ####
#### inside specified backup directory ####
def count_prev_backups(target_dir, backup_path_input, item_list):
    target_listdir = os.listdir(target_dir)
    target_dir_name = os.path.split(target_dir)[1]

    backup_listdir = os.listdir(backup_path_input)

    # if file list is one element -> target item is the item name
    if len(item_list) == 1:
        target_item_path = os.path.join(target_dir, item_list[0])
        # if the item is a file split file name and extension
        if os.path.isfile(target_item_path):
            target_item = os.path.splitext(item_list[0])
        # otherwise take the name of the folder
        else:
            target_item = [item_list[0]]
    # otherwise it's the target directory name
    else:
        target_item = [target_dir_name]


    regex_match = [None] * len(backup_listdir)
    # look for previous backups of the target item inside of backup directory
    for i in range(len(backup_listdir)):
        # if target item is a folder check for pattern target_item(regex)
        if len(target_item) == 1:
            regex_match[i] = re.search(target_item[0] + '(_backup_\d+)$', backup_listdir[i])
        # otherwise look for target_item(regex).extension
        else:
            regex_match[i] = re.search(target_item[0] + '_backup_\d+' + target_item[1],\
                            backup_listdir[i])

        # if a match is found, get backup number from regex pattern
        if regex_match[i] != None:
            regex_match[i] = regex_match[i].group()
            backup_count = int(re.search('\d+', regex_match[i]).group())
        # otherwise backup count is zero
        else:
            backup_count = 0

    return backup_count

#### Make input item list with input item names ####
def make_item_list(target_dir, item_list_input):
    # if no item is specified select all items inside of td
    if len(item_list_input) == 0:
        item_list = os.listdir(target_dir)
    # otherwise make a list with input item names
    else:
        item_list = item_list_input.strip()
        item_list = item_list.replace(' ', '')
        item_list = item_list.split('|')

    return item_list


def main():
    #### Create backup directory tree ####
    def make_backup_path(target_dir, item_list, backup_path_input, j):
        backup_dir_name = os.path.split(backup_path_input)[1]
        # if item list consists of one element don't create a subfolder
        if len(item_list) == 1:
            backup_path = copy.deepcopy(backup_path_input)
        else:
            target_dir_name = os.path.split(target_dir)[1]
            # name backup subfolder as td_backup_j
            backup_subdir = target_dir_name + '_backup_' + str(j)
            # full path to j-th backup subfolder
            backup_path = os.path.join(backup_path_input, backup_subdir)

        # if the path to backup directory does not exist create the directory tree
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        return backup_path

    #### Backup items in item list to backup directory ####
    def backup(target_dir, backup_path, item_list, j):
        # create empty lists
        item_list_bu = [None] * len(item_list) # modified item names
        dest_path = [None] * len(item_list) # i-th backup of item list

        # iterate over all input item names
        for i in range(len(item_list)):
            # if i-th item is a folder use shutil.copytree()
            if os.path.isdir(os.path.join(target_dir, item_list[i])):
                if len(item_list) == 1:
                    item_list_bu[i] = item_list[i] + '_backup_' + str(j)
                else:
                    item_list_bu[i] = item_list[i]
                # destination path
                dest_path[i] = os.path.join(backup_path, item_list_bu[i])
                # copy item
                shutil.copytree(item_list[i], dest_path[i])
            # otherwise use shutil.copy()
            else:
                if len(item_list) == 1:
                    # modify itemname.extension to itemname_j.extension
                    item_list_bu[i] = os.path.splitext(item_list[i])[0] \
                                + '_backup_' + str(j) + os.path.splitext(item_list[i])[1]
                else:
                    item_list_bu[i] = item_list[i]

                # destination path
                dest_path[i] = os.path.join(backup_path, item_list_bu[i])
                # copy item
                shutil.copy(item_list[i], dest_path[i])

            logger.debug('item backed up to: {}'.format(dest_path[i]))
        logger.debug('Number of backed up items: {}'.format(len(item_list)))
    ######################

    #### INPUTS ####
    target_dir = input('Enter full path to target directory (td): ')
    check_path_validity(target_dir)
    print('Content of td:')
    print(os.listdir(target_dir))

    item_list_input = input("Enter item name(s) as <itemname.extension> (separated by a '|').\
    Items need to exist within td. Leave empty to backup all items in td: ")
    item_list = make_item_list(target_dir, item_list_input)
    check_item_in_td(target_dir, item_list)

    backup_path_input = input("Enter full path to backup folder: ")
    check_path_validity(backup_path_input)
    check_backup_dir_in_td(backup_path_input, target_dir)
    ######################

    ##### LOGGER CONFIGURATION #####
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    file_handler = logging.FileHandler(backup_path_input + '//backup_log.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    ######################################

    logger.debug('Path to main backup directory: {}'.format(backup_path_input))
    logger.debug('List of items to backup: {}'.format(item_list))

    # Index for current backup
    backup_count = count_prev_backups(target_dir, backup_path_input, item_list)
    if backup_count == 0: j = 1
    else: j = backup_count + 1

    backup_path = make_backup_path(target_dir, item_list, backup_path_input, j)
    backup(target_dir, backup_path, item_list, j)


if __name__ == '__main__':
    main()
