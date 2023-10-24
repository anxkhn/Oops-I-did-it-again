# Oops I Did It Again

**Summary:**

Welcome to 'Oops I Did It Again,' a project dedicated to helping Python developers overcome non-Pythonic coding habits and write code that adheres to PEP 8 best practices. If you ever find yourself slipping into C++-like syntax when writing Python code, you're not alone. The project's goal is simple: to guide you in writing Python code that is clean, readable, and truly Pythonic. Whether you're a Python beginner or a seasoned developer, you'll find valuable insights here.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run this project, you will need to have the following software installed on your machine:

1. **Python3**: You can download and install Python3 from the official website:
  
  - [Python3](https://www.python.org/downloads/)
2. **Java Development Kit (JDK)**: If you plan to work with Java code, you will need to have the Java Development Kit installed. You can download and install the JDK from the official Oracle website or use OpenJDK:
  
  - [Official Oracle JDK](https://www.oracle.com/java/technologies/javase-downloads.html)
  - [OpenJDK](https://openjdk.java.net/)
3. **C++ Compiler**: For working with C++ code, you will need a C++ compiler. If you're on a Linux-based system, you may already have g++ installed. On Windows, you can use MinGW or Microsoft Visual C++.
  
  - [MinGW for Windows](http://www.mingw.org/)
  - [Microsoft Visual C++](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
4. **pip (Python's package manager)**: If you don't already have pip installed with Python3, you can refer to the [official pip installation guide](https://pip.pypa.io/en/stable/installing/) for installation instructions.
  

You will also need to have Flask and flask_sqlalchemy packages installed to run this application. These will be installed as part of the project's requirements, as mentioned in the "Installing" section in the README.

### Installing

1. Clone the repository to your local machine
  
  ```
  git clone https://github.com/anxkhn/Oops-I-did-it-again.git
  ```
  
2. Navigate to the project directory
  
  ```
  cd Oops-I-did-it-again
  ```
  
3. Install the necessary packages
  
  ```
  pip install -r requirements.txt
  ```
  
4. Start the application
  
  ```
  flask run
  ```
  

The application will now be running on `http://127.0.0.1:5000`

## Deployment

This app is intended to be deployed on a web server. You can use [PythonAnywhere](https://www.pythonanywhere.com) to deploy this application.

## Built With

- [Flask](https://flask.palletsprojects.com/) - A microframework for Python web applications
- [CS50](https://github.com/cs50/python-cs50) - Harvard CS50's library for Python
- [CodeMirror](https://codemirror.net/) - A versatile text editor implemented in JavaScript for browser-based code editing.
- [Material Bootstrap](https://fezvrasta.github.io/bootstrap-material-design/) - A Material Design theme for Bootstrap, providing a modern and clean user interface.
- [Werkzeug](http://werkzeug.pocoo.org/) - A Flask framework that implements WSGI for handling requests.
- [Jinja2](http://jinja.pocoo.org/docs/2.10/) - A templating language for Python, used by Flask.

Additionally, you will need the `compilers` library for Python, C++, and Java installed on your machine, as well as some other libraries (prebuilt) like `subprocess`, `time`, and `os`.

## Contributing

To contribute to the project, please follow the [CONTRIBUTING](https://github.com/anxkhn/codeclip/blob/master/CONTRIBUTING.md) guidelines.

## Author

- **[Anas Khan](https://github.com/anxkhn)**

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/anxkhn/codeclip/blob/master/LICENSE) file for details.