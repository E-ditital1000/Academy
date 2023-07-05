import os
import cloudinary.uploader
import cloudinary.api
from django.shortcuts import render
from django.http import JsonResponse
from .forms import VideoUploadForm
import imghdr


# Cloudinary configuration
cloudinary.config(
    cloud_name='dhauchzdq',
    api_key='925253475554343',
    api_secret='ZUGD48p7y1_ERNIsK9jIybc2hQg'
)


def handle_video_upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']

            # Validate file format
            if imghdr.what(video) is None:
                return JsonResponse({'error': 'Invalid file format. Only image files are allowed.'})

            # Check video file size
            max_file_size = 50 * 1024 * 1024  # 50 MB
            if video.size > max_file_size:
                return JsonResponse({'error': 'Video file size exceeds the maximum limit (50MB)'})

            # Upload the video file to Cloudinary
            upload_result = cloudinary.uploader.upload_large(
                video,
                resource_type='video',
                folder='your_cloudinary_folder'
            )

            # Handle the upload response
            if 'error' in upload_result:
                return JsonResponse({'error': upload_result['error'].message})
            else:
                # Save the video URL or perform other operations
                video_url = upload_result['secure_url']
                # ... Save the video URL or perform other operations ...

                return JsonResponse({'success': 'Video uploaded successfully', 'url': video_url})
        else:
            return JsonResponse({'error': 'Invalid form data'})
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video_form.html', {'form': form})
