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


def compile_cpp(code):

        # Generate a random file name within the temporary folder
        random_file_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        cpp_file_name = os.path.join(temp_folder_path, f"{random_file_name}.cpp")

        # Save the C++ code to the random file
        with open(cpp_file_name, "w") as cpp_file:
            cpp_file.write(code)

        # Compile the C++ code to an executable within the temporary folder
        compile_command = f"g++ {cpp_file_name} -o {os.path.join(temp_folder_path, random_file_name)}.exe"
        try:
            subprocess.check_output(compile_command, shell=True, stderr=subprocess.STDOUT, text=True, cwd=temp_folder_path)
        except subprocess.CalledProcessError as e:
            try:
                os.remove(cpp_file_name)
            except:
                pass
            return (e.output,0)
        # Execute the compiled program within the temporary folder
        executable_name = os.path.join(temp_folder_path, f"{random_file_name}.exe")
        try:
            start_time = time.time()
            result = subprocess.check_output(executable_name, shell=True, stderr=subprocess.STDOUT, text=True, cwd=temp_folder_path)
            end_time = time.time()
            runtime = end_time-start_time
        except subprocess.CalledProcessError as e:
            runtime = 0
            result = e.output
        try:
            os.remove(cpp_file_name)
        except:
            pass
        try:
            os.remove(executable_name)
        except:
            pass
        return (result,runtime)

def compile_python(code):
    try:
        start_time = time.time()
        result = subprocess.check_output(['python', '-c',code], stderr=subprocess.STDOUT, text=True)
        end_time = time.time()
        runtime = end_time-start_time
    except subprocess.CalledProcessError as e:
        result = e.output
        runtime = 0
    return (result,runtime)
