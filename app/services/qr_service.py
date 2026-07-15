import os
import uuid

import qrcode
import cloudinary.uploader


class QRService:

    UPLOAD_DIR = "temp_qr"

    @classmethod
    def generate(cls, text: str):

        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)

        filename = f"{uuid.uuid4()}.png"

        path = os.path.join(cls.UPLOAD_DIR, filename)

        img = qrcode.make(text)

        img.save(path)

        result = cloudinary.uploader.upload(
            path,
            folder="cinema/qrcodes"
        )

        os.remove(path)

        return result["secure_url"]