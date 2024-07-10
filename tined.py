
class Tuning:
    def __init__(self, tine_semitones):
        self.tine_semitones = tine_semitones
        self.tine_count = len(tine_semitones)
    def format(self, semitone):
        return str(self.note_for_semitone[semitone%12]) + str((semitone+9)//12 + 4)
