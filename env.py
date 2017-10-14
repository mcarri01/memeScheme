class Environment:
	def __init__(self, env):
		self.env = env
	def addBind(self, var, val):
		self.env[var] = val
	def getVal(self, var):
		return self.env[var]
