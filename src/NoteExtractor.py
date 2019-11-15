import numpy as np


class NoteExtractor:

    # Constructor
    def __init__(self, staff=None, centroids=None, staff_height=None):
        self.staff_height = staff_height
        self.window_shape = self.get_window_shape(staff_height)
        self.staff = self.frame_staff(staff)
        self.centroids = self.adjust_centroids(centroids)
        self.notes = self.slice_notes(self.staff, self.centroids)

    def get_window_shape(self, staff_height):
        height = int(2*staff_height)
        width = int(0.45 * height)
        return height, width

    # Add whitespace to account for windows being out of bounds
    def frame_staff(self, staff):

        # Get new image shape
        old_shape = np.shape(np.array(staff))
        new_height = old_shape[0] + self.window_shape[0]
        new_width = old_shape[1] + self.window_shape[1]
        new_shape = (new_height, new_width)
        canvas = np.ones(new_shape, dtype=bool)

        # Copy image onto canvas
        for r in range(old_shape[0]):
            for c in range(old_shape[1]):
                y = int(r + self.window_shape[0]/2)
                x = int(c + self.window_shape[1]/2)
                canvas[y, x] = staff[r, c]

        return np.array(canvas)

    # Adjust centroids due to frame
    def adjust_centroids(self, centroids):

        centroids_adjusted = []
        for c in centroids:
            y = c[0] + int(self.window_shape[0]/2)
            x = c[1] + int(self.window_shape[1]/2)
            centroids_adjusted.append((y, x))

        return centroids_adjusted

    # Returns an array of note images all of the same shape
    def slice_notes(self, staff, centroids):

        notes = []
        for c in centroids:
            t_bound = int(c[0] - self.window_shape[0]/2)
            b_bound = int(t_bound + self.window_shape[0])
            l_bound = int(c[1] - self.window_shape[1]/2)
            r_bound = int(l_bound + self.window_shape[1])

            note = staff[t_bound:b_bound, l_bound:r_bound]
            notes.append(note)

        return notes
