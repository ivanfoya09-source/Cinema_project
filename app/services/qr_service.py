import os
import uuid

import qrcode


class QRService:

    UPLOAD_DIR = "app/static/qrcodes"

    @classmethod
    def generate(cls, text: str):

        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)

        filename = f"{uuid.uuid4()}.png"

        path = os.path.join(
            cls.UPLOAD_DIR,
            filename,
        )

        img = qrcode.make(text)

        img.save(path)

        return f"/static/qrcodes/{filename}"