"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def multiply(*args):
  """
  Returns a string with the result of the multiplication of the arguments
  """
  a = int(args[0])
  b = int(args[1])
  multiple = a*b
  return str(multiple)

def add(*args):
  """ Returns a STRING with the sum of the arguments """

  a = int(args[0])
  b = int(args[1])
  cal_sum = a + b
  return str(cal_sum)

def subtract(*args):
  """
  Returns a string with the subtraction result of the arguments
  """
  a = int(args[0])
  b = int(args[1])
  difference = a - b
  return str(difference)

def divide(*args):
  """
  Returns a string with the division result of the arguments
  """
  a = int(args[0])
  b = int(args[1])
  quotient = a/b
  return str(quotient)

def instructions():
  """
  Instructions for using the calculator application
  """
  instruction = """<html>
<head>
<title>WSGI Calculator</title>
</head>

<i>UW Python Certificate - py230</i><br>
<i>Assignment 4 - WSGI Calculator</i><br>
<i>Student: Michael List</i><br>

<h1>WSGI Calculator</h1>
<body>
<p>This simple WSGI web app allows the user to add, subtract, multiply and divide numbers provided in the URL</p>
<p>For example, if you open a browser at `http://localhost:8080/multiple/3/5' then the response
body in the browser will be `15`.</p>
<br>
<h2>URLs</h2>
<ul>
<li>Multiplication: http://localhost:8080/multiply/</li>
<li>Addition: http://localhost:8080/add/</li>
<li>Substraction: http://localhost:8080/subtract/</li>
<li>Division: http://localhost:8080/divide/</li>
</ul>
<h2>Examples</h2>
<ul>
  <li>http://localhost:8080/multiply/3/5   => 15</li>
  <li>http://localhost:8080/add/23/42      => 65</li>
  <li>http://localhost:8080/subtract/23/42 => -19</li>
  <li>http://localhost:8080/divide/22/11   => 2</li>
</ul>
</body>
</html>

  """
  return instruction

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': instructions,
        'add': add,
        'subtract': subtract,
        'divide': divide,
        'multiply': multiply
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    '''
    Your application code from the book database
    work here as well! Remember that your application must
    invoke start_response(status, headers) and also return
    the body of the response in BYTE encoding.

    (bonus): Add error handling for a user attempting
    to divide by zero.
    '''
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
          raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
