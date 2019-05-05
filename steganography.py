#!/usr/bin/python

# need PIL and stepic packages
import Image
import stepic

image1 = Image.open("nature.png")
steg = stepic.encode(image1, 'This is hidden text firoj')
# steg = stepic.encode(i, text)

steg.save("stegnofied.png", "PNG")

image2 = Image.open("stegnofied.png")
image2.show()

eimage = Image.open("stegnofied.png")
s = stepic.decode(eimage)
data = s.decode()
print data
