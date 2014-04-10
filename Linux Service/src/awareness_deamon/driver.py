#!/usr/bin/python
import redis
import config
import json
import logger

r = redis.StrictRedis(host=config.redis['host'], port=config.redis['port'], db=0)

class NotLoggedException(Exception):pass

def program_cleanup():
	print "Service Going Down"
	return 0

#TODO Change name
def reload_service_config():
	pass

def parse_msg(msg):
	'''
		Entry point for incoming messages
	'''
	response = False
	try:
		msg= json.loads(msg)
		if msg['type'] == 'auth':
			if authenticate_application(msg['user'], msg['password']):
				if session_exists(msg['pid']):
					app_session_end(msg['pid'])
				response = app_session_start(msg['pid'])
			else:
				response = {'type':'response','result':False}

		if msg['type'] == 'push':
			'''TODO Check Capabilities of Controller'''
			if is_logged(msg['pid']):
				prepare_envelope_controller(msg['pid'],msg['data'])
				response = True
			else:
				raise NotLoggedException("App %s is not logged in"% msg["pid"] )

		
	except Exception,e:
		print e
		logger.log(e)
	finally:
		return json.dumps(response)
		
def session_exists(pid):
	return is_logged(pid) & r.lrange('%s.messages'%pid) > 0

def app_session_start(pid):
	r.set('%s.logged'%pid,True)
	r.rpush('%s.messages'%pid,'START')
	return {'type':'response','result':True}

def app_session_end(pid):
	r.delete('%s.logged'%pid)
	while r.lrange('%s.messages'%pid) > 0:
		r.rpop('%s.messages'%pid)

def is_logged(pid):
	if r.get('%s.logged'%pid):
		return True
	else:
		return False

def authenticate_application(u,p):
	return True if u == 'app' and p == 'app' else False

def prepare_envelope_controller(pid, data):
	r.rpush('%s.messages'%pid,data)