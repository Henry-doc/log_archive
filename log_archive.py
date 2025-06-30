import os # used to work with file and directories
import tarfile # used in python to create compressed file 
import argparse # its allows your script to accept command line argument
from datetime import datetime # used to get current date and time 


#SETUP THE ARGUMENT PARSER
parser = argparse.ArgumentParser(description="Archive logs from a directory")
parser.add_argument("log_directory", help="the directory contains log to archive")
args = parser.parse_args()


#GET DATE AND TIME 
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

#SET UP PATHS FOR ARCHIVE ANF LOGS
archive_name = f'logs_archive_{timestamp}.ter.gz'
archive_dir = "archive"
log_file = "archive_log.txt"


#TO CREATE AN ARCHIVE DIRECTORY IF IT DONT HAVE ONE 
os.makedirs(archive_dir, exist_ok=True)

#CREATING THE ARCHIVE FILE
archive_path = os.path.join(archive_dir, archive_name)
with tarfile.open(archive_path, "w:gz") as tar:
    tar.add(args.log_directory, arcname=os.path.basename(args.log_directory))

#WRITE TO THE ARCHIVE LOGS 
with open(log_file, "a") as log:
    log.write(f"{timestamp} - Archive {args.log_directory} to {archive_path}")