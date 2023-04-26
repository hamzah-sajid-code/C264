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
    given_file = request.files["input_file"]
    given_proccess = request.form["proccess_selection"]

    secure_file = secure_filename(given_file.filename)
    file = given_file.read()
    get_data = np.fromstring(file, dtype="uint8")
    decoded_data = cv2.imdecode(get_data, cv2.IMREAD_UNCHANGED)

    if given_proccess == "gray":
        output_image = give_gray(decoded_data)
    elif given_proccess == "sketch":
        output_image = give_sketch(decoded_data)
    elif given_proccess == "oil":
        output_image = give_oil(decoded_data)
    elif given_proccess == "rgb":
        output_image = give_rgb(decoded_data)
    elif given_proccess == "water":
        output_image = give_water_color(decoded_data)
    elif given_proccess == "invert":
        output_image = give_invert(decoded_data)
    elif given_proccess == "hdr":
        output_image = give_hdr(decoded_data)

    with open(os.path.join("static/", secure_file), "wb") as f:
        f.write(output_image)

    msg = "Your image is succesfully transferred to the server"
    return render_template("upload.html", filename=secure_file, message=msg)



def give_gray(file):
    grayscaler = cv2.cvtColor(file, cv2.COLOR_RGB2GRAY)
    status, ouput_image = cv2.imencode(".PNG",grayscaler)
    return ouput_image

def give_sketch(file):
    grayscaled = cv2.cvtColor(file, cv2.COLOR_RGB2GRAY)
    sharped_image = cv2.bitwise_not(grayscaled)
    blurred_image = cv2.GaussianBlur(sharped_image, (111,111), 0)
    sharped_image = cv2.bitwise_not(blurred_image)
    sketch_image = cv2.divide(grayscaled,sharped_image, scale=256.0)
    status, ouput_image = cv2.imencode(".PNG", sketch_image)
    return ouput_image

def give_oil(file):
    oil_effect_image = cv2.xphoto.oilPainting(file, 7, 1)
    status, ouput_image = cv2.imencode(".PNG", oil_effect_image)
    return ouput_image

def give_rgb(file):
    rgb_convert = cv2.cvtColor(file, cv2.COLOR_BGR2RGB)
    status, ouput_image = cv2.imencode(".PNG",rgb_convert)
    return ouput_image

def give_water_color(file):
    water_color = cv2.stylization(file, sigma_s=60, sigma_r=0.6)
    status, ouput_image = cv2.imencode(".PNG",water_color)
    return ouput_image

def give_invert(file):
    inverted = cv2.bitwise_not(file)
    status, ouput_image = cv2.imencode(".PNG",inverted)
    return ouput_image

def give_hdr(file):
    hdr = cv2.detailEnhance(file, sigma_s=12, sigma_r=0.15)
    status, ouput_image = cv2.imencode(".PNG",hdr)
    return ouput_image


@app.route("/display/<filename>")
def get_grayed(filename):
    return redirect(url_for("static", filename=filename))


if __name__ == "__main__":
    app.run()