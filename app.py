# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Write load_form function below to Open and redirect to default upload webpage
@app.route("/")
def index():
    return render_template("upload.html")



# Write upload_image Function to upload image and redirect to new webpage
@app.route("/gray", methods=["POST"])
def show_image():
    file = request.files["input_file"]
    secure_file = secure_filename(file.filename)
    new_grayscaled_file = give_gray(file.read())

    with open(os.path.join("static/", secure_file), "wb") as f:
        f.write(new_grayscaled_file)

    msg = "Your image is succesfully transferred to the server"
    return render_template("upload.html", filename=secure_file, message=msg)



def give_gray(file):
    get_data = np.fromstring(file, dtype="uint8")
    print("Get one-line data: ",get_data)
    decoded_data = cv2.imdecode(get_data, cv2.IMREAD_UNCHANGED)
    print(decoded_data)
    grayscaler = cv2.cvtColor(decoded_data, cv2.COLOR_RGB2GRAY)
    status, ouput_image = cv2.imencode(".PNG",grayscaler)
    print(status)
    return ouput_image


# Wite display_image Function to display the uploaded image
@app.route("/display/<filename>")
def get_grayed(filename):
    return redirect(url_for("static", filename=filename))



if __name__ == "__main__":
    app.run()