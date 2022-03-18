#import sys
#idx = int(sys.argv[1])-40
listOfRegEx = [r"/^[xo.]{64}$/i", # Good
               r"/^[xo]*\.[xo]*$/i", # Good
               r"/^((x+o*)?\..*|.*\.(o*x+)?)$/i",#27,21
               r"/^.(..)*$/s", # Good
               r"/^(0|1[01])([01]{2})*$/", # Good
               r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i", #Good
               r"/^(0|10)*1*$/", # Good
               r"/^[bc]*a[bc]*$|^[bc]+$/", #21,17
               r"/^([bc]*a[bc]*a[bc]*)+$|^[bc]+$/", #22,21
               r"/^(2|1[20]*1)([20]*1[20]*1[20]*)*[20]  NN*$/" #38, best 32

               ]
#print(listOfRegEx[idx])
print([1,2,3,4,1].remove(1))
#224