from flask import Flask, jsonify, render_template
from flask_cors import CORS
import numpy as np

app = Flask(__name__, template_folder='C:\\Users\\yunus\\Desktop\\dyson_sphere', static_folder='static') # user needs to change path
CORS(app)

@app.route('/model', methods=['GET'])
def model():
    vertices, faces = create_dyson_sphere(radius=10.0, subdivisions=3)
    return jsonify({'vertices': vertices, 'faces': faces})

def create_dyson_sphere(radius=10.0, subdivisions=3):
    def icosphere(radius, subdivisions):
        t = (1.0 + np.sqrt(5.0)) / 2.0

        vertices = np.array([
            [-1,  t,  0],
            [ 1,  t,  0],
            [-1, -t,  0],
            [ 1, -t,  0],
            [ 0, -1,  t],
            [ 0,  1,  t],
            [ 0, -1, -t],
            [ 0,  1, -t],
            [ t,  0, -1],
            [ t,  0,  1],
            [-t,  0, -1],
            [-t,  0,  1],
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
            [9, 8, 1],
        ])

        vertices = np.array([v/np.linalg.norm(v) for v in vertices])

        for _ in range(subdivisions):
            midpoint_cache = {}
            new_faces = []
            vertices_list = list(vertices)

            def get_midpoint(i, j):
                key = tuple(sorted((i, j)))
                if key in midpoint_cache:
                    return midpoint_cache[key]
                v = (vertices[i] + vertices[j]) / 2
                v = v / np.linalg.norm(v)
                vertices_list.append(v)
                index = len(vertices_list) - 1
                midpoint_cache[key] = index
                return index

            for tri in faces:
                i0, i1, i2 = tri
                a = get_midpoint(i0, i1)
                b = get_midpoint(i1, i2)
                c = get_midpoint(i2, i0)
                new_faces.extend([
                    [i0, a, c],
                    [i1, b, a],
                    [i2, c, b],
                    [a, b, c]
                ])
            vertices = np.array(vertices_list)
            faces = np.array(new_faces)

        vertices *= radius
        return vertices, faces

    vertices, faces = icosphere(radius, subdivisions)
    return vertices.tolist(), faces.tolist()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
