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
    problems = db.execute("SELECT * from problems")
    return render_template('index.html',problems=problems)

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
        'public class Solution {\n    public static List<Integer> generateFibonacci(int n) {\n        // return the answer\n    }\n}',
        'public static void main(String[] args) {\n    int n = 5;\n    List<Integer> result = Solution.generateFibonacci(n);\n    for (int num : result) {\n        System.out.print(num + " ");\n    }\n    System.out.println();\n    n = 8;\n    result = Solution.generateFibonacci(n);\n    for (int num : result) {\n        System.out.print(num + " ");\n    }\n    System.out.println();\n}\n}'
    );
""")

    return redirect('/') 


@app.route('/problems/<problem_id>')
def problem_view(problem_id):
    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    return render_template('questions.html', problem_info=problem_info)

@app.route('/test')
def test():
    return render_template('test.html')


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

if __name__ == '__main__':
    app.run(debug=True)