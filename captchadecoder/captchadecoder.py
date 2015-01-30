__author__ = 'Narongdej'

from operator import itemgetter
import os, sys, hashlib, time
from PIL import Image
import vectorspace


class CaptchaDecoder:

    def DecodeImage(self, imagepath, debug=False):
        im = Image.open(imagepath)
        im = im.convert("P")
        im2 = Image.new("P",im.size, 255)
        temp = {}
        for x in range(im.size[1]):
          for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            temp[pix] = pix
            if pix == 118 or pix == 82: # these are the numbers to get
              im2.putpixel((y,x),0)

        inletter = False
        foundletter=False
        start = 0
        end = 0

        letters = []

        for y in xrange(im2.size[0]):
          for x in xrange(14, im2.size[1]):
            pix = im2.getpixel((y, x))

            if pix != 255:
              inletter = True

          if foundletter == False and inletter == True:
            foundletter = True
            start = y

          if foundletter == True and inletter == False:
            foundletter = False
            end = y
            letters.append((start,end))

          inletter=False

        v = vectorspace.VectorSpace()

        iconset = [x[1] for x in os.walk("iconset")][0]
        imageset = []

        for letter in iconset:
          for img in os.listdir('./iconset/%s/'%(letter)):
            temp = []
            if img != "Thumbs.db":
              temp.append(self.buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
            imageset.append({letter:temp})

        count = 0
        for letter in letters:
          m = hashlib.md5()
          im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))

          guess = []

          for image in imageset:
            for x,y in image.iteritems():
              if len(y) != 0:
                guess.append( ( v.relation(y[0], self.buildvector(im3)),x) )

          guess.sort(reverse=True)
          if debug:
            print "",guess[0]
          else:
            sys.stdout.write(guess[0][1])
          count += 1

    def buildvector(self,im):
          d1 = {}
          count = 0
          for i in im.getdata():
            d1[count] = i
            count += 1
          return d1


    def ImageTopColour(self, imagepath):
        im = Image.open(imagepath)
        im = im.convert("P")
        his = im.histogram()
        values = {}

        for i in range(256):
          values[i] = his[i]

        for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
          print j,k

    # def SaveLetter(self, letter):
    #     count = 0
    #     for letter in letters:
    #       m = hashlib.md5()
    #       im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    #       m.update("%s%s"%(time.time(),count))
    #       im3.save("./%s.gif"%(m.hexdigest()))
    #       count += 1