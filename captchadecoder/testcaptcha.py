import mechanize
import urllib
import json
import captchadecoder;

cd = captchadecoder.CaptchaDecoder()

br = mechanize.Browser()
url = "http://skyscraper.zenyai.net/captcha_api.php"

loops = 3000
result = []
for i in range(loops):
    data = json.loads(br.open(url).read())
    
    answer = data['answer']
    img_url = data['url']

    # f = open('example/%s.png' % answer,'wb')
    # f.write(br.open(img_url).read())
    # f.close()

    guess = cd.DecodeImageURL(img_url, False)

    if guess == answer:
        result.append("Yes")
    else:
        result.append("No")

    print "#" + str(i) + ": " + str(guess) + " " + str(answer) + ", C: " +  str(result.count("Yes")) + " W: " + str(result.count("No"))


print "Total number of correct guess: " + str(result.count("Yes"))
print "Wrong guess: " + str(result.count("No"))