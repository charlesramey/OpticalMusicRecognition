import matplotlib.pyplot as plt
from StaffDetector import StaffDetector
from myfunctions import get_input_im

# Load image
print("This is the right code being run")
filename = 'test1_cropped.png'
input_im = get_input_im(filename)

# Separate Staves
sd = StaffDetector(input_im)

# Display Images
plt.figure(dpi=200)
plt.imshow(sd.im_original, cmap='gray')

plt.figure(dpi=200)
plt.imshow(sd.im_staves, cmap='Greys')

plt.figure(dpi=200)
plt.imshow(sd.im_staves_expanded, cmap='Greys')

plt.figure(dpi=200)
plt.imshow(sd.im_staves_filled, cmap='Greys')
# plt.savefig('transcription_staff.jpg')

staves = sd.im_staves_separated

plt.figure(dpi=200)
for n in range(len(staves)):
    plt.subplot(len(staves),1,n+1)
    plt.imshow(staves[n],cmap = 'gray')
    # plt.axis('off')
# plt.savefig('transcription_staves.jpg')

plt.show()
