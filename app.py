from flask import Flask, render_template, request, jsonify,redirect
from cs50 import SQL
from compiler import compile_python,compile_cpp,compile_java
import subprocess
import time
import os


app = Flask(__name__)

try:
    db = SQL("sqlite:///problems.db")
except:
    db = SQL("sqlite:////home/oopsididit/mysite/problems.db")


db.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        problem_id INTEGER PRIMARY KEY,
        problem_name TEXT,
        problem_description TEXT,
        test_cases TEXT,
        constraints TEXT,
        boiler_code_python TEXT,
        function_call_python TEXT,
        boiler_code_cpp TEXT,
        function_call_cpp TEXT,
        boiler_code_java TEXT,
        function_call_java TEXT,
        testing_code TEXT
    )
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS python (
        problem_id INTEGER PRIMARY KEY,
        problem_name TEXT,
        problem_description TEXT,
        test_cases TEXT,
        constraints TEXT,
        boiler_code_python TEXT,
        function_call_python TEXT,
        testing_code TEXT,
        postitive_keywords TEXT,
        negative_keywords TEXT
    )
""")

db.execute("""
CREATE TABLE IF NOT EXISTS request_logs (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT,
    http_method TEXT,
    url TEXT
)
""")

@app.before_request
def log_request_info():
    # Log request details to the database
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    http_method = request.method
    url = request.url
    db.execute("INSERT INTO request_logs (ip_address, user_agent, http_method, url) VALUES (? ,? ,? , ?)",
    ip_address, user_agent, http_method, url)
    
@app.route('/problems')
def problems():
    problems = db.execute("SELECT * from problems")
    return render_template('problems.html',problems=problems)

@app.route('/python_problems')
def python_problems():
    problems = db.execute("SELECT * from python")
    return render_template('python_problems.html',problems=problems)

@app.route('/create_sample')
def create_sample():
    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases, constraints, boiler_code_python, boiler_code_cpp, testing_code, function_call_cpp, function_call_python, boiler_code_java, function_call_java)
    VALUES (
        'Sum of Squares',
        'You are given a single integer n (1 ≤ n ≤ 1000) representing the range. Your task is to calculate the sum of squares of all positive integers from 1 to n inclusive. Write a program to find this sum using the following formula: Sum = 1² + 2² + 3² + ... + n²',
        'Test Case 1: Input : n = 5\nOutput: 55\nExplanation: the first 5 positive integers (1² + 2² + 3² + 4² + 5²) which results in a sum of 55.\n\nTest Case 2: Input : n = 8\nOutput: 204',
        '1 ≤ n ≤ 1000',
        'def square(n):\n    # return the answer',
        '#include <iostream>\nusing namespace std;\n\nint square(int n) {\n    // return the answer\n}',
        'def square(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i ** 2\n    return total',
        'int main() {\n    int n = 5;\n    cout << square(n) << endl;\n    n = 8;\n    cout << square(n) << endl;\n    return 0;\n}',
        'n = 5\nprint(square(n))\nn = 8\nprint(square(n))',
        'public class Solution {\n    public static int square(int n) {\n        // return the answer\n    }\n}',
        'public static void main(String[] args) {\n    int n = 5;\n    System.out.println(Solution.square(n));\n    n = 8;\n    System.out.println(Solution.square(n));\n}\n}'
    );
""")

    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases, constraints, boiler_code_python, boiler_code_cpp, testing_code, function_call_cpp, function_call_python, boiler_code_java, function_call_java)
    VALUES (
        'Sum of Integers',
        'You are given a single integer n (1 ≤ n ≤ 1000) representing the range. Your task is to calculate the sum of all positive integers from 1 to n inclusive. Write a program to find this sum using the following formula: Sum = 1 + 2 + 3 + ... + n',
        'Test Case 1: Input: n = 5\nOutput: 15\nExplanation: The sum of integers from 1 to 5 is 1 + 2 + 3 + 4 + 5, which results in a sum of 15.\n\nTest Case 2: Input: n = 8\nOutput: 36',
        '1 ≤ n ≤ 1000',
        'def calculate_sum(n):\n    # return the answer',
        '#include <iostream>\nusing namespace std;\n\nint calculate_sum(int n) {\n    // return the answer\n}',
        'def calculate_sum(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total',
        'int main() {\n    int n = 5;\n    cout << calculate_sum(n) << endl;\n    n = 8;\n    cout << calculate_sum(n) << endl;\n    return 0;\n}',
        'n = 5\nprint(calculate_sum(n))\nn = 8\nprint(calculate_sum(n))',
        'public class Solution {\n    public static int calculateSum(int n) {\n        // return the answer\n    }\n}',
        'public static void main(String[] args) {\n    int n = 5;\n    System.out.println(Solution.calculateSum(n));\n    n = 8;\n    System.out.println(Solution.calculateSum(n));\n}\n}'
    );
""")

    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases, constraints, boiler_code_python, boiler_code_cpp, testing_code, function_call_cpp, function_call_python, boiler_code_java, function_call_java)
    VALUES (
        'Factorial Calculation',
        'You are given a single integer n (0 ≤ n ≤ 12) representing a non-negative integer. Your task is to calculate the factorial of n. The factorial of a non-negative integer n is the product of all positive integers less than or equal to n.',
        'Test Case 1: Input: n = 5\nOutput: 120\nExplanation: 5! = 5 * 4 * 3 * 2 * 1 = 120.\n\nTest Case 2: Input: n = 0\nOutput: 1\nExplanation: 0! is defined as 1.',
        '0 ≤ n ≤ 12',
        'def calculate_factorial(n):\n    # return the answer',
        '#include <iostream>\nusing namespace std;\n\nint calculate_factorial(int n) {\n    // return the answer\n}',
        'def calculate_factorial(n):\n    if n == 0:\n        return 1\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result',
        'int main() {\n    int n = 5;\n    cout << calculate_factorial(n) << endl;\n    n = 0;\n    cout << calculate_factorial(n) << endl;\n    return 0;\n}',
        'n = 5\nprint(calculate_factorial(n))\nn = 0\nprint(calculate_factorial(n))',
        'public class Solution {\n    public static int calculateFactorial(int n) {\n        // return the answer\n    }\n}',
        'public static void main(String[] args) {\n    int n = 5;\n    System.out.println(Solution.calculateFactorial(n));\n    n = 0;\n    System.out.println(Solution.calculateFactorial(n));\n}\n}'
    );
""")

    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases, constraints, boiler_code_python, boiler_code_cpp, testing_code, function_call_cpp, function_call_python, boiler_code_java, function_call_java)
    VALUES (
        'Palindrome Check',
        'You are given a string s. Your task is to determine whether s is a palindrome. A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward. Ignore spaces, punctuation, and capitalization.',
        'Test Case 1: Input: s = "racecar"\nOutput: True\nExplanation: "racecar" is a palindrome.\n\nTest Case 2: Input: s = "hello"\nOutput: False\nExplanation: "hello" is not a palindrome.',
        '1 ≤ len(s) ≤ 1000',
        'def is_palindrome(s):\n    # return the answer',
        '#include <iostream>\nusing namespace std;\n\nbool is_palindrome(string s) {\n    // return the answer\n}',
        'def is_palindrome(s):\n    s = s.lower().replace(" ", "").strip()\n    return s == s[::-1]',
        'int main() {\n    string s = "racecar";\n    cout << is_palindrome(s) << endl;\n    s = "hello";\n    cout << is_palindrome(s) << endl;\n    return 0;\n}',
        's = "racecar"\nprint(is_palindrome(s))\ns = "hello"\nprint(is_palindrome(s))',
        'public class Solution {\n    public static boolean isPalindrome(String s) {\n        // return the answer\n    }\n}',
        'public static void main(String[] args) {\n    String s = "racecar";\n    System.out.println(Solution.isPalindrome(s));\n    s = "hello";\n    System.out.println(Solution.isPalindrome(s));\n}\n}'
    );
""")

    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases, constraints, boiler_code_python, boiler_code_cpp, testing_code, function_call_cpp, function_call_python, boiler_code_java, function_call_java)
    VALUES (
        'Fibonacci Series',
        'You are given a single integer n (0 ≤ n ≤ 30). Your task is to generate the first n numbers in the Fibonacci sequence.',
        'Test Case 1: Input: n = 5\nOutput: [0, 1, 1, 2, 3]\nExplanation: The first 5 numbers in the Fibonacci sequence are [0, 1, 1, 2, 3].\n\nTest Case 2: Input: n = 8\nOutput: [0, 1, 1, 2, 3, 5, 8, 13]',
        '0 ≤ n ≤ 30',
        'def generate_fibonacci(n):\n    # return the answer',
        '#include <iostream>\n#include <vector>\nusing namespace std;\n\nvector<int> generate_fibonacci(int n) {\n    // return the answer\n}',
        'def generate_fibonacci(n):\n    fibonacci = [0, 1]\n    while len(fibonacci) < n:\n        next_number = fibonacci[-1] + fibonacci[-2]\n        fibonacci.append(next_number)\n    return fibonacci',
        'int main() {\n    int n = 5;\n    vector<int> result = generate_fibonacci(n);\n    for (int num : result) {\n        cout << num << " ";\n    }\n    cout << endl;\n    n = 8;\n    result = generate_fibonacci(n);\n    for (int num : result) {\n        cout << num << " ";\n    }\n    cout << endl;\n}',
        'n = 5\nresult = generate_fibonacci(n)\nfor num in result:\n    print(num, end=" ")\nn = 8\nresult = generate_fibonacci(n)\nfor num in result:\n    print(num, end=" ")',
        'import java.util.List;\nimport java.util.ArrayList;\n    public class Solution {\n    public static List<Integer> generateFibonacci(int n) {\n        // return the answer\n    }\n',
        'public static void main(String[] args) {\n    int n = 5;\n    List<Integer> result = Solution.generateFibonacci(n);\n    for (int num : result) {\n        System.out.print(num + " ");\n    }\n    System.out.println();\n    n = 8;\n    result = Solution.generateFibonacci(n);\n    for (int num : result) {\n        System.out.print(num + " ");\n    }\n    System.out.println();\n}\n}'
    );
""")

    return redirect('/') 

@app.route('/create_sample_python')
def create_sample_python():
    db.execute("""
    INSERT INTO python (problem_name, problem_description, test_cases, constraints, boiler_code_python, function_call_python, testing_code,negative_keywords)
VALUES (
    'The Quest for Truth : The Silent Mystery',
    "Once upon a time in a quaint little village, there lived a curious and imaginative child named Alex. Alex had heard tales of a mystical forest where the truth was said to be hidden among its many secrets. Determined to uncover this truth, Alex embarked on a journey deep into the heart of the forest.

As Alex ventured into the forest, various encounters tested the child's understanding of truth and falsehood. Here's how the story unfolds:

Scene 1: The Silent Mystery

Alex encountered a silent figure sitting by a tree. It was None. Curious, Alex asked, 'Are you a guardian of the forest's truth?' None remained silent, confirming the tales that None is considered False in the world of Python.
",
    'Test Case 1: Checking the Silent Mystery with None
mystery_value = None
Expected Output: True

Test Case 2: Checking with a non-None value
mystery_value = 5
Expected Output: False
',
    'Avoid using the == operator for comparisons.',
    'def check_mystery_value(mystery_value):
	# return True or False
', 
    'print(check_mystery_value(None))\nprint(check_mystery_value(5))',
    'def check_mystery_value(mystery_value):
	if mystery_value:
		return True
	else:
		return False
','==');""")
    db.execute("""
    INSERT INTO python (problem_name, problem_description, test_cases, constraints, boiler_code_python, function_call_python, testing_code,negative_keywords)
    VALUES (
        'The Quest for Truth : The Enigmatic Riddler',
        "Once upon a time in a quaint little village, there lived a curious and imaginative child named Alex. Alex had heard tales of a mystical forest where the truth was said to be hidden among its many secrets. Determined to uncover this truth, Alex embarked on a journey deep into the heart of the forest.

As Alex ventured into the forest, various encounters tested the child's understanding of truth and falsehood. Here's how the story unfolds:

Scene 2: The Enigmatic Riddler

Further along the path, Alex met a mysterious person who posed a riddle. 'I speak in riddles,' the person said. 'Is this statement true or false: ''I am the Riddler''?' It turned out that the Riddler's statement was False.
",
        'Test Case 1: Solving the Riddlers Statement
riddler_statement = "I am the Riddler"
Expected Output: True

Test Case 2: An Empty Riddle
riddler_statement = ""
Expected Output: False
',
        'Avoid using the == operator for comparisons.',
        'def check_riddler_statement(riddler_statement):
	# return True or False
', 
        'print(check_riddler_statement("I am the Riddler"))\nprint(check_riddler_statement(""))',
        'def check_riddler_statement(riddler_statement):
	if riddler_statement:
		return True
	else:
		return False
','==');""")
    db.execute("""
    INSERT INTO python (problem_name, problem_description, test_cases, constraints, boiler_code_python, function_call_python, testing_code,negative_keywords)
    VALUES (
        'The Quest for Truth : The Tale of the Null Wizard',
        "Once upon a time in a quaint little village, there lived a curious and imaginative child named Alex. Alex had heard tales of a mystical forest where the truth was said to be hidden among its many secrets. Determined to uncover this truth, Alex embarked on a journey deep into the heart of the forest.

As Alex ventured into the forest, various encounters tested the child's understanding of truth and falsehood. Here's how the story unfolds:

Scene 3: The Tale of the Null Wizard

In a clearing, Alex found an old book with a spell called 'Nullify.' When cast, it had a peculiar effect - it set things to 0. Alex cast the spell on a nearby object, turning it into 0.
",
        'Test Case 1: Casting the Nullify Spell
spell_result = 0
Expected Output: True

Test Case 2: A Different Spell Result
spell_result = 42
Expected Output: False
',
        'Avoid using the == operator for comparisons.',
        'def check_spell_result(spell_result):
	# return True or False
', 
        'print(check_spell_result(0))\nprint(check_spell_result(42))',
        'def check_spell_result(spell_result):
	if spell_result == 0:
		return True
	else:
		return False
','==');""")
    db.execute("""
    INSERT INTO python (problem_name, problem_description, test_cases, constraints, boiler_code_python, function_call_python, testing_code,negative_keywords)
    VALUES (
        'The Quest for Truth : The Ghostly Whisper',
        "Once upon a time in a quaint little village, there lived a curious and imaginative child named Alex. Alex had heard tales of a mystical forest where the truth was said to be hidden among its many secrets. Determined to uncover this truth, Alex embarked on a journey deep into the heart of the forest.

As Alex ventured into the forest, various encounters tested the child's understanding of truth and falsehood. Here's how the story unfolds:

Scene 4: The Ghostly Whisper

In a misty part of the forest, a voice echoed, 'I exist, but I'm empty.' It was an empty string, and it too was considered False in the forest of Python.
",
        'Test Case 1: The Ghostly Whisper Speaks
ghostly_whisper = ""
Expected Output: True

Test Case 2: Whispering Something
ghostly_whisper = "Whisper"
Expected Output: False
',
        'Avoid using the == operator for comparisons.',
        'def check_ghostly_whisper(ghostly_whisper):
	# return True or False
', 
        'print(check_ghostly_whisper(""))\nprint(check_ghostly_whisper("Whisper"))',
        'def check_ghostly_whisper(ghostly_whisper):
	if not ghostly_whisper:
		return True
	else:
		return False
','==');""")
    db.execute("""
    INSERT INTO python (problem_name, problem_description, test_cases, constraints, boiler_code_python, function_call_python, testing_code,negative_keywords)
    VALUES (
        'The Quest for Truth : The Guardian Trees',
        "Once upon a time in a quaint little village, there lived a curious and imaginative child named Alex. Alex had heard tales of a mystical forest where the truth was said to be hidden among its many secrets. Determined to uncover this truth, Alex embarked on a journey deep into the heart of the forest.

As Alex ventured into the forest, various encounters tested the child's understanding of truth and falsehood. Here's how the story unfolds:

Scene 5: The Guardian Trees

As Alex ventured deeper, they encountered two guardian trees. One was an empty list, and the other an empty dictionary. They stood silently, representing the emptiness that is considered False in the forest.
",
        'Test Case 1: The Silent Guardians
guardian_list = []
guardian_dict = {}
Expected Output: True

Test Case 2: The Active Guardians
guardian_list = [1, 2, 3]
guardian_dict = {"key": "value"}
Expected Output: False
',
        'Avoid using the == operator for comparisons.',
        'def check_guardian_trees(guardian_list, guardian_dict):
	# return True or False
', 
        'print(check_guardian_trees([], {}))\nprint(check_guardian_trees([1, 2, 3], {"key": "value"}))',
        'def check_guardian_trees(guardian_list, guardian_dict):
	if not guardian_list and not guardian_dict:
		return True
	else:
		return False
','==');""")

    return redirect('/index_python') 


@app.route('/problem/<problem_id>')
def problem_view(problem_id):
    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    return render_template('questions.html', problem_info=problem_info)

@app.route('/python_problem/<problem_id>')
def problem_view_python(problem_id):
    problem_info = db.execute("SELECT * from python WHERE problem_id = ?", problem_id)[0]
    return render_template('questions_python.html', problem_info=problem_info)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_code():
    code = request.form['code']
    problem_id = request.form['problem_id']
    lang = request.form['lang']
    type = request.form['type']

    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    boiler_code_cpp = problem_info['boiler_code_cpp']
    boiler_code_python = problem_info['boiler_code_python']
    boiler_code_java = problem_info['boiler_code_java']
    function_call_cpp = problem_info["function_call_cpp"]
    function_call_python = problem_info["function_call_python"]
    function_call_java = problem_info["function_call_java"]

    testing_code = problem_info["testing_code"]

    if code == boiler_code_python or code == boiler_code_cpp or code == boiler_code_java:
        response = {
            "testcase_passed": False,
            "result": "Please enter code.",
        }
        return jsonify(response)        

    # print(testing_code +"\n"+ function_call_python)
    try:
        if lang == "python":
            result,runtime = compile_python(code+"\n"+function_call_python)
        elif lang == "cpp":
            result,runtime = compile_cpp(code+"\n"+function_call_cpp)
        elif lang == "java":
            result,runtime = compile_java(code+"\n"+function_call_java)

        runtime = runtime * 1000  # Convert seconds to milliseconds and multiply by 1000
        runtime_formatted = "{:.2f}".format(runtime)  # Format to have 4 digits
        
        testcase_passed = False
        code = testing_code +"\n"+ function_call_python
        code = code.replace('\t', '    ')

        if type == "check":
            testing_code_result = subprocess.check_output(['python', '-c', testing_code +"\n"+ function_call_python], stderr=subprocess.STDOUT, text=True)
            testcase_passed = result.strip() == testing_code_result.strip()
        if runtime == 0:
            status = False
        else:
            status = True

        # Compare the results of the two executions
        # Return the result and testcase_passed as JSON
        response = {
            "testcase_passed": testcase_passed,
            "result": result,
            "status": status,
            "time" : runtime_formatted
        }
        return jsonify(response)
    except subprocess.CalledProcessError as e:
        response = {
            "testcase_passed": False,
            "result": f"There is an error in your code, please check again.\nError: {e.output}",
            "status": False
        }
        return jsonify(response)
    
@app.route('/check_python', methods=['POST'])
def check_python_code():
    code = request.form['code']
    problem_id = request.form['problem_id']
    lang = request.form['lang']
    type = request.form['type']

    problem_info = db.execute("SELECT * from python WHERE problem_id = ?", problem_id)[0]
    boiler_code_python = problem_info['boiler_code_python']
    function_call_python = problem_info["function_call_python"]

    testing_code = problem_info["testing_code"]

    if code == boiler_code_python:
        response = {
            "testcase_passed": False,
            "result": "Please enter code.",
        }
        return jsonify(response)        

    # print(code +"\n"+ function_call_python)
    try:
        if lang == "python":
            result,runtime = compile_python(code+"\n"+function_call_python)
        runtime = runtime * 1000  # Convert seconds to milliseconds and multiply by 1000
        runtime_formatted = "{:.2f}".format(runtime)  # Format to have 4 digits
        
        testcase_passed = False
        
        if type == "check":
            testing_code_result = subprocess.check_output(['python', '-c', testing_code +"\n"+ function_call_python], stderr=subprocess.STDOUT, text=True)
            testcase_passed = result.strip() == testing_code_result.strip()
        if runtime == 0:
            status = False
        else:
            status = True
        if problem_info["negative_keywords"] in code:
            result = f"Your code should not use {problem_info['negative_keywords']} in solution. \nOutput : \n{result}" 
        # Compare the results of the two executions
        # Return the result and testcase_passed as JSON
        response = {
            "testcase_passed": testcase_passed,
            "result": result,
            "status": status,
            "time" : runtime_formatted
        }
        return jsonify(response)
    except subprocess.CalledProcessError as e:
        response = {
            "testcase_passed": False,
            "result": f"There is an error in your code, please check again.\nError: {e.output}",
            "status": False
        }
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)