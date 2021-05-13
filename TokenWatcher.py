# -*- coding: windows-1250 -*-
import redis
from _datetime import datetime
from datetime import timedelta
from time import sleep
from math import inf

class token_watcher():

	clean_period = 60 #SECONDS
	session_token_life_time = 5 #MINUTES
	chat_token_life_time = 10 #MINUTES

	def __init__(self):
        redis_host='192.168.100.19'
        redis_port=6379
        
        self.r=redis.Redis(host=redis_host, 
                           port=redis_port,
                           decode_responses=True)
        
	def clean_daemon(self):
		while True:
			sleep(self.clean_period)

			self.clear_user_tokens
			self.clear_chat_tokens
			

	def clear_user_tokens(self):
		if(self.r.zcard('z_sessions_user')>0)
				session_time=(datetime.now()-timedelta(minutes=self.session_token_life_time)).strftime("%m%d%H%M%S")
				for token in self.r.zrangebyscore('z_sessions_user', -inf, session_time):
					self.r.hdel('h_tokens_user', token)

				self.r.zremrangebyscore('z_sessions_user', -inf, session_time)


	def clear_chat_tokens(self):
		if(self.r.zcard('z_sessions_chat')>0)
				chat_time=(datetime.now()-timedelta(minutes=self.chat_token_life_time)).strftime("%m%d%H%M%S")
				for token in self.r.zrangebyscore('z_sessions_chat', -inf, chat_time):
					self.r.hdel('h_tokens_chat', token)
					self.r.delete()

				self.r.zremrangebyscore('z_sessions_chat', -inf, chat_time)
