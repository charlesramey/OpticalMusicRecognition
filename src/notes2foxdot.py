import Note
import matplotlib.pyplot as plt
import numpy as np
from StaffDetector import StaffDetector
from myfunctions import get_input_im
from find_notes import find_notes


# Takes an array of notes, returns arrays of pitches and durations
def notes2foxdot(notes):
    pitches = []
    durations = []
    
    for n in notes:
        pitches.append(n.pitch)
        durations.append(n.duration)
    
    return pitches, durations


# Load image
filename = 'test1.jpg'
input_im = get_input_im(filename)

# Process image
sd = StaffDetector(input_im)
top_line = sd.im_staves_separated[0]
centroids = find_notes(top_line)
print(centroids)

# Add centroids to staff
staff = sd.im_staves_expanded_separated[0]
staff = np.where(staff == 0, 255, 0)
staff_rgb = np.stack([staff, staff, staff], axis=-1)
for c in centroids:
    staff_rgb[c[0]-1, c[1]-1] = [255, 0, 0]
    staff_rgb[c[0]-1, c[1]+0] = [255, 0, 0]
    staff_rgb[c[0]-1, c[1]+1] = [255, 0, 0]
    staff_rgb[c[0]+0, c[1]-1] = [255, 0, 0]
    staff_rgb[c[0]+0, c[1]+0] = [255, 0, 0]
    staff_rgb[c[0]+0, c[1]+1] = [255, 0, 0]
    staff_rgb[c[0]+1, c[1]-1] = [255, 0, 0]
    staff_rgb[c[0]+1, c[1]+0] = [255, 0, 0]
    staff_rgb[c[0]+1, c[1]+1] = [255, 0, 0]

# Create notes
notes = []
for c in centroids:
    note = Note.Note(centroid=c, staff_indices=sd.staff_indices[0])
    note.calculate_pitch()
    notes.append(note)

pitches, durations = notes2foxdot(notes)
print(pitches)
print(durations)

# Display staff with fabricated centroids
plt.figure(dpi=200)
plt.imshow(staff_rgb)
plt.show()
