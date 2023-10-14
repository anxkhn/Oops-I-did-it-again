from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/check', methods=['POST'])
def check_code():
    code = request.form['code']
    print(code)
    base = "n = 5\n"
    final = "\nsquare(n)"
    try:
        result = subprocess.check_output(['python', '-c', base + code + final], stderr=subprocess.STDOUT, text=True)
        code = """def square(n):
    total = 0
    for i in range(1, n + 1):
        total += i ** 2
    print(total)
"""
        result2 = subprocess.check_output(['python', '-c', base + code + final], stderr=subprocess.STDOUT, text=True)

        # Compare the results of the two executions
        testcase_passed = result.strip() == result2.strip()

        # Return the result and testcase_passed as JSON
        response = {
            "testcase_passed": testcase_passed,
            "result": result
        }
        return jsonify(response)
    except subprocess.CalledProcessError as e:
        return jsonify({
            "testcase_passed": False,
            "result": e.output
        })


if __name__ == '__main__':
    app.run(debug=True)