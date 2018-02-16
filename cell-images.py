import json
import os
import requests
import time
import shutil

# set authorization bearer header with Smartsheet Access Token
token = "Bearer " + os.environ['SMARTSHEET_ACCESS_TOKEN']
payload = {"Authorization": token,
          "Content-Type": "application/json"}

# get your sheets you want to download
backed_up_sheets = {"Birthdays": 8534633835980676}
# set the dir value with the current location of the python script that is running
dir = os.path.dirname(os.path.realpath(__file__))
# Smartsheet API Urls
API_URL = "https://api.smartsheet.com/2.0/"
SHEETS_URL = API_URL + "sheets/"
GET_IMAGE_URLS_URL = API_URL + "imageurls"

amount = len(backed_up_sheets)

i = 1
for el in backed_up_sheets:
    # get sheet
    raw_sheet = requests.get(SHEETS_URL+str(backed_up_sheets[el]), headers=payload)
    sheet = raw_sheet.json()
    # parse sheet
    for row in sheet['rows']:
        for cell in row['cells']:
            # step 1: Identify the cell that contains an image
            if "image" in cell:
                # step 2: get image info from cell
                cell_image = cell["image"]
                # step 3: get image url
                image_url_response = requests.post(GET_IMAGE_URLS_URL, headers=payload, json=[{"imageId": str(cell["image"]["id"])}]) 
                image_url_json = image_url_response.json()
                # step 4: download the image from the url
                image_url = image_url_json["imageUrls"][0]["url"]
                img_response = requests.get(image_url, stream=True)
                # make sure img directory exists
                img_dir = dir + "/img/"
                if not os.path.exists(img_dir):
                    os.makedirs(img_dir)
                # save image file
                with open(img_dir + cell["displayValue"], 'wb') as f:
                    img_response.raw.decode_content = True
                    shutil.copyfileobj(img_response.raw, f)
    print ('Progress in sheets: ' + str(i) + '/' + str(amount))
    i += 1