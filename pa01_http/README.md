# Programming assignment 1 (pa01)
Welcome to the World Wide Web (HTTP)

![](ithinkthereforeiam.png)

## Deliverables
* `web_server.py`
* `iactuallytestedthis-web_server.png`
* `client_browser.py`
* `iactuallytestedthis-client_browser.png`
* `report.md`

## Details
* Finish / fill in your python server `web_server.py`.
* Write the client `client_browser.py`.
* Include screenshots of you how you ran the code,
with your web browser and termials displaying the results.
* All source and text files should be utf-8 with Unix delimiters, written in Python3.

## Grading
Run the grade script via:
`bash grade.sh`

Open it to see what commands we run,
and run them yourself manually!

## Hints
* To debug your web server:
    1. Open Wireshark
    2. Open a browser, have it visit your server.
* To debug your web client:
    1. Open Wireshark
    2. Have it actually "visit" a real website.
* Only after debugging each with a known correct server/client,
should you test them against each other!
* Have fun!

## Part 1: You code a simple Web server
In this lab, you will learn the basics of socket programming for TCP connections in Python.
You will create a socket, bind it to a specific address and port, 
as well as send and receive HTTP packets.
You will also learn some basics of the HTTP header format.
You will develop a web server that handles client requests.
Your web server should:
* accept and parse the HTTP request, 
* get the requested file from the server's file system, 
* create an HTTP response message consisting of the requested file preceded by header lines, and then 
* send the response directly to the client.
* If the requested file is not present in the server, 
then the server should send an HTTP "404 Not Found" message back to the client.

### Code
Read the skeleton code for the Web server in the repository.
Complete the skeleton code.
The places where you need to fill in code are marked with `pass`.
Each place may require one or more lines of code.

### Running the Server
There are some an HTML files in the `web_files/` directory,
e.g., `hello_world.html`.
Run the server program.
Observe it's funtionality in a web browser.
To do so, visit this in the web browser:

`http://127.0.0.1:6789/hello_world.html`

Note also the use of the port number after the colon.
You need to replace this port number with whatever port you have used in the server code.
In the above example, we have used the port number 6789.
The browser should then display the contents of `hello_world.html`.
If you omit ":6789", the browser will assume port 80,
and you will get the web page from the server,
only if your server is listening at port 80.
Then change the url to get a file that is not present at the server. 
You should get a "404 Not Found" message, 
and return the 404 file.

This first part will get you some points,
independent of whether you complete the next section!

## Part 2: Multi-thread the server
Use multithreading on your server,
so that is capable of serving multiple requests simultaneously.
Using threading, first create a main thread in which your modified server listens for clients at a fixed port.
When it receives a TCP connection request from a client,
it will set up the TCP connection to service the client request in a separate thread.
There will be a separate TCP connection in a separate thread for each request/response pair.

## Part 3: You code a simple Web browser
Instead of using a browser,
write your own HTTP client to test your server,
and query various websites.
Your client will connect to the server using a TCP connection,
send an HTTP request to the server,
and display the server response as an output.
You can assume that the HTTP request sent is a GET method.
The client should take command line arguments,
specifying the server IP address or host name,
the port at which the server is listening,
and the path at which the requested object is stored at the server.
The following is an input command format to run the client.

`client_browser.py server_host server_port filename`

It should be able to work with real websites on the actual internet too!

## Part 4: write up
Write a `report.md` which includes:
* the above 2 screenshots, so that they are visible in the git-classses web interface, and 
* descriptions of each screenshot
* notes about your setup.
