class GameTimer:
	def __init__(self, minute, second):
		self.start = "0{}:00".format(minute)
		self.minute = minute
		self.second = second

	def RunMinutes(self):
		if self.minute > 0:
			self.minute -= 1

	def RunSeconds(self):
		if self.second > 0:
			self.second -= 1
		elif self.second == 0 and self.minute > 0:
			self.RunMinutes()
			self.second = 59