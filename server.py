from flask import Flask, request, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Dosya bulunamadı!", 400

    file = request.files["file"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return f"Fotoğraf kaydedildi: {filename}", 200

@app.route("/gallery")
def gallery():
    files = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    html = "<h1>📷 Yüklenen Fotoğraflar</h1>"
    for file in files:
        html += f'<div><img src="/uploads/{file}" width="300"><p>{file}</p></div><hr>'
    return html

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
