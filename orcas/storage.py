import os
import numpy as np
import time
import glob


class Storage:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)

    def has_faces(self):
        return len(glob.glob(os.path.join(self.path, "*.dump")))

    def scan_faces(self):
        output = []
        for dump_file in glob.glob(os.path.join(self.path, "*.dump")):
            face_id = dump_file[dump_file.rindex("/") + 1:-5][:36]
            face_encoding = np.loadtxt(dump_file)
            output.append([face_encoding, face_id])

        return output

    def save_face(self, face):
        prefix = "{}".format(face.id)
        number = len(glob.glob(os.path.join(self.path, prefix + "*.dump")))
        np.savetxt(os.path.join(self.path, "{}-{}-{}.dump".format(prefix, int(time.time() / 10000) * 10, number)),
                   face.encoding)
