import os
import subprocess
import random
import time
import string


temp_folder_name = 'COMPILER_TEMP'
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
            return ("Runtime Error: " + e.output,0)
        # Execute the compiled program within the temporary folder
        executable_name = os.path.join(temp_folder_path, f"{random_file_name}.exe")
        try:
            start_time = time.time()
            result = subprocess.check_output(executable_name, shell=True, stderr=subprocess.STDOUT, text=True, cwd=temp_folder_path)
            end_time = time.time()
            runtime = end_time-start_time
        except subprocess.CalledProcessError as e:
            runtime = 0
            result = "Compile Time Error" + e.output
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
    code = code.replace('\t', '    ')
    try:
        start_time = time.time()
        result = subprocess.check_output(['python', '-c',code], stderr=subprocess.STDOUT, text=True)
        end_time = time.time()
        runtime = end_time-start_time
    except subprocess.CalledProcessError as e:
        result =  "Compile Time Error" + e.output
        runtime = 0
    return (result,runtime)

def compile_java(code):
    # Generate a random file name within the temporary folder
    random_file_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    code = code.replace("Solution",random_file_name)
    java_file_name = os.path.join(temp_folder_path, f"{random_file_name}.java")
    
    # Save the Java code to the random file
    with open(java_file_name, "w") as java_file:
        java_file.write(code)

    # Compile the Java code to a class file within the temporary folder
    compile_command = f"javac {java_file_name}"
    try:
        subprocess.check_output(compile_command, shell=True, stderr=subprocess.STDOUT, text=True, cwd=temp_folder_path)
    except subprocess.CalledProcessError as e:
        try:
            os.remove(java_file_name)
        except:
            pass
        return ("Runtime Error: " + e.output, 0)

    # Execute the compiled Java program within the temporary folder
    class_name = random_file_name
    try:
        start_time = time.time()
        result = subprocess.check_output(f"java {class_name}", shell=True, stderr=subprocess.STDOUT, text=True, cwd=temp_folder_path)
        end_time = time.time()
        runtime = end_time - start_time
    except subprocess.CalledProcessError as e:
        runtime = 0
        result = e.output

    try:
        os.remove(java_file_name)
    except:
        pass
    try:
        os.remove(f"{class_name}.class")
    except:
        pass

    return (result, runtime)