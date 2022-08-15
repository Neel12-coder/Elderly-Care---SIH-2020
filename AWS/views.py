from django.shortcuts import render,redirect
from .tasks import job
from django.http import JsonResponse
import urllib.error,urllib.parse,urllib.request
import json
from math import radians, sin, cos, acos
from .models import Patient,HealtParameter
from django.contrib import messages
from sklearn.ensemble import RandomForestClassifier
import pandas
import os
import pickle
import pandas as pd
from sklearn import metrics,svm
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from .models import HealtParameter
from django.db.models import Max
def displayPage(request):
    job(repeat=10,repeat_until = None)
#     df=pd.read_csv(os.path.join(modulePath,'heartPredict.csv')) #put the location of your csv file
#     df = pd.DataFrame(df)
#     X = df.iloc[:,:-1]
#     y = df.iloc[:,-1]
#     model= RandomForestClassifier(n_estimators=100,random_state=0)
#     model.fit(X,y)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1) # 75% training and 25% test
    #cl = svm.SVC(kernel='linear',probability=False) # Linear Kernel
    #cl.fit(X_train, y_train)
#     clf = RandomForestClassifier()
#     clf.fit(X_train,y_train)
#     prediction = clf.predict(X_test)
    #accuracy = accuracy_score(prediction,y_test)

#     filename = 'model4.pickle'
#     pickle.dump(model, open(filename,'wb'))
    # obj = pickle.load(open(filePath, 'rb'))
    # print(obj)

#     vinit = unpickled_model.predict_proba(pd.DataFrame(it))[0][0]
#     print(vinit,"Hii")
    #Predict the response for test dataset
    # y_pred = obj.predict(X_test)
    # cm = confusion_matrix(y_pred,y_test)
    # prfs = precision_recall_fscore_support(y_pred,y_test)
#     print("Accuracy:",metrics.accuracy_score(y_test, prediction))
    # print('Confusion Matrix: ',cm)
    # print('Precision: ', prfs[0])
    # print('Recall:    ', prfs[1])
    # filename = 'model3.pickle'
    # pickle.dump(cl, open(filename,'wb'))
    # print(modulePath + '\heartPredict.csv')
    return render(request,"ElderlyCare/timepass.html")

def testingPage(request):
    api_address = 'https://api.thingspeak.com/channels/957630/feeds.json?api_key=5WCJ31SXSPOQCFFJ'
    uh = urllib.request.urlopen(api_address)
    data = uh.read().decode()
    info = json.loads(data)
    elat = radians(19.046350)
    elon = radians(72.889280)
    pat = Patient.objects.get(id = 1)
    slat = radians(pat.safe_latitude)
    slon = radians(pat.safe_longitude)
    distance = 6371000 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    if pat.safe_distance <= distance:
          return JsonResponse({"message":"Danger"})
    else:
          return JsonResponse({"message":"All Good."})
    return JsonResponse(info)

def testing(request):
    return render(request,"ElderlyCare/relativedash.html")

def landingPage(request):
    return render(request,"ElderlyCare/landing.html")

def dashboardPage(request):
    health= HealtParameter.objects.all()
    current_values = health.order_by('-id')[0]
    context = {
        'health': health,
        'current_values':current_values,
    }
    
    return render(request, 'ElderlyCare/patientdash.html', context)
def locationPage(request):
      if request.method == 'POST':
            pat = Patient.objects.get(id = 1)
            pat.safe_latitude = request.POST.get("latitude")
            pat.safe_longitude = request.POST.get("longitude")
            print(request.POST.get("longitude"),"vinit")
            pat.save()
            messages.success(request, "Application Details successfully updated!")          
            return redirect('locationPage')
      return render(request,"ElderlyCare/relative.html")

def storeCurrentLocation(request,lat,long):
      pat = Patient.objects.get(id = 1)
      pat.safe_latitude = lat
      pat.safe_longitude = long
      pat.save()
      return JsonResponse({"complete":200})

def predictForDoctor(request):
      if request.method == 'POST':
            modulePath = os.path.dirname(__file__)  # get current directory
            filePath = os.path.join(modulePath,'model4.pickle')
            unpickled_model = pickle.load(open(filePath,'rb'))
            if request.POST.get("maxh") != '':
                it = [{'cp':request.POST.get("cp"),'oldpeak':request.POST.get("oldpeak"),'thal':request.POST.get("thal"),'maxh':request.POST.get("maxh"),'age':request.POST.get("age"),'nomv':request.POST.get("nomv"),'chol':request.POST.get("chol"),'restbp':request.POST.get("restbp"),'slope':request.POST.get("slope"),'exang':request.POST.get("exang"),'sex':request.POST.get("sex"),'restecg':request.POST.get("restecg"),
                    'fbs':request.POST.get("fbs")}]
            else:
                parameters = HealtParameter.objects.filter(patient_id =1).order_by('-id')[:10].aggregate(Max('pulse'))
                print(parameters['pulse__max'])
                it = [{'cp':request.POST.get("cp"),'oldpeak':request.POST.get("oldpeak"),'thal':request.POST.get("thal"),'maxh':parameters['pulse__max'],'age':request.POST.get("age"),'nomv':request.POST.get("nomv"),'chol':request.POST.get("chol"),'restbp':request.POST.get("restbp"),'slope':request.POST.get("slope"),'exang':request.POST.get("exang"),'sex':request.POST.get("sex"),'restecg':request.POST.get("restecg"),
                    'fbs':request.POST.get("fbs")}]            
            vinit = unpickled_model.predict_proba(pd.DataFrame(it))[0][0]
            print(vinit,"Hii")
            context = { 
                "percentage":vinit * 100,
            }
            return render(request,"ElderlyCare/showProbability.html",context)
def predictFromDoctor(request):
      if request.method == 'GET':
        return render(request,"ElderlyCare/myform.html")







