class Note:
    
    # Constructor
    def __init__(self, pitch=0, duration=1, clef='treble', key=0, line=0, accidental=0, centroid=(0, 0), staff_indices=[]):
        
        # Primary variables, to be calculated later
        self.pitch = pitch
        self.duration = duration
        
        # Secondary variables, used to calculate pitch
        self.clef = clef
        self.key = key
        self.line = line
        self.accidental = accidental
        self.note_centroid = centroid
        self.staff_indices = staff_indices
    
    # Shift staff indices when array length reached
    def adjust_index(self, arr, mode):

        # Get shift amount
        shift = arr[0][0] - arr[len(arr)-1][0]
        output = []

        # Shift indices up on staff, which is down numerically
        if mode == 'up':
            for n in arr:
                a = n[0] - shift
                b = n[1] - shift
                output.append((a, b))
        # Shift indices down on staff, which is up numerically
        if mode == 'down':
            for n in arr:
                a = n[0] + shift
                b = n[1] + shift
                output.append((a, b))

        return output

    # Get line of note from centroid position
    def calculate_line(self):
        
        index = self.staff_indices.copy()
        
        # Get row of centroid
        r = self.note_centroid[0]
        line = 0

        print(r)

        i = 0
        # If centroid at line 0 or above
        if r < index[0][0]:
            while not r > index[i][1]:
                i += 1
                line += 1
                if i == 8:
                    i = 0
                    index = self.adjust_index(index, 'up')
                    
        # If centroid is below line 0
        else:
            while not r < index[i][0]:
                i -= 1
                line -= 1
                if i == -1:
                    i = 7
                    index = self.adjust_index(index, 'down')
                    
        self.line = line
    
    # Shifts line_notes in calculate_pitch based on detected key
    def key_shift(self, notes):
        
        # Local Variables
        key = self.key
        sharps = [1, 5, 2, 6, 3, 0, 4]  # Line indices in sharp order, treble clef
        flats = [4, 0, 3, 6, 2, 5, 1]   # Line indices in flat order, treble clef
        
        # Change key signature line location based on clef
        if self.clef == 'treble':
            pass
        elif self.clef == 'bass':
            sharps = [6, 3, 0, 4, 1, 5, 2]
            flats = [2, 5, 1, 4, 0, 3, 6]
        
        # Increment/Decrement line values based on key signature
        n = 0
        if key > 0:
            while n < key:
                notes[sharps[n]] += 1
                n += 1
        elif key < 0:
            key = abs(key)
            while n < key:
                notes[flats[n]] += 1
                n += 1
        
        return notes
            
    # Calculates pitch based on clef, key, and accidentals
    def calculate_pitch(self):
        
        # line_notes chooses a note based on the line its on.
        # index 0 is line 0, which is the bottom line of the staff
        # index 1 is line 1, which is the bottom space of the staff
        line_notes = []
        
        # Shift line notes based on clef
        if self.clef == 'treble':
            # In treble clef, the bottom line of the staff is an E
            # Since middle C is 0 and 2 lines below the staff,
            # and note E is 4 half steps up, E corresponds to the integer 4
            line_notes = [4, 5, 7, 9, 11, 12, 14]
        if self.clef == 'bass':
            # In bass clef, the bottom line of the staff is a G
            line_notes = [-17, -15, -13, -12, -10, -8, -7]
        
        # Accidentals override key_signature, so
        # adjust line notes based on key only if no accidentals are detected
        if self.accidental != 0:
            line_notes = self.key_shift(line_notes)
        
        # Get pitch based on line alone
        self.calculate_line()
        octave_shift = 0
        octave = 12
        line = self.line
        # If note is on or above staff
        if line >= 0:
            while line > 6:
                line -= 7
                octave_shift += 1
        # If note is below staff
        else:
            octave_shift = -1
            while line < -7:
                line += 7
                octave_shift -= 1
    
            line = (line+7) % 7
        
        # Get pitch based on line, modify based on octaves and accidentals
        line_pitch = line_notes[abs(line)] + (octave_shift * octave) + self.accidental
        self.pitch = line_pitch
