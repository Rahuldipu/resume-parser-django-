# Create your views here.
import spacy
import pandas as pd
from pyresparser import ResumeParser
spacy.load('en_core_web_sm')


from django.shortcuts import render
from .models import FileData
from django.conf import settings
import os


def home(request):
    return render(request, "index.html")


def result(request):
    df = pd.DataFrame()
    if request.method == 'POST':
        resume_file = request.FILES.getlist('test')
        for f in resume_file:
            res_obj = FileData(resume_file=f)
            res_obj.save()
        filelist = os.listdir('media/resumes/')
        k = 1
        for j in filelist:
            print(type(j))
            if j != ".ipynb_checkpoints":
                print('resume ' + str(k) + ' processing')
                data = ResumeParser('media/resumes/' + j).get_extracted_data()
                for i in data:
                    if type(data[i]) == list:
                        listToStr = ','.join([str(elem) for elem in data[i]])
                        data[i] = listToStr
                df = df.append(data, ignore_index=True)
                k = k + 1
        df = df[["name", "email", "mobile_number", "degree", "experience", "designation", "skills", "college_name","company_names","no_of_pages","total_experience"]]
    physical_files = set()
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root is not None:
        for relative_root, dirs, files in os.walk(media_root):
            for file_ in files:
                # Compute the relative file path to the media directory, so it can be compared to the values from the db
                relative_file = os.path.join(os.path.relpath(relative_root, media_root), file_)
                physical_files.add(relative_file)

    if physical_files:
        for file_ in physical_files:
            os.remove(os.path.join(media_root, file_))

    return render(request, "result.html",{"data":df})
