class Detector:
	def __init__(self, hostile_words, less_hostile_words):
		self.hostile_words = hostile_words
		self.less_hostile_words = less_hostile_words

	def detect(self, text):

		text_lower = text.lower()
		hostile_counts = {}
		less_hostile_counts = {}

		for w in self.hostile_words:
			count = text_lower.count(w.lower())
			if count > 0:
				hostile_counts[w] = count

		for w in self.less_hostile_words:
			count = text_lower.count(w.lower())
			if count > 0:
				less_hostile_counts[w] = count

		return {
			"hostile": hostile_counts,
			"less_hostile": less_hostile_counts
		}

