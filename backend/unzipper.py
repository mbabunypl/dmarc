import os
import gzip as gz
import zipfile
import shutil


def unzip_reports(folder_path):
    reports_folder = os.path.abspath(folder_path)
    
    for file_name in os.listdir(reports_folder):
        file_path = os.path.join(reports_folder, file_name)
        
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(reports_folder)
            os.remove(file_path) # Removes the zipfile and gzfile 
                
        if file_name.endswith('.gz'):
            with gz.open(file_path,'rb') as gz_file:
                with open(file_path[:-3],'wb') as uncompressed_file:
                    shutil.copyfileobj(gz_file,uncompressed_file)
            os.remove(file_path) # Removes the zipfile and gzfile 



