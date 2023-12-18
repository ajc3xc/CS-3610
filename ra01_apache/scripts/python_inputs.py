#!/usr/bin/python3

import cgi

print("Content-type: text/html\n\n")
print("Hello, World.")

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
arg1 = form.getvalue("arg1")
print("'arg1' was: " + arg1)
