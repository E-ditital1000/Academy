
import os
import cloudinary.uploader
import cloudinary.api
import imghdr


# Cloudinary configuration
cloudinary.config(
    cloud_name='dhauchzdq',
    api_key='925253475554343',
    api_secret='ZUGD48p7y1_ERNIsK9jIybc2hQg'
)

# Path to your static files directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')

# Iterate over files in the static directory
for root, dirs, files in os.walk(static_dir):
    for file in files:
        file_path = os.path.join(root, file)

        # Validate file format
        if imghdr.what(file_path) is None:
            print(f"Skipping file {file} due to invalid image format")
            continue

        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(file_path, folder='your_cloudinary_folder')
        print(f"Uploaded file {file}: {upload_result['secure_url']}")
