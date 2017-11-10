import argparse
import os
from scipy.misc import imread, imresize
import face_tool
from storage import Storage
import logger
from shutil import copyfile

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="input directory that contains image files.")
ap.add_argument("-o", "--output", required=True,
                help="output directory.")
ap.add_argument("-s", "--scale", default=50, type=int,
                help="reduce image size as percentage.")
ap.add_argument("-t", "--threshold", default=0.5, type=float,
                help="threshold of face recognizer.")
ap.add_argument("-d", "--database", default=os.path.join(os.environ['HOME'], ".face_cluster"), type=str,
                help="place to save encoded face information.")
args = vars(ap.parse_args())

faces = []

logger.info("Reading storage ...")
storage = Storage(args["database"])
if storage.has_faces():
    logger.info("Scanning known faces ...")
    known_faces_list = storage.scan_faces()
    known_faces = []
    for known_face_encoding, known_face_id in known_faces_list:
        face = face_tool.Face(known_face_encoding, id=known_face_id, cache=True)
        known_faces.append(face)
    logger.info("{} faces has been loaded from database.".format(len(known_faces)))
    faces += known_faces


def scan_images(path):
    logger.info("Scanning images ...")
    output = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".jpg"):
                output.append(os.path.join(root, f))
    return output


def process_files(files):
    for f in files:
        logger.info("Reading {}".format(f), newline=False)
        image = imread(f)
        image = imresize(image, args["scale"])
        detected_faces = face_tool.detect_faces(image)
        landmarks = face_tool.face_landmarks(image, detected_faces)
        encodings = face_tool.face_encodings(image, landmarks)

        prepared_known_faces = [face.encoding for face in faces]
        labels = []
        for face_encoding in encodings:
            index, _ = face_tool.compare_faces(prepared_known_faces, face_encoding)
            face = face_tool.Face(face_encoding, path=f)
            if index >= 0:
                face.id = faces[index].id
            labels.append(str(face.id))
            faces.append(face)
        logger.info(". Done", prefix=False)
        logger.info("Details , {} faces , labels {}".format(len(detected_faces), labels))


def main():
    process_files(scan_images(args["input"]))
    if not os.path.exists(args["output"]):
        os.mkdir(args["output"])

    face_counter = {}
    logger.info("Saving faces, {} detected".format(len(faces)))
    for face in faces:
        if not face.cache:
            storage.save_face(face)

            target_path = os.path.join(args["output"], str(face.id))
            if not os.path.exists(target_path):
                os.mkdir(target_path)

            number = 0
            if face.id in face_counter:
                number = face_counter[face.id]
            copyfile(face.path, os.path.join(target_path, "{}.jpg".format(number)))
            face_counter[face.id] = number + 1


if __name__ == "__main__":
    main()
