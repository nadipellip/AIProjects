#import sys
#idx = int(sys.argv[1])-30
listOfRegEx = [r"/^0$|^10[10]$/",
               r"/^[01]*$/",
               r"/0$/",
               r"/\w*[aeiou]\w*[aeiou]\w*/i",
               r"/^0$|^1[01]*0$/",
               r"/^[01]*110[01]*$/",
               r"/^.{2,4}$/s",
               r"/^\d{3} *-? *\d\d *-? *\d{4}$/",
               r"/^.*?d\w*/mi",
               r"/^1[01]*1$|^0[10]*0$|^[01]?$/"
               ]
print(not set() and not set())
#101010010101
#01100110
