from ftplib import FTP
import os
import logging
from datetime import datetime


log_file_path = os.path.join(os.getcwd(), 'summary.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s '
                                                                       '%(name)s '
                                                                       '- %(levelname)s - %(message)s')

def server_folder(ftp, folder, local_dir):
    try:
        os.makedirs(local_dir)
    except OSError:
        pass  # Ignore this exception

    ftp.cwd(folder)
    items = ftp.nlst()  # get items from ftp server

    for item in items:
        local_path = os.path.join(local_dir, item)
        try:
            if '.' in item:  # check for . extensions
                with open(local_path, 'wb') as f:
                    ftp.retrbinary('RETR ' + item, f.write)  #RETR is to retrieve a file from the FTP server;retrbinary is to retrieve a file from FTP server in binary mode

            else:
                server_folder(ftp, item, local_path)
        except Exception as e:  # only print if file is unable to download from FTP to localhost
            logging.error(f"Error downloading {item}: {e}")
            logging.error(f"Error downloading files from FTP server {ftp.host()}")

def write_summary_file():
    current_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')  # Date and time in specified format
    logging.info("Downloading file from ftp server done.")

# FTP server credentials (login:password ftp-admin:admin)
ftp_host = '127.0.0.1'
ftp_user = 'ftp-admin'
ftp_passwd = 'admin'
ftp_folder = '/project_resource/resource/do_not_touch'  # Update the FTP folder path
local_dir = os.path.join(os.getcwd(), 'history_a')

# Main code block
try:
    with FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_passwd)  # Log in to FTP server using credentials above
        server_folder(ftp, ftp_folder, local_dir)
        write_summary_file()
except Exception as e:  # Handle exceptions that occur during execution
    logging.error(f"Error: {e}")
