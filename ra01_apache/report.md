##Testing
![] (iactuallytestedthis-apache_setup.png)
~ I ran the apache setup in docker and requested localhost to get index.html. After that, I opened Firefox
and requested localhost to demonstrate it loaded index.html in both

##Questions
1) The traffic is TCP connections
2) When I followed the TCP stream, it gave me a new window with a request and all of the return content
3) The data can be read from the HTTP protocol, in which the HTML code, data type, data length etc. is returned
4) Since the TCP stream can be read, it is not encrypted
