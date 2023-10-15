from flask import Flask, render_template, request, jsonify,redirect
from cs50 import SQL
import subprocess


app = Flask(__name__)
db = SQL("sqlite:///problems.db")

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


@app.route('/')
def index():
    return render_template('index.html')

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
    'Constraints: 1 ≤ n ≤ 1000',
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
    'Constraints: 1 ≤ n ≤ 1000',
    'def calculate_sum(n):\n    # return the answer',
    'def calculate_sum(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total',
    'n = 5\n
print(calculate_sum(n))\n
n = 8\n
print(calculate_sum(n))'
);
""")
    return redirect('/1') 


@app.route('/<problem_id>')
def problem_view(problem_id):
    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    return render_template('index.html',problem_info=problem_info)

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/check/<problem_id>', methods=['POST'])
def check_code(problem_id):
    code = request.form['code']
    problem_info = db.execute("SELECT * from problems WHERE problem_id = ?", problem_id)[0]
    boiler_code = problem_info['boiler_code']
    if code == boiler_code:
        response = {
            "testcase_passed": False,
            "result": "Please enter code."
        }
        return jsonify(response)        

    final = problem_info["function_call_code"]
    code2 = problem_info["testing_code"]

    try:
        result = subprocess.check_output(['python', '-c', code +"\n"+ final], stderr=subprocess.STDOUT, text=True)
        result2 = subprocess.check_output(['python', '-c', code2 +"\n"+ final], stderr=subprocess.STDOUT, text=True)

        # Compare the results of the two executions
        testcase_passed = result.strip() == result2.strip()

        # Return the result and testcase_passed as JSON
        response = {
            "testcase_passed": testcase_passed,
            "result": result
        }
        return jsonify(response)
    except subprocess.CalledProcessError as e:
        response = {
            "testcase_passed": False,
            "result": f"There is an error in your code, please check again.\nError: {e.output}"
        }
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)