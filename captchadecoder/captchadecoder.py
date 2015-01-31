__author__ = 'Narongdej'

from operator import itemgetter
import os, sys, hashlib, time, urllib, cStringIO
from PIL import Image
import vectorspace


class CaptchaDecoder:

    def __init__(self):
        self.v = vectorspace.VectorSpace()

        iconset = [x[1] for x in os.walk("iconset")][0]
        self.imageset = []

        for letter in iconset:
          for img in os.listdir('./iconset/%s/'%(letter)):
            temp = []
            if img != "Thumbs.db":
              temp.append(self.buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
            self.imageset.append({letter:temp})

        self.limit = None


    def DecodeImageURL(self, imageurl, debug=False):
        file = cStringIO.StringIO(urllib.urlopen(imageurl).read())
        return self.DecodeImage(file, debug)

    def DecodeImage(self, imagepath, debug=False):
        im = Image.open(imagepath)

        if self.limit is None:
            self.ImageTopColour(im)

        inletter = False
        foundletter=False
        start = 0
        end = 0

        letters = []

        for y in xrange(im.size[0]): # slice across
            for x in xrange(im.size[1]): # slice down
                pix = im.getpixel((y, x))
                if pix[3] >= self.limit:
                    inletter = True

            if foundletter == False and inletter == True:
                foundletter = True
                start = y

            if foundletter == True and inletter == False:
                foundletter = False
                end = y
                letters.append((start,end))

            inletter = False

        if len(letters) < 4:
            if(debug):
                print "Letter cut not correctly, returning false"
            return

        v = self.v
        imageset = self.imageset

        count = 0
        answer = ""
        for letter in letters:
          m = hashlib.md5()
          im3 = im.crop(( letter[0] , 0, letter[1],im.size[1] ))

          guess = []

          for image in imageset:
            for x,y in image.iteritems():
              if len(y) != 0:
                guess.append( ( v.relation(y[0], self.buildvector(im3)),x) )

          guess.sort(reverse=True)
          if debug:
            print "",guess[0]
          else:
            answer += guess[0][1]
          count += 1
        return answer

    def buildvector(self,im):
          d1 = {}
          count = 0
          for i in im.getdata():
            d1[count] = sum(i)
            count += 1
          return d1


    def ImageTopColour(self, im):

        # import operator
        #
        # from collections import defaultdict
        # by_color = defaultdict(int)
        # for pixel in im.getdata():
        #     by_color[sum(pixel)] += 1
        # self.limit = sorted(by_color.items(), key=operator.itemgetter(1), reverse=True)[10][0]
        # #print sorted(by_color.items(), key=operator.itemgetter(1), reverse=True)
        self.limit = 170

    def TrainLearningSet(self, imagedirectory):
        trainingset = [x[2] for x in os.walk(imagedirectory)][0]
        filename = [os.path.splitext(filename)[0] for filename in trainingset]

        tsCount = 0
        for ts in trainingset:
            im = Image.open(imagedirectory + ts)

            if self.limit is None:
                self.ImageTopColour(im)

            inletter = False
            foundletter = False
            start = 0
            end = 0


            letters = []
            for y in xrange(im.size[0]): # slice across
                for x in xrange(im.size[1]): # slice down
                    pix = im.getpixel((y, x))
                    #print sum(pix)
                    if pix[3] >= self.limit:
                        inletter = True

                if foundletter == False and inletter == True:
                    foundletter = True
                    start = y

                if foundletter == True and inletter == False:
                    foundletter = False
                    end = y
                    letters.append((start,end))

                inletter = False

            #if len(letters) < 4:
                #break

            count = 0
            for letter in letters:
                m = hashlib.md5()
                im3 = im.crop(( letter[0] , 0, letter[1],im.size[1] ))
                m.update("%s%s"%(time.time(),count))

                try:
                    if not os.path.exists("iconset/"+filename[tsCount][count] + "/"):
                        os.makedirs("iconset/"+filename[tsCount][count] + "/")

                    im3.save("iconset/%s/%s.png"%(str(filename[tsCount][count]), m.hexdigest()))
                    count += 1
                except Exception:
                    pass

            tsCount += 1



    # def SaveLetter(self, letter):
    #     count = 0
    #     for letter in letters:
    #       m = hashlib.md5()
    #       im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    #       m.update("%s%s"%(time.time(),count))
    #       im3.save("./%s.gif"%(m.hexdigest()))
    #       count += 1