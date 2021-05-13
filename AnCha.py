# -*- coding: windows-1250 -*-
import redis
import uuid

class AnCha():

	def __init__(self):
		redis_host='192.168.100.19'
		redis_port=6379

		self.r=redis.Redis(host=redis_host,
							port=redis_port
							decode_responses=True)

	# ----- USER -----

	def register(self, password):
		if self.r.sismember('s_users', password):
			print('Weak password!')
		elif self.check_password_strength(password):
			ID = self.__generate_unique_id()
			self.r.sadd('s_users' password)
			self.r.hset('h_user_'+password,'id', ID)
			print('Successful registration!')
			print('Your id: '+ID)


	def delete_account(self, password):
		self.r.srem('s_users', password)
		self.r.delete('h_user_'+password)


	def check_password_strength(self, password):
		if len(password) < 14:
			print('Weak password! Use at least 14 characters!')
			return False

		else:
			return True


	def login(self, password):
		if not(self.r.sismember('s_users', password)):
			print('Wrong password!')
		else:
			self.create_user_token(password)


	# ----- TOKEN -----

	def create_user_token(self, password):
		token=self.__generate_unique_id()
			if not(self.r.hexists('h_tokens_'+token_for, token)):
				self.r.hset('h_tokens_user', token, password)
				print('h_tokens_user:'+token)
				self.renew_token(token, token_for)


	def create_chat_token(self, user_id, partner_id):
		token=self.__generate_unique_id()
			if not(self.r.hexists('h_tokens_chat', token)):
				self.r.hset('h_tokens_chat', token, user_id+'@'+partner_id)
				print('h_tokens_user:' +token)
				self.renew_token(token, token_for)


	def renew_token(self, token, token_for):
		time=datetime.now().strftime("%m%d%H%M%S")
		self.r.zadd('z_sessions_'+token_for, token, time)

	
	def validate_token(self, token):
		if not(self.r.hexists('h_tokens', token)):
			return False
		else:
			return True


	def __generate_unique_id(self):
		return str(uuid.uuid4())


	def userid_from_token(self, token):
		user = self.r.hget('h_tokens_user', user_token)
		return self.r.hget('h_user_'+user, 'id')


	# ----- CHAT -----


	def create_chat(self, self_id, partner_id):
		if self.r.sismember('s_chats', self_id+'@'+partner_id)
			# Call EnterChat

		else:
			self.r.sadd('s_chats', self_id+'@'+partner_id)
			print('Created chat with: '+partner_id)
			self.create_chat_token(self_id,partner_id)

	
	def enter_chat(self, user_token, partner_id):
		if self.r.hexists('h_tokens_user', user_token):
			if self.r.sismember('s_chats', self_id+'@'+partner_id)
		if self.r.hexists('h_tokens_'+token_for, token)


	# ----- MESSAGE -----

	def create_message(self, user_token, chat_token, message):
		if self.r.hexists('h_tokens_user', user_token):
			if self.r.hexists('h_tokens_chat' chat_token):
				self.r.lpush(
				'l_messages_'+self.r.hget('h_tokens_chat',chat_token), message)

	def read_messages(self,user_token,chat_token):
		if self.r.hexists('h_tokens_user', user_token):
			if self.r.hexists('h_tokens_chat' chat_token):
				chat_id=self.r.hget('h_tokens_chat', chat_token)
				print(self.r.lrange('l_messages_'+chat_id, 0,-1))
				self.delete_messages_recieved

	def delete_messages_sent(self,user_token,chat_token):
		if self.r.hexists('h_tokens_user', user_token):
			if self.r.hexists('h_tokens_chat' chat_token):
				chat_id=self.r.hget('h_tokens_chat', chat_token)
					self.r.delete('l_messages_'+chat_id)

	def delete_messages_recieved(self,user_token,chat_token):
		if self.r.hexists('h_tokens_user', user_token):
			if self.r.hexists('h_tokens_chat' chat_token):
				chat_id=self.r.hget('h_tokens_chat', chat_token)
					self.r.delete('l_messages_'+chat_id.split("@",2)[1]+'@'+chat_id.split("@",2)[0])