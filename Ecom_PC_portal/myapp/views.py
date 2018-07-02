# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from Ecom_PC_portal.myapp.models import Document
from Ecom_PC_portal.myapp.forms import DocumentForm
import time
import subprocess
from Ecom_PC_portal.myapp import label_image
from Ecom_PC_portal.myapp import color_detector
import os
import json
import ast


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Document.objects.all().delete()
            newdoc = Document(docfile=request.FILES['docfile'])
            print(newdoc.docfile.url)
            print("docfile",request.FILES['docfile'])

            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    if len(documents) != 0:        
        # print("documents::",documents)
        path_for_prediction = "/Users/coviam/Documents/Ecom_PC_portal"+documents[len(documents)-1].docfile.url
        print ("path_for_prediction",path_for_prediction)
        path = documents[len(documents)-1].docfile.url
    
        for doc in documents:
            documents.delete()
        # Render list page with the documents and the form
        # change categories to actual categories returned from predictor
        # change the color change to the predicted color value
    
        classes_scores,categories,color_codes = get_prediction( path_for_prediction)

        return render(
            request,
            'list.html',
            {'form': form, 'path':path, 'categories':categories
            , 'color':color_codes, 'classes_scores':classes_scores}
        )
    else:
        return render(
            request,
            'list.html',
            {'form': form, 'path':"", 'categories':["","",""]
            , 'color':"", 'classes_scores':zip([""],[""])}
        )

# get prediction from the trained model and return categories list, color - string,
# and two list for all categories name combined and their prooperties
def get_prediction(image_path = None):
    path = os.path.dirname(os.path.abspath(__file__))
    # print("path:{}".format(path))
    # print("image_path:{}".format(image_path))
    #run python command to fetch prediction.
    #if not image_path:
    output = label_image.predict(path, image_path)
    color =color_detector.detect_color(image_path)

    print("color is")
    print(color)

    # color_codes = []
    # for item in color:
    #     color_codes.append('#%02x%02x%02x' % (int(item[0]), int(item[1]), int(item[2])))
    # print(color_codes)
    # print(type(color_codes))
    color= '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))
    # print("output is :{}".format(output))
    label_file = open('/Users/coviam/Documents/Ecom_PC_portal/Ecom_PC_portal/myapp/flipkart_labels1.txt','r')
    labels = eval(label_file.read())
    scores=[]
    classes=[]
    for out in output:
        scores.append(next(iter(out.values())))
        classes.append(next(iter(out)))

    cat = labels[next(iter(output[0]))]
    categories = ast.literal_eval(cat)
    classes_scores = zip(classes, scores)
    return classes_scores,categories,color
