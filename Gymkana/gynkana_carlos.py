import http.client
import socket
import struct

import ast
import operator as op

import _thread
import sys
import os

#THIS CODE IS TAKEN FROM 'J.F Sebastian' at STACKOVERFLOW.COM (line 10 to 36)

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

def solving(operation):
    return solve(ast.parse(operation, mode='eval').body)


def solve(operation):
    if (isinstance(operation, ast.Num)):
        return operation.n

    if (isinstance(operation, ast.BinOp)):
        left = solve(operation.left)
        right = solve(operation.right)

    if isinstance(operation.op, ast.Add):
        return left + right

    elif isinstance(operation.op, ast.Sub):
        return left - right

    elif isinstance(operation.op, ast.Mult):
        return left * right

    elif isinstance(operation.op, ast.Div):
        return left // right

def replace(function):
    print(function)
    function = function.replace('[', '(')
    function = function.replace(']', ')')
    function = function.replace('{', '(')
    function = function.replace('}', ')')
    return function

# Code author: David Villa Alises
def cksum(data):
    def sum16(data):
        "sum all the the 16-bit words in data"
        if len(data) % 2:
            data += b'\0'

        return sum(struct.unpack("!%sH" % (len(data) // 2), data))

    retval = sum16(data)  # sum
    retval = sum16(struct.pack('!L', retval))  # one's complement sum
    retval = (retval & 0xFFFF) ^ 0xFFFF  # one's complement
    return retval

server = 'atclab.esi.uclm.es'

def phase0():

    sock0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock0.connect((server, 2000))
    msg0 = (sock0.recv(1024)).decode('utf-8')

    print(msg0)
    sock0.close()
    result0 = msg0.split()[0]
    return result0

def phase1(message):

    UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPserver.bind(('', 2022))

    msg1 = message + ' 2022'

    UDPserver.sendto(msg1.encode('utf-8'), (server, 2000))
    #UDPserver.recv(1024).decode('utf-8')
    msg2 = (UDPserver.recv(1024)).decode('utf-8')
    UDPserver.close

    print(msg2)
    result1 = msg2.split()[0]
    return result1

def phase2(message):

    TCPport = int(message)
    TCPServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPServer.connect((server, TCPport))
    finished_operations = False

    while finished_operations == False:
        operation = TCPServer.recv(4096).decode('utf-8')
        operation = replace(operation)

        if operation.count('(') == operation.count(')'):
            if operation[0] == '(':
                result = ('(' + str(solving(operation)) + ')')
                print(result)
                TCPServer.send(result.encode())
        else:
            operation += TCPServer.recv(64).decode('utf-8')
            operation = replace(operation)
            if operation[0] == '(':
                result = ('(' + str(solving(operation)) + ')')
                print(result)
                TCPServer.send(result.encode())
            else:
                break
        if operation[0] != '(':
            finished_operations = True

    TCPServer.close()
    print(operation)
    msg3 = operation.split()[0]
    return msg3

def phase3(message):

    http_sock = http.client.HTTPConnection(server, 5000)
    http_sock.request("GET", "/" + str(message))
    response = http_sock.getresponse()

    reading = response.read()
    http_sol = str(reading.decode())
    print(http_sol)
    http_sock.close()
    msg4 = http_sol.split()[0]
    return msg4

def phase4(message):
    import time
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))

    header=struct.pack('!bbHhh',8,0,0,3669,5) #1110  y el 1 numero que yo quiera
    timestamp=struct.pack('!d',time.time())
    checksum=cksum(header+timestamp+message.encode())
    packett=struct.pack('!bbHhh',8,0,checksum,3669,5)+timestamp+message.encode()
    sock.sendto(packett,('atclab.esi.uclm.es',80))
    sock.recv(2048)
    identificador=(sock.recv(2048)[36:]).decode()

    print(identificador)

    iden=identificador.split("\n")[0]
    return iden

#Main execution
print('Gymmkana, Álvaro Ángel-Moreno Pinilla. 2º A group\n')
print('Connection step:')
result = phase0()
print('Step 1:')
result = phase1(result)
print('Step 2:')
result = phase2(result)
print('Step 3:')
result = phase3(result)
print('Step 4:')
result = phase4(result)
print('Step 5:')
#phase5(result)
