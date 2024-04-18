#-------------------------------------------------------------------------------
# Name:        module1
#-------------------------------------------------------------------------------

api = "https://api.apis.guru/v2/list.json"
import requests
from requests import get
import pickle
import os
def main():
   grpFile = "grps.json"
   fileFound = 0
   # check if file exist, if not pull from api
   # if file exist read data, check for number of records and send a
   # pull request to api server and match with number of records if matched use local file.
   res = get(api, verify=False)
   try:
       os.stat(grpFile)
       fileFound = 1
   except FileNotFoundError as e:
         print('File not found') # create a new file and add contents
         fileFound = 0
   if fileFound: # read from file
     with open(grpFile, "rb") as gfile:
       data = pickle.load(gfile)
   else:
        res = get(api, verify=False)
        with open(grpFile, "wb") as gfile:
            data =res.json()
            pickle.dump(data, gfile)
   print(data)

   # with open()


if __name__ == '__main__':
    main()
