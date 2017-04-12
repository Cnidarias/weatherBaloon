from PIL import Image
import base91
import io
from os import walk
from timeit import default_timer as timer
import numpy
from scipy.signal import fftconvolve


def main(path):
    output = open('testresult2.txt', 'w')
    output.write("Filename,Quality,ImageSize,PacketSize,UsedPackets,NRMSE,SSIM,ExecutionTime\n")
    files = next(walk(path))[2]
    total = len(files)
    for idx, f in enumerate(files):
        qual = 100
        file_start = timer()
        while qual >= 5:
            start = timer()
            try:
                res = generateImageBase69(path+"/"+f, qual)
            except:
                print("failure on {}".format(f))
                qual -= 10
                continue
            end = timer()
            output.write("{},{},{},{},{},{}\n".format(f, qual, res[0], res[1], res[2], (end-start)))
            qual -= 10
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



def ssim(im1, im2, window, k=(0.01, 0.03), l=255):
    """See https://ece.uwaterloo.ca/~z70wang/research/ssim/"""
    # Check if the window is smaller than the images.
    for a, b in zip(window.shape, im1.shape):
        if a > b:
            return None, None
    # Values in k must be positive according to the base implementation.
    for ki in k:
        if ki < 0:
            return None, None

    c1 = (k[0] * l) ** 2
    c2 = (k[1] * l) ** 2
    window = window/numpy.sum(window)

    mu1 = fftconvolve(im1, window, mode='valid')
    mu2 = fftconvolve(im2, window, mode='valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = fftconvolve(im1 * im1, window, mode='valid') - mu1_sq
    sigma2_sq = fftconvolve(im2 * im2, window, mode='valid') - mu2_sq
    sigma12 = fftconvolve(im1 * im2, window, mode='valid') - mu1_mu2

    if c1 > 0 and c2 > 0:
        num = (2 * mu1_mu2 + c1) * (2 * sigma12 + c2)
        den = (mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2)
        ssim_map = num / den
    else:
        num1 = 2 * mu1_mu2 + c1
        num2 = 2 * sigma12 + c2
        den1 = mu1_sq + mu2_sq + c1
        den2 = sigma1_sq + sigma2_sq + c2
        ssim_map = numpy.ones(numpy.shape(mu1))
        index = (den1 * den2) > 0
        ssim_map[index] = (num1[index] * num2[index]) / (den1[index] * den2[index])
        index = (den1 != 0) & (den2 == 0)
        ssim_map[index] = num1[index] / den1[index]

    mssim = ssim_map.mean()
    return mssim, ssim_map


def nrmse(im1, im2):
    a, b = im1.shape
    rmse = numpy.sqrt(numpy.sum((im2 - im1) ** 2) / float(a * b))
    max_val = max(numpy.max(im1), numpy.max(im2))
    min_val = min(numpy.min(im1), numpy.min(im2))
    return 1 - (rmse / (max_val - min_val))


if __name__ == "__main__":
    import sys
    from scipy.signal import gaussian
    from PIL import Image

    img1 = Image.open(sys.argv[1])
    img2 = Image.open(sys.argv[2])

    if img1.size != img2.size:
        print("Error: images size differ")
        raise SystemExit

    # Create a 2d gaussian for the window parameter
    win = numpy.array([gaussian(11, 1.5)])
    win2d = win * (win.T)

    num_metrics = 2
    sim_index = [2 for _ in range(num_metrics)]
    for band1, band2 in zip(img1.split(), img2.split()):
        b1 = numpy.asarray(band1, dtype=numpy.double)
        b2 = numpy.asarray(band2, dtype=numpy.double)
        # SSIM
        res, smap = ssim(b1, b2, win2d)

        m = [res, nrmse(b1, b2)]
        for i in range(num_metrics):
            sim_index[i] = min(m[i], sim_index[i])

    print("Result:", sim_index)




if __name__ == '__main__':
  main("mob")
