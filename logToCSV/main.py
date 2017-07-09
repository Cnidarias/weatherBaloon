import re

def main():
    patternStr = '(\d+) Thread-3 DATA:gps:(\d+\.\d+)\,(\d+\.\d+)\,(\d+\.\d+)\,(\d+\.\d+)\; 3:(\d+)\;7:(\d+);4:(\d+);135:(\d+)\;131:(\d+)\;d:(\d+\.\d+)'

    outfileGood = open('output.csv', 'w')
    outfileGood.write('time,h,lat,lon,sat,3,7,4,135,131,d\n')

    outfileBad = open('failed.log', 'w')

    out1 = open('out1.csv', 'w')
    out1.write('time\n')
    out2 = open('out2.csv', 'w')
    out2.write('h\n')
    out3 = open('out3.csv', 'w')
    out3.write('lat\n')
    out4 = open('out4.csv', 'w')
    out4.write('lon\n')
    out5 = open('out5.csv', 'w')
    out5.write('sat\n')
    out6 = open('out6.csv', 'w')
    out6.write('3\n')
    out7 = open('out7.csv', 'w')
    out7.write('7\n')
    out8 = open('out8.csv', 'w')
    out8.write('4\n')
    out9 = open('out9.csv', 'w')
    out9.write('135\n')
    out10 = open('out10.csv', 'w')
    out10.write('131\n')
    out11 = open('out11.csv', 'w')
    out11.write('d\n')

    pattern = re.compile(patternStr, re.DOTALL)
    for line in open('ttyACM1.log'):
        line.rstrip('\n')
        res = pattern.search(line)

        print(line)
        if res is not None:
            r = res.groups()
            outfileGood.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10]))
            out1.write('{}\n'.format(r[0]))
            out2.write('{}\n'.format(r[1]))
            out3.write('{}\n'.format(r[2]))
            out4.write('{}\n'.format(r[3]))
            out5.write('{}\n'.format(r[4]))
            out6.write('{}\n'.format(r[5]))
            out7.write('{}\n'.format(r[6]))
            out8.write('{}\n'.format(r[7]))
            out9.write('{}\n'.format(r[8]))
            out10.write('{}\n'.format(r[9]))
            out11.write('{}\n'.format(r[10]))
            print(r)
        else:
            if len(line) > 5:
                outfileBad.write('{}'.format(line))

    outfileGood.close()
    outfileBad.close()
    out1.close()
    out2.close()
    out3.close()
    out4.close()
    out5.close()
    out6.close()
    out7.close()
    out8.close()
    out9.close()
    out10.close()
    out11.close()




if __name__ == '__main__':
    main()
