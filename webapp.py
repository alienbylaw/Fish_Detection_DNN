import streamlit as st
import os
from PIL import Image
import subprocess
import sys
import os

#Importing the detection script that is connected to the AI model
import detect_fish_script as fish_script

#Accepts a list of photos and saves them fish_test_images to be uploaded into the model
def photo_to_folder(image):

    path = "C:/Users/ailee/OneDrive/Documents/Archipelagos Institute of Marine Conservation/Object Detection Model/models/research/object_detection/test_images/fish_test_images/"
    
    with open(os.path.join(path, image.name), "wb") as f:

        f.write(image.getbuffer())
        return st.success(f"Saved File: {image} \n")


def generate_command_string():
    model_path = ".\\new_model\\content\\inference_graph\\saved_model\\"
    labelmap_path = ".\\labelmap.pbtxt"
    test_images_path = ".\\test_images\\fish_test_images\\"

    command_string = (
        f"python .\\detect_fish_script.py. "
        f"-m {model_path} "
        f"-l {labelmap_path} "
        f"-i {test_images_path}"
    )

    return command_string

#Function to delete all previous pictures in test folder before uploading new pictures
def del_prev_pics(path):

    for file in os.listdir(path):
        os.remove(os.path.join(path,file))




def main():
    
    # - - - - - - - - - - - - - SETUP - - - - - - - - - - - - - - - - -


    st.sidebar.image(".\\archi_logo.png", use_column_width=True)

    

    pic_path = "C:/Users/ailee/OneDrive/Documents/Archipelagos Institute of Marine Conservation/Object Detection Model/models/research/object_detection/test_images/fish_test_images/"
    output_path = "C:/Users/ailee/OneDrive/Documents/Archipelagos Institute of Marine Conservation/Object Detection Model/models/research/object_detection/outputs/"
    path = "C:/Users/ailee/OneDrive/Documents/Archipelagos Institute of Marine Conservation/Object Detection Model/models/research/object_detection/"

    #deleting previously saved images in test and output folder
    del_prev_pics(pic_path)
    del_prev_pics(output_path)


    st.title("Welcome to the Fish Detector Machine! :fish:")

    menu = ["Home", "Document Files", "Sources/Resources", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":


        st.subheader("Home")

        #Contains a list of all images uploaded
        image_file = st.file_uploader("Upload your pictures of fish for the DDN to detect them.", type = ["png", "jpg", "jpeg"], accept_multiple_files=True)
        
        #If the image upload spot is not empty, it will enter this conditional statement below
        if image_file is not None:
            
             #Keeps track of the number of photos uploaded and organizes it
             i = 1
            #creating a dictinary with information for each picture
             for image in image_file:
                 
                 file_details = {f"FileName{str(i)}":image.name,f"FileType{str(i)}":image.type, f"FileSize{str(i)}":image.size}

                 st.write(file_details)

                 photo_to_folder(image)

                 #Appending the iterator 
                 i = i + 1


             if st.button("Press to begin detection model."):
                 
                 #- - - - - - - - - - - - -Running detect_fish_script.py - - - - - - - -
                 #run the fish detection script here 
                 subprocess.call(f"{generate_command_string()}")
                 
                 # - - - - - - - - - - - - - - - - - - Creating dictionary with picture names and object values - - - - - - -

                  #txt file containing all the objects detected and their file paths
                 #Creating a list of the txt file. Each object is a line in the txt file
                 with open("objects_identified.txt", "r") as file:
                     #reads each line from the txt file, and stores it in a list with this one line
                     objects = [line.strip() for line in file]

                 
                 #finding how many photos there are to be iterated over
                 lines = len(objects)
                 pic_info = {}
                 i = 0

                 #Create a dictionary out of the data in the txt file. First value is the name, below it is the value.
                 #Appending the list values into a dictionary
                 while i < lines:
                     #All objects that are %2 = 0 will be a name, otherwise they will be a value 
                     pic_info[objects[i]] = objects[i+1]
                     i = i + 2





                 
                 # can compare the file details to the dictionary with a for loop to check if its in it

                 
                 #make a slide show of the pictures and pair them up to look nice

                 st.write('Fish detected with a confidence of less then 50% will not be displayed in images.')
                 
                 #Checking if the output file corresponds to a key in the dictionary (have the same name)
                 for output in os.listdir(output_path):
                     
                     #displaying images by obtaining the output picture in the output file and finding the same name in the dictionary
                     if output in pic_info:
                         
                         #st.select_slider('Images with Detected Fish', f' Image name:{output} - - - - - Total Number of Fish Detected: {pic_info[output]}', '.\\outputs\\')
                         st.image(f'.\outputs\{output}', caption=f' Image name : {output} - - - - - Total Number of Fish Detected : {pic_info[output]}')
                         


                     else:
                         st.write("Problem occured when attempting to display photos. Please try again.")
                         

                    #ADD AN ARCHIPELAGOS IMAGE SOMEWHERE IN THE CORNER OF THE WEBSITE

                 
                     

                     
    




     #Not sure if I need this one       
    elif choice == "Document Files":
        st.subheader("Document Files")
        st.write("All the following documents were used in the creation of the AI model. Click on one of the links below to download the corresponding document.")

        with open("detect_fish_script.py") as file:

            st.download_button("Fish Detection Python Script : Combines the AI model with the inputted images to develop final output images", data=file, file_name="detect_fish_script.py")


    


        with open("C:/Users/ailee/OneDrive/Documents/Archipelagos Institute of Marine Conservation/Object Detection Model/models/model_file.zip", encoding="latin-1") as file:

            st.download_button(label="Model architecture folder obtained from TensorFlow (edits have been made to fit the needs of this particular object detection model)", data=file,file_name="model_file.zip")


        st.write("\nAll other required documents that have been created for the Fish Detection model are in the Model Architecture folder.")

    #Contains copies of the individual python script for the detection and links to all sources I used (tensorflow, etc)
    elif choice == "Sources/Resources":
        st.subheader("Sources/Resources")
        st.write("\n\n Tensorflow Model Architecture - Provided the model architecture via a zipped folder which contained the skeleton required to create a personalized fish detection model:")
        st.write("https://github.com/tensorflow/models")
        st.write("\n\n How to Train Personal AI Model Tutorial - Provided a guide for how to create a custom object detector using the TensorFlow Object Detection API:")
        st.write("https://neptune.ai/blog/how-to-train-your-own-object-detector-using-tensorflow-object-detection-api")
        st.write("\n\nConfig File for the Tensorflow Model - Used together with the Tensorflow Model. The config file chosen depends on your model and Tensorflow version :")
        st.write("https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API")
        st.write("\n\nStreamlit documentation - Used to create the Streamlit webapp : ")
        st.write("https://docs.streamlit.io/")

    #Discription of me and why I made the project. Consider if this were to go on my github.
    elif choice == "About":
        st.subheader("About")
        st.write("")
        st.write("Welcome to the Fish Detector Machine!\n\nThis project was created by Aileen Mulaw, a student at the University of Calgary studying Geomatics Engineering with an Aerospace Engineering minor. It was made in collaboration with the Archipelagos Institute of Marine Conservation as a student project under the GIS/Remote Sensing team. ")
        st.write("\n\n ROV imaging is a very useful tool that has innovated the marine technology sector. As much as this technology has revolutionized marine imaging, it still has multiple limitations that interfer with the research of scientists. One of the most apparent problems is the need for scientists to watch countless videos to identify different species that appear along with counting the number that appear on the screen, frame by frame. ")
        st.subheader("How Can We Fix This?")
        st.write("With the use of AI technology of course! AI technology has revolutionized the world in the past 2 years, and seems to be ever evolving as it continues to grow with the creation of modern technology. AI is slowly being introduced and integrated into different industries and sectors, which also includes the marine sector. This project was created to demonstrate how we can use AI technology to relieve scientists of having to go through the painstaking process of interating through videos manually which could lead to hours of time wasted that could have been used analyzing/interpreting data. When instead, an AI could produce close to perfect results in the matter of seconds. ")
    

if __name__ == '__main__':
    main()
