__author__ = 'Narongdej'

import captchadecoder;

cd = captchadecoder.CaptchaDecoder()
#cd.ImageTopColour("example/0055.png")
cd.TrainLearningSet("trainingset/")
#cd.DecodeImage("example/9316.png", True)
#
import os
imagedirectory = "example/"
trainingset = [x[2] for x in os.walk(imagedirectory)][0]
filename = [os.path.splitext(filename)[0] for filename in trainingset]

i = 0
result = []
for ts in trainingset:
    decodeResult = cd.DecodeImage("example/"+ts, False)
    print decodeResult, filename[i]
    if filename[i] == decodeResult:
        result.append("Yes")
    else:
        result.append("No")

    i += 1

print result.count("Yes")
print result.count("No")
