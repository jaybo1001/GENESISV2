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
    files = glob.glob(staging_path + '/*')
    for f in files:
        os.remove(f)

    # Command to export iMessages
    export_command = 'imessage-exporter -f html -c compatible -o ' + staging_path

    # Run the command in the shell
    subprocess.run(export_command, shell=True)

    # Count the number of downloaded messages
    downloaded_files = glob.glob(staging_path + '/*')
    print(f"Downloaded {len(downloaded_files)} messages.")

    # Calculate checksums for files in staging and export directories
    staging_checksums = {f: calculate_checksum(os.path.join(staging_path, f)) for f in os.listdir(staging_path) if os.path.isfile(os.path.join(staging_path, f))}
    export_checksums = {f: calculate_checksum(os.path.join(export_path, f)) for f in os.listdir(export_path) if os.path.isfile(os.path.join(export_path, f))}

    # Determine new files based on checksum comparison
    new_files = [f for f in staging_checksums if f not in export_checksums or staging_checksums[f] != export_checksums[f]]

    # Delete all files in the target directory
    files = glob.glob(target_path + '/*')
    for f in files:
        os.remove(f)

     # Append new messages to the export directory and copy them to the target directory
    for file in new_files:
        # Copy the file to the target directory
        shutil.copy(os.path.join(staging_path, file), target_path)
        
        # Move the file to the export directory, overwriting if it already exists
        destination_file = os.path.join(export_path, file)
        if os.path.exists(destination_file):
            os.remove(destination_file)
        shutil.move(os.path.join(staging_path, file), destination_file)

    print(f"Added {len(new_files)} new records.")

if __name__ == "__main__":
    export_imessages()