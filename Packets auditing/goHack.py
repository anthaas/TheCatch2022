import os
from PIL import Image
from collections import Counter
import pytesseract
import requests
from requests.structures import CaseInsensitiveDict
import re


def search_by_color(bg_color, pkg_color, path_to_file):
    with Image.open(path_to_file) as im:
        px = im.load()
    pixels = [i for i in im.getdata()]
    background, package = Counter(pixels).most_common(2)  # get two locors with most occurences
    bg_color, bg_count = background
    pkg_color, pkg_count = package
    if searching_bg_color == bg_color and searching_pkg_color == pkg_color:
        return pytesseract.image_to_string(im, config="--psm 6")  # using tesseract OCR
    return ""


searching_bg_color = (242, 121, 48)  # desired color of background
searching_pkg_color = (0, 133, 71)  # desired color of package icon

print("start searching in subfolder data")

url = "http://pickup.mysterious-delivery.thecatch.cz"
processed_files = 0
for path, subdirs, files in os.walk("data"):
    for name in files:
        processed_files += 1
        if processed_files % 100 == 0:
            print(f"analyzed {processed_files} files...")
        full_path = os.path.join(path, name)
        result = search_by_color(searching_bg_color, searching_pkg_color, full_path)
        if result != "":
            code = result.split(" ")[-1].strip()
            print(f"trying code {code} from file {full_path}")
            # try the extracted code in POST
            headers = CaseInsensitiveDict()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data = "packet-id=" + code + "&track-packet="
            response = requests.post(url, headers=headers, data=data)
            if "FLAG" in response.text:
                print(re.search(".*(FLAG\{.*\}).*", response.text).group(1))
                exit
            else:
                print("Nope!")
            print()
