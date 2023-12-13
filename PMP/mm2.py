import os
import shutil
import fileinput

# Define the paths
staging_path = os.path.expanduser('/Users/polaris/PMPx/genesis_main/app/PMP/message_manager/staging')
export_path = os.path.expanduser('/Users/polaris/PMPx/genesis_main/app/PMP/message_manager/data')

# Iterate over each file in the staging directory
for root, dirs, files in os.walk(staging_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        
        try:
            # Open each file and look for links containing 'attachments'
            with fileinput.FileInput(file_path, inplace=True, mode='r', encoding='utf-8') as file:
                for line in file:
                    # Replace 'attachments' with 'data' in these links
                    print(line.replace('attachments', 'data'), end='')
            
            # Move the modified file to the data directory
            shutil.move(file_path, export_path)

        except UnicodeDecodeError:
            print(f"UnicodeDecodeError encountered in file: {file_path}")
