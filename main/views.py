import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from static.project.final3 import Camera, RoomSegmentation


# Create your views here.

def main(request):
    samples = os.listdir(os.path.join(settings.ROOM_SEGMENTATION_DIR, 'results'))
    uploaded = False
    filename = ""
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        uploaded = True

    return render(request, 'home.html', {"samples": samples, "uploaded": uploaded, "upload": filename})


def sample_view(request, map_name):
    print(map_name)
    images = os.listdir(os.path.join(settings.ROOM_SEGMENTATION_DIR, 'results', map_name))
    images.sort(key=lambda x: int(x[0]))
    images = [os.path.join('project', 'results', map_name, i) for i in images]
    print(images)
    return render(request, "sample.html", {"images": images})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
    return render(request, 'core/simple_upload.html')


def room_segmentation(request, file_name):
    print(file_name)
    return render(request, 'Run.html')


@csrf_exempt
def xhr_test(request):
    method = request.POST.get("method")
    url = request.POST.get("url")
    images = None;
    if method == "cam":
        print(os.path.join(settings.MEDIA_ROOT), url)
        print(os.path.join(settings.MEDIA_ROOT, url))
        camera = Camera(os.path.join(settings.MEDIA_ROOT, url))
        img = camera.detect_map()[0]
        camscanner = RoomSegmentation(m=1, b=5, min_dist=1600, min_l=100,
                                      image_file=img, image_name=url,
                                      base_dir=os.path.join(settings.ROOM_SEGMENTATION_DIR, 'site_results'))
        camscanner.run(url.split(".")[0])
    elif method == "map":
        office_d = RoomSegmentation(m=1, b=15, min_dist=1600, min_l=100,
                                    image_file=None, image_name=url,
                                    base_dir=os.path.join(settings.ROOM_SEGMENTATION_DIR, 'site_results'),
                                    media_upload=os.path.join(settings.MEDIA_ROOT, url))
        print("Running")
        office_d.run(url.split(".")[0])
        print("END",os.path.join(settings.ROOM_SEGMENTATION_DIR, 'site_results', url.split(".")[0]))
        images = os.listdir(os.path.join(settings.ROOM_SEGMENTATION_DIR, 'site_results', url.split(".")[0]))
        print(images)
        images.sort(key=lambda x: int(x[0]))
        images = [os.path.join('project', 'site_results', url.split(".")[0], i) for i in images]
        print(images)

    return JsonResponse({"method": "gooz","images":images})
