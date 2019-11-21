from myfunctions import get_input_im, notes2foxdot, preprocess
from StaffDetector import StaffDetector
from find_notes import find_notes
import matplotlib.pyplot as plt
from FoxDot import *
import NoteExtractor
import numpy as np
import joblib
import Note


def main():

    # Classes to foxdot durations
    duration_conv = {'eighth': 0.5, 'quarter': 1, 'half': 2, 'whole': 4}

    # Load note duration recognizer
    neural_net = joblib.load('new_scale.model')

    # Load image
    filename = 'test5.png'
    input_im = get_input_im(filename)

    # Separate Staves
    sd = StaffDetector(input_im)
    staves = sd.im_staves_subtracted_separated
    print("Staff detector ran successfully!")
    print()

    # Find notes from staves
    centroids = []
    im_notes = []
    print("Detecting notes...")
    for n in range(len(staves)):
        print("Iteration", n, "of", len(staves))
        # Find centroids
        dummy = find_notes(staves[n], min_r=10, max_r=15, thresh=0.5)
        centroids.append(dummy)

        # Note Extractor takes in an image of a staff, the staff height, and a list of note centroids. It returns
        # a list of images where each image is centered on the centroids specified.
        ne = NoteExtractor.NoteExtractor(staff=sd.im_staves_separated[n], centroids=dummy, staff_height=sd.staff_height-22)
        count = 0
        for note in ne.notes:
            count += 1
            if count < 0:
                plt.figure()
                plt.imshow(note)
                plt.show()
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
        plt.figure(1, dpi=200)
        plt.subplot(len(staves), 1, n+1)
        if n == 0:
            plt.title("Detected Centroids on Notes")
        plt.imshow(sd.im_staves_separated[n], cmap='gray')
        plt.axis('off')
        plt.scatter([r[1] for r in dummy], [c[0] for c in dummy], marker='.', color='r', s=[1 for n in dummy])

        # Plots centroids on the expanded staves
        # plt.figure(2, dpi=200)
        # plt.subplot(len(staves), 1, n+1)
        # if n == 0:
        #     plt.title("Detected Centroids on Expanded Staff")
        # plt.imshow(sd.im_staves_expanded_separated[n], cmap='Greys')
        # plt.axis('off')
        # plt.scatter([r[1] for r in dummy], [c[0] for c in dummy], marker='.', color='r', s=[1 for n in dummy])
    print()
    plt.show()

    # Check if all notes are the same shape
    shape = np.shape(im_notes[0])
    for note in im_notes:
        if np.shape(note) != shape:
            print("Different note image shape detected")

    # Select specific images and see how they are classified
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.imshow(im_notes[4])
    sample = preprocess(note)
    duration = neural_net.predict(sample.reshape(1, -1))
    plt.title(duration[0])

    plt.subplot(2, 2, 2)
    plt.imshow(im_notes[40])
    sample = preprocess(note)
    duration = neural_net.predict(sample.reshape(1, -1))
    plt.title(duration[0])

    plt.subplot(2, 2, 3)
    plt.imshow(im_notes[55])
    sample = preprocess(note)
    duration = neural_net.predict(sample.reshape(1, -1))
    plt.title(duration[0])

    plt.subplot(2, 2, 4)
    plt.imshow(im_notes[84])
    sample = preprocess(note)
    duration = neural_net.predict(sample.reshape(1, -1))
    plt.title(duration[0])
    plt.show()

    # Randomly select some images and see how they are classified
    shuffled = np.copy(im_notes)
    np.random.shuffle(shuffled)
    plt.figure(figsize=(7, 10), dpi=100)
    n = 0
    for note in shuffled:
        n += 1
        if n > 25:
            break
        plt.subplot(5, 5, n)
        plt.imshow(note, cmap='gray')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        sample = preprocess(note)
        duration = neural_net.predict(sample.reshape(1, -1))
        plt.title(duration[0])
    plt.show()

    plt.figure(figsize=(7, 10), dpi=100)
    n = 0
    for note in shuffled:
        n += 1
        if n > 25:
            break
        plt.subplot(5, 5, n)
        sample = preprocess(note)
        plt.imshow(sample.reshape((48, 21)), cmap='gray')
        plt.tick_params(
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False)  # labels along the bottom edge are off
        duration = neural_net.predict(sample.reshape(1, -1))
        plt.title(duration[0])
    plt.show()
    # Get note durations
    durations = []
    for note in im_notes:
        sample = preprocess(note)
        duration = neural_net.predict(sample.reshape(1, -1))
        durations.append(duration_conv[duration[0]])

    # Create notes
    notes = []
    for n in range(len(centroids)):
        for c in centroids[n]:
            note = Note.Note(centroid=c, staff_indices=sd.staff_indices[n])
            note.calculate_pitch()
            notes.append(note)

    # Print foxdot notes
    pitches, _ = notes2foxdot(notes)
    print("Pitches:  ", pitches)
    print("Durations:", durations)

    # Remove first two pitches and last pitch
    pitches = pitches[2:len(pitches)-1]

    # Play FoxDot pitches
    Scale.default = Scale.chromatic
    Clock.set_time(-1)
    Clock.set_tempo(260)
    p1 = Player()
    p1 >> keys(pitches)
    Go()


if __name__ == '__main__':
    main()