Eduardo Santín
CCOM 4205
Project 1 - Application Layer
 
Assignment 1: Web Server
This is a simple tcp webserver that can serve simple html files to a browser. It can also handle 404 errors if the file is not found.

    Requirements:
    1.python3
    2.basic html file(included in the repository, named helloworld.html)

    How to run:
    1. Open a terminal and navigate to the directory where the files are located.

    2. Run the command: python3 server.py
        a.I assigned it to port 8080 due to port 80 giving me issues

    3. Open a browser and type in the url: localhost:8080/helloworld.html
        a. If you want to see the 404 error, type in the url: localhost:8080/404.html, or any other file that is not in the directory

Assignment 4: Web Proxy
This is a simple tcp proxy server that handles http requests from a client, searches the same request to a server, caches it and serves it back to the client. At the time it only can fetch simple html files. What I used to test this proxy was the site: http://httpforever.com/

    Requirements:
    1.python3
    2.browser with proxy settings set to localhost and port 12000

    How to run:
    1. Open a terminal and navigate to the directory where the files are located.
    2. Run the command: python3 proxy.py localhost
    3. Open a browser and type in a url that is http://, for example: http://httpforever.com/

    Comments:
    1. When opening firefox will running the proxy sometimes,
        it will request canonical html from firefox and will crash the proxy.
        I am not sure if this is a part of the assignment but the browser seems to be sending this request and it is causing the proxy to crash.
        
        1.1 I implemented a quick fix to this issue at last minute
        and it seems to be working.

    2. 