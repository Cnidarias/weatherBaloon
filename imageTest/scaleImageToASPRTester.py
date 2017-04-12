from PIL import Image
import base91
import io
from os import walk
from timeit import default_timer as timer


def main(path):
  output = open('testresult.txt', 'w')
  output.write("Filename,Quality,ImageSize,UsedPackets,ExecutionTime\n")
  files = next(walk(path))[2]
  total = len(files)
  for idx, f in enumerate(files):
    qual = 100
    while qual >= 5:
      start = timer()
      res = generateImageBase69(path+"/"+f, qual)
      end = timer()
      output.write("{},{},{},{},{},{}\n".format(f, qual, res[0], res[1], res[2], (end-start)))
      qual -= 5
    output.write("\n")
    print("Progress: {}/{}".format(idx + 1, total))
  output.close()




def generateImageBase69(filename, quality):
  img = Image.open(filename, mode='r')
  img.thumbnail((320, 240), Image.ANTIALIAS)
  img = img.convert('L')
  outputCompressed = io.BytesIO()
  img.save(outputCompressed, format='jpeg', optimize=True, quality=quality)
  dataCompressed = outputCompressed.getvalue()
  resCompressed = base91.encode(dataCompressed)
  resCompressed += "__END"
  return len(dataCompressed), len(resCompressed), print_file(resCompressed, 0)

def generateHeader(imageID, part):
  r = str(imageID) + "_" + str(part) + "___"
  return r, len(r)


def print_file(bytesToSend, image_id):
  i = 0
  bytescovered = 0
  retString = ""
  while bytescovered < len(bytesToSend):
    head = generateHeader(image_id, i)
    end = bytescovered + (255 - head[1])
    retString += head[0] + bytesToSend[bytescovered:end] + "\n"
    bytescovered = end
    i += 1
  return i+1







if __name__ == '__main__':
  main("Mobius")
