import base91
import io
from os import walk
from timeit import default_timer as timer
import numpy
from PIL import Image
from ssim import compute_ssim



def main(path):
    output = open('testresult2.txt', 'w')
    output.write("Filename,Quality,ImageSize,PacketSize,UsedPackets,NRMSE,SSIM,ExecutionTime\n")
    files = next(walk(path))[2]
    total = len(files)
    for idx, f in enumerate(files):
        qual = 100
        file_start = timer()
        img1 = None
        while qual >= 5:
            start = timer()
            try:
                res = generateImageBase69(path+"/"+f, qual)
            except:
                print("failure on {}".format(f))
                break
            end = timer()
            if qual == 100:
                img1 = Image.open(res[3])

            compImage = Image.open(res[3])
            ssimval = compute_ssim(img1, compImage)
            nrmseval = nrmse(img1, compImage)
            output.write("{},{},{},{},{},{},{},{}\n".format(f, qual, res[0], res[1], res[2], nrmseval, ssimval, (end-start)))
            qual -= 5

        output.write("\n")
        file_end = timer()
        print("Progress: {}/{} ({})-- {}".format(idx + 1, total, (idx+1)*100.0/float(total), file_end - file_start))
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
    return len(dataCompressed), len(resCompressed), print_file(resCompressed, 0), outputCompressed



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


def nrmse(img1, img2):
    im1 = numpy.asarray(img1, dtype=numpy.double).T
    im2 = numpy.asarray(img2, dtype=numpy.double).T
    a, b = im1.shape
    rmse = numpy.sqrt(numpy.sum((im2 - im1) ** 2) / float(a * b))
    max_val = max(numpy.max(im1), numpy.max(im2))
    min_val = min(numpy.min(im1), numpy.min(im2))
    return 1 - (rmse / (max_val - min_val))

if __name__ == '__main__':
    main("mob")
