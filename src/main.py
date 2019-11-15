import matplotlib.pyplot as plt
from find_notes import find_notes
import Note
import NoteExtractor
from StaffDetector import StaffDetector
from myfunctions import get_input_im, notes2foxdot
from FoxDot import *
import numpy as np

# Load image
filename = 'test4.png'
input_im = get_input_im(filename)

# Separate Staves
sd = StaffDetector(input_im)
staves = sd.im_staves_subtracted_separated

# Find notes from staves
centroids = []
im_notes = []
for n in range(len(staves)):
    # Find centroids
    dummy = find_notes(staves[n], min_r=10, max_r=15, thresh=0.5)
    centroids.append(dummy)

    # Note Extractor takes in an image of a staff, the staff height, and a list of note centroids. It returns a list of
    # images where each image is centered on the centroids specified.
    ne = NoteExtractor.NoteExtractor(staff=sd.im_staves_separated[n], centroids=dummy, staff_height=sd.staff_height)
    for note in ne.notes:
        im_notes.append(note)

    # Uncomment these to view plots

    # Plots the "notes" extracted from each staff
    # c = 0
    # plt.figure(dpi=200)
    # for note in ne.notes:
    #     c += 1
    #     im_notes.append(note)
    #     plt.subplot(4, 4, c)
    #     plt.imshow(note, cmap='gray')

    # Plots centroids on the actual image
    # plt.figure(1, dpi=200)
    # plt.subplot(len(staves), 1, n+1)
    # if n == 0:
    #     plt.title("Detected Centroids on Notes")
    # plt.imshow(sd.im_staves_separated[n], cmap='gray')
    # plt.axis('off')
    # plt.scatter([r[1] for r in dummy], [c[0] for c in dummy], marker='.', color='r', s=[1 for n in dummy])

    # Plots centroids on the expanded staves
    # plt.figure(2, dpi=200)
    # plt.subplot(len(staves), 1, n+1)
    # if n == 0:
    #     plt.title("Detected Centroids on Expanded Staff")
    # plt.imshow(sd.im_staves_expanded_separated[n], cmap='Greys')
    # plt.axis('off')
    # plt.scatter([r[1] for r in dummy], [c[0] for c in dummy], marker='.', color='r', s=[1 for n in dummy])
plt.show()

# Check if all notes are the same shape
shape = np.shape(im_notes[0])
for note in im_notes:
    if np.shape(note) != shape:
        print("Different note image shape detected")

# Create notes
notes = []
for n in range(len(centroids)):
    for c in centroids[n]:
        note = Note.Note(centroid=c, staff_indices=sd.staff_indices[n])
        note.calculate_pitch()
        notes.append(note)

# Print foxdot notes
pitches, durations = notes2foxdot(notes)
print("Pitches:", pitches)

# Remove first two pitches and last pitch
pitches = pitches[2:len(pitches)-1]

# Play FoxDot pitches
Scale.default = Scale.chromatic
Clock.set_time(-1)
Clock.set_tempo(260)
p1 = Player()
p1 >> keys(pitches)
Go()


