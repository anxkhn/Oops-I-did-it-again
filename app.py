from flask import Flask, render_template, request, jsonify,redirect
from cs50 import SQL
from compiler import compile_python,compile_cpp
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
        boiler_code TEXT,
        testing_code TEXT,
        function_call_code TEXT
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
    
@app.route('/')
def index():
    unique_visits = db.execute("SELECT COUNT(DISTINCT ip_address) FROM request_logs")[0]['COUNT(DISTINCT ip_address)'] + 50
    problems = db.execute("SELECT * from problems")
    return render_template('index.html',problems=problems,unique_visits=unique_visits)

@app.route('/create_sample')
def create_sample():
    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases,constraints,boiler_code, testing_code, function_call_code)
VALUES (
    'Sum of Squares',
    'You are given a single integer n (1 ≤ n ≤ 1000) representing the range. Your task is to calculate the sum of squares of all positive integers from 1 to n inclusive. 
    
    Write a program to find this sum using the following formula: 
    
    Sum = 1² + 2² + 3² + ... + n²',
    'Test Case 1: 
    Input : n = 5
    Output: 55,
    Explanation: the first 5 positive integers (1² + 2² + 3² + 4² + 5²) which results in a sum of 55.

    Test Case 2: 
    Input : n = 8
    Output: 204',
    '1 ≤ n ≤ 1000',
    'def square(n):\n    # return the answer',
    'def square(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i ** 2\n    return total',
    'n = 5\n
print(square(n))\n
n = 8\n
print(square(n))'
);

""")
    db.execute("""INSERT INTO problems (problem_name, problem_description, test_cases, constraints, boiler_code, testing_code, function_call_code)
VALUES (
    'Sum of Integers',
    'You are given a single integer n (1 ≤ n ≤ 1000) representing the range. Your task is to calculate the sum of all positive integers from 1 to n inclusive. 
    
    Write a program to find this sum using the following formula: 
    
    Sum = 1 + 2 + 3 + ... + n',
    'Test Case 1: 
    Input: n = 5
    Output: 15
    Explanation: The sum of integers from 1 to 5 is 1 + 2 + 3 + 4 + 5, which results in a sum of 15.

    Test Case 2: 
    Input: n = 8
    Output: 36',
    '1 ≤ n ≤ 1000',
    'def calculate_sum(n):\n    # return the answer',
    'def calculate_sum(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total',
    'n = 5\n
print(calculate_sum(n))\n
n = 8\n
print(calculate_sum(n))'
);
""")
    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases,constraints,boiler_code, testing_code, function_call_code)
    VALUES (
        'Factorial Calculation',
        'You are given a single integer n (0 ≤ n ≤ 12) representing a non-negative integer. Your task is to calculate the factorial of n. The factorial of a non-negative integer n is the product of all positive integers less than or equal to n.',
        'Test Case 1: 
        Input: n = 5
        Output: 120
        Explanation: 5! = 5 * 4 * 3 * 2 * 1 = 120.
        
        Test Case 2: 
        Input: n = 0
        Output: 1
        Explanation: 0! is defined as 1.',
        '0 ≤ n ≤ 12',
        'def calculate_factorial(n):\n    # return the answer',
        'def calculate_factorial(n):\n    if n == 0:\n        return 1\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result',
        'n = 5\n
print(calculate_factorial(n))\n
n = 0\n
print(calculate_factorial(n))');
""")
    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases,constraints,boiler_code, testing_code, function_call_code)
    VALUES (
        'Palindrome Check',
        'You are given a string s. Your task is to determine whether s is a palindrome. A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward. Ignore spaces, punctuation, and capitalization.',
        'Test Case 1: 
        Input: s = "racecar"
        Output: True
        Explanation: "racecar" is a palindrome.
        
        Test Case 2: 
        Input: s = "hello"
        Output: False
        Explanation: "hello" is not a palindrome.',
        '1 ≤ len(s) ≤ 1000',
        'def is_palindrome(s):\n    # return the answer',
        'def is_palindrome(s):\n    s = s.lower().replace(" ", "").strip()\n    return s == s[::-1]',
        's = "racecar"\n
print(is_palindrome(s))\n
s = "hello"\n
print(is_palindrome(s))');
""")
    db.execute("""
    INSERT INTO problems (problem_name, problem_description, test_cases,constraints,boiler_code, testing_code, function_call_code)
    VALUES (
        'Fibonacci Series',
        'You are given a single integer n (0 ≤ n ≤ 30). Your task is to generate the first n numbers in the Fibonacci sequence.',
        'Test Case 1: 
        Input: n = 5
        Output: [0, 1, 1, 2, 3]
        Explanation: The first 5 numbers in the Fibonacci sequence are [0, 1, 1, 2, 3].
        
        Test Case 2: 
        Input: n = 8
        Output: [0, 1, 1, 2, 3, 5, 8, 13]',
        '0 ≤ n ≤ 30',
        'def generate_fibonacci(n):\n    # return the answer',
        'def generate_fibonacci(n):\n    fibonacci = [0, 1]\n    while len(fibonacci) < n:\n        next_number = fibonacci[-1] + fibonacci[-2]\n        fibonacci.append(next_number)\n    return fibonacci',
        'n = 5\n
print(generate_fibonacci(n))\n
n = 8\n
print(generate_fibonacci(n))');
""")

    return redirect('/') 


@app.route('/problems/<problem_id>')
def problem_view(problem_id):
    unique_visits = db.execute("SELECT COUNT(DISTINCT ip_address) FROM request_logs")[0]['COUNT(DISTINCT ip_address)'] + 50
    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    return render_template('questions.html',problem_info=problem_info,unique_visits=unique_visits)

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/check', methods=['POST'])
def check_code():
    code = request.form['code']
    problem_id = request.form['problem_id']
    lang = request.form['lang']
    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    boiler_code = problem_info['boiler_code']
    if code == boiler_code:
        response = {
            "testcase_passed": False,
            "result": "Please enter code.",
        }
        return jsonify(response)        

    final = problem_info["function_call_code"]
    code2 = problem_info["testing_code"]

    # print(code +"\n"+ final)
    try:
        if lang == "py":
            result,runtime = compile_python(code+"\n"+final)
        elif lang == "cpp":
            result,runtime = compile_cpp(code)
        print(result)
        runtime = runtime * 1000  # Convert seconds to milliseconds and multiply by 1000
        runtime_formatted = "{:.2f}".format(runtime)  # Format to have 4 digits
        result2 = subprocess.check_output(['python', '-c', code2 +"\n"+ final], stderr=subprocess.STDOUT, text=True)
        if runtime == 0:
            status = False
        else:
            status = True
        # Compare the results of the two executions
        testcase_passed = result.strip() == result2.strip()

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