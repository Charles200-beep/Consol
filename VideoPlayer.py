import sys, time, cv2, io
from PIL import Image, ImageOps
from moviepy.editor import *
from playsound import playsound

ASCII_CHARS = ["@", "#", "a", "%", "?", "*", "+", ";", ":", ",", "."]

def main():
    if isinstance(sys.argv[1], str):
        vidcap = cv2.VideoCapture(sys.argv[1])
        moviepy_vid = VideoFileClip(sys.argv[1])
    else:
        print("Wrong arguments!")

    audio = moviepy_vid.audio
    audio.write_audiofile("sound.wav")
    success, image = vidcap.read()
    image_str = asciiify(image)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    playsound(os.path.abspath("sound.wav"), block=False)
    while success:
        print(image_str)
        print(fps)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        success, image = vidcap.read()
        image_str = asciiify(image)
        time.sleep(1/60)

def asciiify(image):
    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
    image_pil = Image.open(io.BytesIO(image_bytes))
    image_pil = resize(image_pil, 130)
    image_pil = to_grayscale(image_pil)
    return to_ascii(image_pil)

def to_grayscale(image):
    return image.convert("L")

def invert(image):
    return ImageOps.invert(image)

def resize(image, new_width = 100):
    old_width, old_height = image.size
    new_height = new_width * old_height / old_width
    return image.resize((int(new_width), int(new_height)))

def to_ascii(image):
    pixels = list(image.getdata())
    ascii_str = ""
    ascii_image = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[int(pixel // 25)]
    for i in range(0, len(ascii_str), image.width):
        ascii_image += ascii_str[i:i + image.width] + "\n"
    return ascii_image

if __name__ == "__main__":
    main()