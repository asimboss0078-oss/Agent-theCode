import random

class APIKeyManager:
    def __init__(self, token_csv):
        self.tokens = token_csv.split(',') if token_csv else []

    def get_token(self):
        return random.choice(self.tokens) if self.tokens else None

    def add_key(self, key):
        self.tokens.append(key)

    def list_keys(self):
        return self.tokens
