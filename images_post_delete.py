import glob, re, os, shutil

from get_images import landmark_shorthand, make_directories
from location_landmark_dict import alt_names, landmark_total_images

landmark_list = list(landmark_total_images.keys())
images_path, _ = make_directories()

def delete_directory(landmark, landmark_path, retained, deleted_list):
    if (retained < 175):
        print("There is not enough images to classify the landmark of", landmark)
        try: 
            shutil.rmtree(landmark_path)
            print("Success: Deleted the", landmark, "directory")
        except Exception as e: 
            print("Error: Failed to delete image because of", e)
        deleted_list.append(landmark)
    return deleted_list       

def edit_dictionaries(deleted_list): 
    for landmark in deleted_list: 
        with open("location_landmark_dict.py", "r+") as file: 
            lines = file.readlines()
        file.close()

        with open("location_landmark_dict.py", "w") as file: 
            for line in lines: 
                search_match = re.search(landmark, line)
                if search_match == None: 
                    file.write(line) 
        file.close()
        
deleted_list = []
for landmark in landmark_list:
    print("The number of images for", landmark, "downloaded is", end=" ")
    print(f"{landmark_total_images[landmark]}.")
    short_landmark = landmark_shorthand(alt_names, landmark)
    landmark_path = os.path.join(images_path, short_landmark)
    files = glob.glob(f"{landmark_path}/*.jpg")
    retained = len(files)
    print("The total number of images for", landmark, "after deletion is", end=" ")
    print(f"{retained}.")
    retained_pc = round(retained/landmark_total_images[landmark] * 100, 2)
    print(f"Therefore {retained_pc} percent of", landmark, "images retained.")
    deleted_list = delete_directory(landmark, landmark_path, retained, deleted_list)
    print("===============================")
edit_dictionaries(deleted_list)