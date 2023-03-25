from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import numpy as np
from vpython import *
app = Flask(__name__)
CORS(app)

@app.route('/model', methods=['GET'])
def index():
    vertices,faces = create_dyson_sphere()
    return jsonify({
        'vertices': vertices,
        'faces': faces })

def create_dyson_sphere(radius=1.0, subdivisions=2):
    def icosphere(radius, subdivisions):
        t = (1.0 + np.sqrt(5.0)) / 2.0

        vertices = np.array([
            [-1, t, 0],
            [1, t, 0],
            [-1, -t, 0],
            [1, -t, 0],

            [0, -1, t],
            [0, 1, t],
            [0, -1, -t],
            [0, 1, -t],

            [t, 0, -1],
            [t, 0, 1],
            [-t, 0, -1],
            [-t, 0, 1],
        ])

        faces = np.array([
            [0, 11, 5],
            [0, 5, 1],
            [0, 1, 7],
            [0, 7, 10],
            [0, 10, 11],

            [1, 5, 9],
            [5, 11, 4],
            [11, 10, 2],
            [10, 7, 6],
            [7, 1, 8],

            [3, 9, 4],
            [3, 4, 2],
            [3, 2, 6],
            [3, 6, 8],
            [3, 8, 9],

            [4, 9, 5],
            [2, 4, 11],
            [6, 2, 10],
            [8, 6, 7],
            [9, 8, 1],])

        for _ in range(subdivisions):
            new_faces = []

            for face in faces:
                v1, v2, v3 = vertices[face]

                v12 = np.add(v1, v2) / 2
                v23 = np.add(v2, v3) / 2
                v31 = np.add(v3, v1) / 2

                v12 /= np.linalg.norm(v12)
                v23 /= np.linalg.norm(v23)
                v31 /= np.linalg.norm(v31)



                v12_idx = len(vertices)
                v23_idx = v12_idx + 1
                v31_idx = v12_idx + 2

                vertices = np.vstack([vertices, v12, v23, v31])

                new_faces.extend([
                    [face[0], v12_idx, v31_idx],
                    [v12_idx, face[1], v23_idx],
                    [v31_idx, v23_idx, face[2]],
                    [v12_idx, v23_idx, v31_idx],])

            faces = np.array(new_faces)

        vertices *= radius

        return vertices, faces

    vertices, faces = icosphere(radius, subdivisions)
    return vertices.tolist(), faces.tolist()


@app.route('/')
def serve_index():
    ##change the pathway when you copy the code
    return send_from_directory('C:\\Users\\yunus\\PycharmProjects\\DysonSphere\\templates','index.html')
if __name__ == '__main__':
    app.run(debug=True)

