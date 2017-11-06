import dlib
import uuid
import numpy as np
import os

_base_dir = os.path.dirname(__file__)

_detector = dlib.get_frontal_face_detector()
_predictor = dlib.shape_predictor(os.path.join(os.path.join(_base_dir, "data"), "shape_predictor_5_face_landmarks.dat"))
_encoder = dlib.face_recognition_model_v1(os.path.join(os.path.join(_base_dir, "data"), "dlib_face_recognition_resnet_model_v1.dat"))


def detect_faces(img):
    return _detector(img, 1)


def face_landmarks(img, locations):
    return [_predictor(img, location) for location in locations]


def face_encodings(img, locations):
    return [np.array(_encoder.compute_face_descriptor(img, location, 1)) for
            location in locations]


def face_distance(encoded_faces, face_to_compare):
    if len(encoded_faces) == 0:
        return np.empty(0)

    return np.linalg.norm(encoded_faces - face_to_compare, axis=1)


def compare_faces(known_face_encodings, face_encoding_to_check, threshold=0.5):
    if not known_face_encodings:
        return -1, 0.0

    matches = list(face_distance(known_face_encodings, face_encoding_to_check))
    index = np.argmin(matches)
    if matches[index] < threshold:
        return index, matches[index]
    return -1, 0.0


def cluster_faces(descriptors, threshold=0.5):
    return dlib.chinese_whispers_clustering(descriptors, threshold)


class Face:
    def __init__(self, encoding, id=None, cache=False, path=None):
        if not id:
            self.id = uuid.uuid4()
        else:
            self.id = id

        if not path and not cache:
            raise RuntimeError("face is not cache and has not path")
        self.path = path
        self.cache = cache
        self.encoding = encoding
