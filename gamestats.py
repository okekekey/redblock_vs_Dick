import os
from cryptography.fernet import Fernet


class GameStats():
    """Tracks the high score for red block vs dick."""
    
    def __init__(self) -> None:
        """Initializes high score and secret key"""
        # just to prevent an easy acces to a high_score file
        secret_key = b'sUCr1z2cA4T3Os4A2U8zXLJyXHEattYZ4ous4pdHfUg=' #Fernet.generate_key()
        self.cipher_suite = Fernet(secret_key)
        self.open_high_score()

    def save_high_score(self, settings):
        """Encrypts and writes to the file high score"""
        if settings.current_score > self.high_score:
            self.high_score = settings.current_score
            data = str(self.high_score)
            encrypted_scores = self.cipher_suite.encrypt(data.encode())
            with open('high_score.txt', 'w') as hs_file:
                hs_file.write(str(encrypted_scores))

    def open_high_score(self):
        """Open hs file or creates it"""
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as hs_file:
                encrypted_data = hs_file.read()
                encrypted_data = encrypted_data[2:-1] #in other way tokens dont match
                decrypted_scores = self.cipher_suite.decrypt(encrypted_data).decode()

                self.high_score = int(decrypted_scores)
        else:
            with open('high_score.txt', 'w') as hs_file:
                hs_file.write('0')
                self.high_score = 0

