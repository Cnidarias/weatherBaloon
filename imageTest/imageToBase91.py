import io
import base91
from PIL import Image

def main():
   filename = "Mobius/IMAG0888.JPG"
   img  = Image.open(filename, mode='r')
   img.thumbnail((320, 240), Image.ANTIALIAS)
   img = img.convert('L')


   outputCompressed = io.BytesIO()
   img.save(outputCompressed, format='jpeg', optimize=True, quality=50)
   img.save("testImageCompressed.jpg", format='jpeg', optimize=True, quality=50)
   dataCompressed = outputCompressed.getvalue()
   resCompressed = base91.encode(dataCompressed)
   resCompressed += "__END"

   outputNormal = io.BytesIO()
   img.save(outputNormal, format='jpeg', optimize=True, quality=100)
   img.save("testImageUnCompressed.jpg", format='jpeg', optimize=True, quality=100)
   dataNormal = outputNormal.getvalue()
   resNormal = base91.encode(dataNormal)
   resNormal += "__END"


   print_file(resCompressed, 0, "compressed.txt")
   print_file(resNormal, 1, "uncompressed.txt")

def generateHeader(imageID, part):
    r = str(imageID) + "_" + str(part) + "___"
    return r, len(r)


def print_file(bytesToSend, image_id, filename = None):
    if filename is not None:
        f = open(filename, 'w')
    i = 0
    bytescovered = 0
    while bytescovered < len(bytesToSend):
        head = generateHeader(image_id, i)
        end = bytescovered + (255 - head[1])
        print head[0] + bytesToSend[bytescovered:end]
        if filename is not None:
            f.write(head[0]+bytesToSend[bytescovered:end])
            f.write("\n")
        bytescovered = end
        i += 1
    f.close()

if __name__ == '__main__':
    main()
