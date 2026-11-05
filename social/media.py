import cloudinary
from django.conf import settings

print("Cloudinary settings:", {
    "cloud_name": settings.CLOUDINARY_STORAGE.get("CLOUD_NAME"),
    "api_key_configured": bool(
        settings.CLOUDINARY_STORAGE.get("API_KEY")
    ),
    "api_secret_configured": bool(
        settings.CLOUDINARY_STORAGE.get("API_SECRET")
    ),
})

cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=settings.CLOUDINARY_STORAGE["API_KEY"],
    api_secret=settings.CLOUDINARY_STORAGE["API_SECRET"],
)

import cloudinary.api

result = cloudinary.api.ping()
print(result)