from utils.logger import Logger

logger = Logger.get_logger(service_name="ThreatDetectionService")

class Detector:
	def __init__(self, hostile_words, less_hostile_words):
		self.hostile_words = hostile_words
		self.less_hostile_words = less_hostile_words

	def count_hostile_words(self, text_lower):
		hostile_counts = {}
		for word in self.hostile_words:
			count = text_lower.count(word.lower())
			if count > 0:
				hostile_counts[word] = count
		return hostile_counts

	def count_less_hostile_words(self, text_lower):
		less_hostile_counts = {}
		for word in self.less_hostile_words:
			count = text_lower.count(word.lower())
			if count > 0:
				less_hostile_counts[word] = count
		return less_hostile_counts

	def calculate_threat_percentage(self, total_words, total_hostile_words, total_less_hostile_words):
		if total_words == 0:
			return 0.0		
		weighted_threat_words = (total_hostile_words * 2) + (total_less_hostile_words * 1)
		bds_percent = round((weighted_threat_words / total_words) * 100, 2)	
		return bds_percent

	def determine_threat_level(self, bds_percent):
		if bds_percent < 2:
			return "none"
		elif bds_percent <= 5:
			return "medium"
		else:
			return "high"

	def detect(self, text):	
		try:
			text_lower = text.lower()
			total_words = len(text_lower.split())			
			hostile_counts = self.count_hostile_words(text_lower)
			less_hostile_counts = self.count_less_hostile_words(text_lower)			
			total_hostile_words = sum(hostile_counts.values())
			total_less_hostile_words = sum(less_hostile_counts.values())
			bds_percent = self.calculate_threat_percentage(total_words, total_hostile_words, total_less_hostile_words)
			bds_threat_level = self.determine_threat_level(bds_percent)
			logger.info(f"Detection result Level: {bds_threat_level}, Percent: {bds_percent}%")
			return {
				"bds_threat_level": bds_threat_level,
				"bds_percent": bds_percent,
				"is_bds": bds_threat_level != "none",
			}			
		except Exception as e:
			logger.error(f"Error in threat detection: {e}")
			raise  



