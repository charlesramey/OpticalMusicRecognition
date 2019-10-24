import Note

#Takes an array of notes, returns arrays of pitches and durations
def notes2foxdot(notes):
    pitches = []
    durations = []
    
    for n in notes:
        pitches.append(n.pitch)
        durations.append(n.duration)
    
    return(pitches,durations)


#Make Notes
notes = []
for n in range(29):
    line = n - 9
    note = Note.Note(line = line,duration = 1)
    note.calculate_pitch()
    notes.append(note)

#Get pitches and durations
pitches,durations = notes2foxdot(notes)
print(pitches)
print(durations)