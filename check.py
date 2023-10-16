import os
import subprocess
import random
import time
import string

temp_folder_name = 'CPP_TEMP'
current_directory = os.getcwd()
temp_folder_path = os.path.join(current_directory, temp_folder_name)
if not os.path.exists(temp_folder_path):
    os.mkdir(temp_folder_path)
