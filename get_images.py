import os, re, requests, shutil, time
from location_landmark_dict import location_landmark, alt_names
from math import ceil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def make_directories(): 
    directory_path = r"C:\Users\Gordon Li\Desktop\computer_vision"
    images_folder_path = os.path.join(directory_path, "images")
    chrome_driver_path = os.path.join(directory_path, "chrome_driver")
    chrome_driver_src = os.path.join(directory_path, "chromedriver.exe")
    chrome_driver_dest = os.path.join(chrome_driver_path, "chromedriver.exe")

    if os.path.exists(images_folder_path) == False: 
        os.mkdir(images_folder_path)
        
    if os.path.exists(chrome_driver_path) == False: 
        os.mkdir(chrome_driver_path)
        shutil.move(chrome_driver_src, chrome_driver_dest)
    return images_folder_path, chrome_driver_dest

def phrase_link(landmark): 
    landmark_string = landmark.replace(" ", "%20")
    return landmark_string

def landmark_shorthand(alt_names, landmark): 
    try: 
        landmark_short = alt_names[landmark].lower()
    except: 
        string_list = landmark.split(" ")
        if (string_list[0] == "The"): 
            landmark_short = string_list[1].lower()
        else: 
            landmark_short = string_list[0].lower()
    return landmark_short

def make_landmark_directories(images_path, landmark_short): 
    landmark_path = os.path.join(images_path, landmark_short)
    if os.path.exists(landmark_path) == False: 
        os.mkdir(landmark_path)
    return landmark_path

def total_images(phrase_landmark, web_driver): 
    url = fr"https://www.istockphoto.com/search/2/image?phrase={phrase_landmark}"
    web_driver.get(url)
    time.sleep(1.5)
    get_title = web_driver.title
    word_list = get_title.split()
    total_images = ceil(0.05 * int(word_list[0].replace(",", "")))   
    no_images = min(max(300, total_images), 1250) 
    return no_images
        

def scroll_end(web_driver): 
    web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)
    
    
def download_image(url, file_name, valid_images, valid_images_list): 
    
    response = requests.get(url)

    if not response.ok: 
        print("Failed to download image")

    else: 
        with open(file_name, "wb") as file: 
            file.write(response.content)
            valid_images += 1
            valid_images_list.append(url)
            print(f"Successful Image Download - {file_name}")
    
    return valid_images, valid_images_list

def get_image_url(images_path, web_driver, phrase_landmark, landmark_short, total_images): 
    valid_images_list = []
    valid_images = 0 
    page_no = 1
    while (valid_images < total_images):
        search_url = f"https://www.istockphoto.com/search/2/image?phrase={phrase_landmark}&page={page_no}"
        web_driver.get(search_url)
        scroll_end(web_driver)
        images = web_driver.find_elements(By.CLASS_NAME, "yGh0CfFS4AMLWjEE9W7v")
        for image in images: 
            src_url = image.get_attribute('src')
            file = landmark_short + f"_{valid_images + 1}.jpg"
            file_name = os.path.join(images_path, file)
            valid_images, valid_images_list = download_image(src_url, file_name, valid_images, valid_images_list)
            if (valid_images == total_images): 
                break
        page_no = page_no + 1

if __name__ == "__main__": 
    images_path, chrome_drive_path = make_directories()
    service = Service(executable_path=chrome_drive_path)
    web_driver = webdriver.Chrome(service=service)
    landmark_list = list(location_landmark.keys())[8:]
    images_dict = {} 
    for landmark in landmark_list: 
        phrase_landmark = phrase_link(landmark)
        landmark_short = landmark_shorthand(alt_names, landmark)
        landmark_path = make_landmark_directories(images_path, landmark_short)
        no_images = 1250
        images_dict[landmark] = no_images
        get_image_url(landmark_path, web_driver, phrase_landmark, landmark_short, no_images)
    with open("location_landmark_dict.py", "a") as file: 
        file.write("landmark_total_images = {\n")
        i = 0
        for landmark in images_dict.keys(): 
            file.write(f"""    "{landmark}": {images_dict[landmark]}""")
            if (i != len(landmark_list) - 1): 
                file.write(",\n")
            else: 
                file.write("\n")
            i += 1
        file.write("}\n")
