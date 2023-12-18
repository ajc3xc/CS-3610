# Lab 4: ICMP Pinger Lab

In this lab, you will gain a better understanding of Internet Control Message Protocol (ICMP).
You will learn to implement a Ping application using ICMP request and reply messages.

Ping is a computer network application used to test whether a particular host is reachable across an IP network.
It is also used to self-test the network interface card of the computer or as a latency test.
It works by sending ICMP "echo replyg packets to the target host and listening for ICMP "echo reply" replies.
The "echo reply" is sometimes called a pong.
Ping measures the round-trip time, records packet loss, and prints a statistical summary of the echo reply packets received (the minimum, maximum, and the mean of the round-trip times and in some versions the standard deviation of the mean).

Your task is to develop your own Ping application in Python.
Your application will use ICMP but, in order to keep it simple, will not exactly follow the official specification in RFC 1739.
Note that you will only need to write the client side of the program, as the functionality needed on the server side is built into almost all operating systems.

You should complete the Ping application so that it sends ping requests to a specified host separated by approximately one second. Each message contains a payload of data that includes a timestamp.
After sending each packet, the application waits up to one second to receive a reply.
If one second goes by without a reply from the server, then the client assumes that either the ping packet or the pong packet was lost in the network (or that the server is down).

You will need to report the minimum, maximum, and average RTTs at the end of all pings from the client.
In addition, calculate the packet loss rate (in percentage).

## Code
Below you will find the skeleton code for the client. You are to complete the skeleton code. The places where you need to fill in code are marked with #Fill in start and #Fill in end . Each place may require one or more lines of code.

## Additional Notes
1. In "receiveOnePingg method, you need to receive the structure `ICMP_ECHO_REPLY` and fetch the information you need, such as checksum, sequence number, time to live (TTL), etc. Study the "sendOnePing" method before trying to complete the "receiveOnePing" method.
2. You do not need to be concerned about the checksum, as it is already given in the code.
3. This lab requires the use of raw sockets. In some operating systems, you may need administrator/root privileges to be able to run your Pinger program.
4. See the end of this programming exercise for more information on ICMP.  

## Testing the Pinger
First, test your client by sending packets to localhost, that is, 127.0.0.1. 
Then, you should see how your Pinger application communicates across the network by pinging servers in different continents.

## What to Hand in
You will hand in the complete client code and screenshots of your Pinger output for four target hosts, each on a different continent.

## Optional exercise
2. Your program can only detect timeouts in receiving ICMP echo responses.
Modify the Pinger program to parse the ICMP response error codes and display the corresponding error results to the user.
Examples of ICMP response error codes are 
0: Destination Network Unreachable, 
1: Destination Host Unreachable.

# Background
Internet Control Message Protocol (ICMP)

## Header
The ICMP header starts after bit 160 of the IP header (unless IP options are used).
* Type - ICMP type.
* Code - Subtype to the given ICMP type.
* Checksum - Error checking data calculated from the ICMP header + data, with value 0 for this field.
* ID - An ID value, should be returned in the case of echo reply.
* Sequence - A sequence value, should be returned in the case of echo reply.

## Echo Request
The echo request is an ICMP message whose data is expected to be received back in an echo reply ("pong").
The host must respond to all echo requests with an echo reply containing the exact data received in the request message.
* Type must be set to 8.
* Code must be set to 0.
* The Identifier and Sequence Number can be used by the client to match the reply with the request that caused the reply.
In practice, most Linux systems use a unique identifier for every ping process, and sequence number is an increasing number within that process.
Windows uses a fixed identifier, which varies between Windows versions, and a sequence number that is only reset at boot time.
* The data received by the echo request must be entirely included in the echo reply.

## Echo Reply
The echo reply is an ICMP message generated in response to an echo request, and is mandatory for all hosts and routers.
* Type and code must be set to 0.
* The identifier and sequence number can be used by the client to determine which echo requests e associated with the echo replies.
* The data received in the echo request must be entirely included in the echo reply.
