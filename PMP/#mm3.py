#mm3.py

import subprocess
import os
import filecmp
import shutil
import glob
import hashlib

def calculate_checksum(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read() 
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash

def export_imessages():
    # Path to the staging directory
    staging_path = os.path.expanduser('/Users/polaris/PMPx/genesis_main/app/PMP/message_manager/staging')

    # Path to the exported iMessage chats
    export_path = os.path.expanduser('/Users/polaris/PMPx/genesis_main/app/PMP/message_manager/data')

    # Path to the target directory
    target_path = os.path.expanduser('/Users/polaris/PMPx/genesis_main/app/PMP/message_manager/processing')

    # Delete all files in the staging directory
    #files = glob.glob(staging_path + '/*')
    #for f in files:
    #    os.remove(f)

    # Command to export iMessages
    export_command = 'imessage-exporter -f html -c compatible -o ' + export_path

    # Run the command in the shell
    subprocess.run(export_command, shell=True)



if __name__ == "__main__":
    export_imessages()