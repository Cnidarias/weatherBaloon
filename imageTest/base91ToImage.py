import io
import base91
import random
from PIL import Image

class regenerateImage():
    def __init__(self, image_id):
        self.image_id = image_id
        self.parts = {}
        self.endReceived = False
        self.endPartNumber = None
        self.endDeliminator = "__END"

    def addPart(self, part):
        parsed = part.split("___", 1)
        header = parsed[0]
        content = parsed[1]
        info = header.split("_")
        if info[0] is not self.image_id:
            return
        key = int(info[1])
        if key in self.parts:
            return 

        if content.endswith(self.endDeliminator):
            print "got END"
            content = content[:-len(self.endDeliminator)]
            self.endPartNumber = key
            self.endReceived = True


        self.parts[key] = content
        print "added" + str(key)

        if self.endReceived:
            self.checkImage()


    def checkImage(self):
        i = 0
        while i <= self.endPartNumber:
            if i not in self.parts:
                print "NOT ALL PARTS"
                return
            i += 1
        # we have gather all parts - so lets convert and make image

        i = 0
        imageBuffer = ""
        while i <= self.endPartNumber:
            imageBuffer += self.parts[i]
            i += 1

        decodedImage = base91.decode(imageBuffer)
        ioBuffer = io.BytesIO()
        ioBuffer.write(decodedImage)
        ioBuffer.seek(0)
        print "made IMAGE"

        img = Image.open(ioBuffer)
        img.show()



def main():
    imageProcessors = dict()

    filename = "compressed.txt"
    r = getImage(filename)
    for ele in r:
        res = ele.split("_", 1)
        if res[0] in imageProcessors:
            imageProcessors[res[0]].addPart(ele)
            print "added processor"
        else:
            print "made processor"
            imageProcessors[res[0]] = regenerateImage(res[0])
            imageProcessors[res[0]].addPart(ele)




def getImage(filename):
    return [line.strip() for line in open(filename, 'r')]
    




if __name__ == '__main__':
    main()
