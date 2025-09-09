import base64

def decode_base64_list(encoded_str):
	decoded = base64.b64decode(encoded_str).decode('utf-8')
	return [word.strip() for word in decoded.split(',')]
