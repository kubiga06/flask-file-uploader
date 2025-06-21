from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for
import os
from urllib.parse import unquote

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Transfer File Modern</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background-color: #f5f7fa;
            font-family: 'Segoe UI', sans-serif;
        }
        .upload-area {
            border: 2px dashed #c0c0c0;
            border-radius: 1rem;
            padding: 2rem;
            background-color: #fff;
            text-align: center;
            margin-bottom: 2rem;
        }
        .file-card {
            background-color: white;
            border-radius: 1rem;
            padding: 1rem 1.2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .filename {
            word-break: break-all;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        .file-actions {
            display: flex;
            justify-content: flex-start;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .btn-sm {
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
<div class="container py-4">
    <h2 class="text-center mb-4"><i class="bi bi-cloud-upload-fill text-primary"></i> Transfer File</h2>

    <form method="POST" enctype="multipart/form-data" class="upload-area">
        <label class="form-label fs-5 mb-3">Pilih file untuk diunggah:</label>
        <input type="file" name="file" multiple class="form-control mb-3" required>
        <button class="btn btn-primary" type="submit"><i class="bi bi-upload"></i> Upload</button>
    </form>

    <h4 class="mb-3"><i class="bi bi-folder-fill"></i> File Tersimpan</h4>
    {% if files %}
        {% for filename in files %}
        <div class="file-card">
            <div class="filename"><i class="bi bi-file-earmark-text"></i> {{ filename }}</div>
            <div class="file-actions">
                <a href="/uploads/{{ filename }}" class="btn btn-sm btn-success">Download</a>
                <a href="/delete/{{ filename }}" class="btn btn-sm btn-danger" onclick="return confirm('Hapus file {{ filename }}?');">Hapus</a>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <p class="text-muted">Belum ada file diunggah.</p>
    {% endif %}
</div>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_files = request.files.getlist('file')
    for uploaded_file in uploaded_files:
        if uploaded_file and uploaded_file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    filename = unquote(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/delete/<path:filename>')
def delete_file(filename):
    filename = unquote(filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return redirect(url_for('index'))
    else:
        return f"File {filename} not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
