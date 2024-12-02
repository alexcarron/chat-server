import secrets

KEY_LENGTH = 128

def generate_session_key():
	return secrets.token_hex(KEY_LENGTH // 2)