import os # used to work with file and directories
import tarfile # used in python to create compressed file 
import argparse # its allows your script to accept command line argument
from datetime import datetime # used to get current date and time 
import smtplib 
from email.mime.text import MIMEText
import boto3 


#SETUP THE ARGUMENT PARSER
parser = argparse.ArgumentParser(description="Archive logs from a directory")
parser.add_argument("log_directory", help="the directory contains log to archive")
parser.add_argument("--keep-original", action="store_true", help="keep original logs after archiving")
parser.add_argument("--verbose", action="store_true", help="print detail status")
parser.add_argument("--email", help="send an email alert to this address")
parser.add_argument("--s3-bucket", help="upload archive to this s3 bucket")
args = parser.parse_args()


#GET DATE AND TIME 
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

#SET UP PATHS FOR ARCHIVE ANF LOGS
archive_name = f'logs_archive_{timestamp}.tar.gz'
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

#TO REMOVE ORIGINAL LOGS
if not args.keep_original:
    if args.verbose:
        print("deleting original logs")
    for root, _, files in os.walk(args.log_directory):
        for file in files:
            try:
                os.remove(os.path.join(root, file))
            except Exception as e:
                print(f"Error deleting {file}:", e)

#TO SEND EMAIL NOTIFICATION
def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    password = "your_email_password"  # Use environment variables in real projects

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        print("❌ Email failed:", e)

# Only send if --email is provided
if args.email:
    send_email(
        "✅ Log Archive Complete",
        f"The logs from {args.log_directory} were archived as {archive_name}.",
        args.email
    )
    if args.verbose:
        print("📨 Email notification sent.")
