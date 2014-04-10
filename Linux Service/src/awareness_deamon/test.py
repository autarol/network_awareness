import json
import socket
import config

ip = config.host
port = config.port

def test_login():
	d={'type':'auth','user':'app','password':'app','pid':123}
	message = json.dumps(d)
	print "Sent: {}".format(message)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip, port))
	sock.sendall(message)
	response = sock.recv(1024)
	print "Received: {}".format(response)
	sock.close()

def test_push():
	
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, port))
	except Exception,e:
		print e, "Connection Failed"
	try:
		d={'type':'auth','user':'app','password':'app','pid':123}
		message = json.dumps(d)
		print "Sent: {}".format(message)
		sock.sendall(message)
		response = sock.recv(1024)
		print "Received: {}".format(response)

		d={'type':'push','pid':123,'data':"M:10.0.1.2,R:10.0.1.3,WL:300"}
		print "Sent: {}".format(d)
		message = json.dumps(d)
		sock.sendall(message)
		response = sock.recv(1024)
		print "Received: {}".format(response)
	finally:
		sock.close()	

