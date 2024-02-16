import os
import ftplib
import socket
import time
import logging
import zipfile
from pathlib import Path

hostname = "xxx.xxx.xxx.xxx" # FTP IP Address 
username = "XXXXXXXXX" # FTP User Name
password = "XXXXXXXX" # FTP Password
local_dir = "C:\\XXXXX" # Insert the LOCAL path
remote_dir = "//Notas" #insert only the REMOTE directory
directory = "C:\\Notas" #Insert the LOCAL directory

fmt = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt, handlers=[logging.StreamHandler(), logging.FileHandler("ftp.log")])
while True:

    # First try/except block
    try:
        def extract_zip_files(directory):
            p = Path(directory)
            for f in p.glob('*.zip'):
                with zipfile.ZipFile(f, 'r') as archive:
                    archive.extractall("c:\\Notas")
                    print(f"Extracted contents from '{f.name}' to '{f.stem}' directory.")

        # Usage example
        extract_zip_files("c:\\Notas")

        file_list = os.listdir(local_dir)
        
        # Validating if there are files
        if not file_list:
            logging.info("No files to upload, waiting for new files...")
            time.sleep(300)
            continue
                    
        with ftplib.FTP(host=hostname, user=username, passwd=password) as ftp:
            logging.info("Connection established with FTP server")
            ftp.cwd(remote_dir)
            logging.info(f"Accessing {remote_dir}")
            for file_name in file_list:
                # Second try/except block
                try:
                    file_path = os.path.join(local_dir, file_name)
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            logging.info(f"Uploading {file_name}...")
                            ftp.storbinary(f'STOR {file_name}', file)
                        os.remove(file_path)
                except Exception as e:
                    logging.error(f'Error uploading {file_name}: {str(e)}')
                    continue

            logging.info(f"Uploaded all files to {remote_dir}")

        logging.info(f"The process will restart in five minutes")
        time.sleep(300)

    except socket.gaierror:
        logging.critical('Invalid Hostname.')
        break

    except ftplib.error_perm:
        logging.critical('Invalid username, password or remote '
                         'directory path.')
        break

    except FileNotFoundError:
        logging.critical(f'{local_dir} is not a valid directory.' 
                          'Please check path informed.')
        break