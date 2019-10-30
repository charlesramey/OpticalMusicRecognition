import matplotlib.pyplot as plt
from find_notes import find_notes
import Note
from StaffDetector import StaffDetector
from myfunctions import get_input_im, notes2foxdot
from FoxDot import *

# Load image
filename = 'test4.png'
input_im = get_input_im(filename)

# Separate Staves
sd = StaffDetector(input_im)
staves = sd.im_staves_separated

# Find notes from staves
centroids = []
for n in range(len(staves)):
    # Find centroids
    dummy = find_notes(staves[n], min_r=10, max_r=15, thresh=0.85)
    centroids.append(dummy)

    # Plot centroids
    plt.figure(1, dpi=500)
    plt.subplot(len(staves), 1, n+1)
    if n == 0:
        plt.title("Detected Centroids on Notes")
    plt.imshow(staves[n], cmap='gray')
    plt.axis('off')
    plt.scatter([r[1] for r in dummy], [c[0] for c in dummy], marker='.', color='r', s=[3 for n in dummy])

    plt.figure(2, dpi=500)
    plt.subplot(len(staves), 1, n+1)
    if n == 0:
        plt.title("Detected Centroids on Expanded Staff")
    plt.imshow(sd.im_staves_expanded_separated[n], cmap='Greys')
    plt.axis('off')
    plt.scatter([r[1] for r in dummy], [c[0] for c in dummy], marker='.', color='r', s=[1 for n in dummy])

plt.figure(1, dpi=500)
plt.savefig('test4_centroids_original.png')
plt.figure(2, dpi=500)
plt.savefig('test4_centroids_staves.png')
plt.show()

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

'''
# Play FoxDot pitches
Scale.default = Scale.chromatic
p1 = Player()
p1 >> keys(pitches)
Clock.set_time(-1)
Go()
'''

'''
# Display Images
plt.figure(dpi=200)
plt.imshow(sd.im_original, cmap='gray')

plt.figure(dpi=200)
plt.imshow(sd.im_staves, cmap='Greys')

plt.figure(dpi=200)
plt.imshow(sd.im_staves_expanded, cmap='Greys')

plt.figure(dpi=200)
plt.imshow(sd.im_staves_filled, cmap='Greys')

staves = sd.im_staves_separated

plt.figure(dpi=200)
for n in range(len(staves)):
    plt.subplot(len(staves),1,n+1)
    plt.imshow(staves[n], cmap='gray')

plt.show()
'''




