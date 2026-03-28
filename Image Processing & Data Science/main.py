import matplotlib.pyplot as plt
import imageio.v3 as iio
import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, render_template, request, redirect, url_for
import os


app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_colors(image_path, k=10):
    img = iio.imread(image_path)

    if img.shape[2] == 4:
        img = img[:, :, :3]

    pixels = img.reshape(-1, 3)

    sample_size = 10000
    if len(pixels) > sample_size:
        indices = np.random.choice(len(pixels), sample_size, replace=False)
        pixels = pixels[indices]

    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)

    labels = kmeans.labels_
    counts = np.bincount(labels)

    sorted_indices = np.argsort(counts)[::-1]
    colors = colors[sorted_indices]
    counts = counts[sorted_indices]

    total = counts.sum()
    percentages = (counts / total) * 100

    # Convert to HEX
    def rgb_to_hex(c):
        return '#{:02x}{:02x}{:02x}'.format(c[0], c[1], c[2])

    hex_colors = [rgb_to_hex(c) for c in colors]

    return hex_colors, percentages


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["image"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            hex_colors, percentages = extract_colors(filepath)

            return render_template(
                "index.html",
                colors = zip(hex_colors, percentages),
                image=filepath
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)



