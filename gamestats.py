import os

class GameStats():
    """Track statistics for red block vs dick."""

    def __init__(self) -> None:
        """Initialize statistics."""
        self.open_high_score()
    
    
    def open_high_score(self):
        """Open hs file or creates it"""
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as hs_file:
                self.high_score = hs_file.read()
                self.high_score = int(self.high_score)
        else:
            with open('high_score.txt', 'w') as hs_file:
                hs_file.write('0')
                self.high_score = 0

    def save_high_score(self, settings):
        """Writes high score to the file if it is over current score"""
        if settings.current_score > self.high_score:
            self.high_score = settings.current_score
            with open('high_score.txt', 'w') as hs_file:
                hs_file.write(str(self.high_score))
                #print(type(self.high_score), self.high_score)
        