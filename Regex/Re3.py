import sys
idx = int(sys.argv[1])-50
listOfRegEx = [r"/(\w)*\w*\1\w*/i",
               r"/(\w)*(\w*\1\w*){3}/i",
               r"/^(0|1)([01]*\1)*$/",
               r"/(?=\w*cat)\b\w{6}\b/i",
               r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
               r"/\b(?!\w*cat)\w{6}\b/i",
               r"/(?!(\w)*\w*\1)\b\w+/i",
               r"/^(?!.*10011)[01]*$/",
               r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
               r"/^(?!.*1.1)[01]*$/"
              ]
print(listOfRegEx[idx])
