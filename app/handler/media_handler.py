import os
from werkzeug.utils import secure_filename
import cloudinary.uploader
import cloudinary

# 🧠 Cloudinary Configuration (set this once in your app)
cloudinary.config(
    cloud_name="dq1ocnjpe",
    api_key="122838318438894",
    api_secret="MqO8XJ8BxmB1hy5h_XOls3r-ZRU"
)

class MediaHandler:
    def __init__(self, file, upload_dir="static/uploads", allowed_extensions=None, use_cloud=False):
        self.file = file
        self.upload_dir = upload_dir
        self.allowed_extensions = allowed_extensions or {"png", "jpg", "jpeg", "gif", "mp4", "wmv", "webp", "avi", "mpeg"}
        self.filename = secure_filename(file.filename) if file else None
        self.use_cloud = use_cloud
        self.cloud_url = None

        if not use_cloud:
            os.makedirs(upload_dir, exist_ok=True)

    def is_allowed(self):
        if not self.filename:
            return False
        ext = self.filename.rsplit('.', 1)[-1].lower()
        return '.' in self.filename and ext in self.allowed_extensions

    def save(self, custom_name=None):
        if not self.is_allowed():
            raise ValueError("File type not allowed")

        if self.use_cloud:
            result = cloudinary.uploader.upload(self.file)
            self.cloud_url = result.get("secure_url")
            return self.cloud_url, None  # cloud_url, no filename
        else:
            name = custom_name or self.filename
            save_path = os.path.join(self.upload_dir, name)
            self.file.save(save_path)
            self.filename = name  # update if custom_name used
            return save_path, name

    def get_url(self, app_root=""):
        if self.use_cloud:
            return self.cloud_url
        return os.path.join(app_root, self.upload_dir, self.filename).replace("\\", "/")

    def remove(self, filename=None, filepath=None):
        if self.use_cloud:
            raise NotImplementedError("Remove not supported for cloud uploads")

        name = filename or self.filename
        gpath = filepath or self.upload_dir
        if not name:
            raise ValueError("No filename specified for removal")

        path = os.path.join(gpath, name)
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
