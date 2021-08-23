from django.shortcuts import render, redirect
import joblib
from .models import CovidList

reloadCovidModel = joblib.load('./models/covid_svm.pkl')
symptoms_values = []

def index(request):
    return render(request, 'index.html')


def predictCovidDisease(request):
    print(request)
    list = ['bp', 'fever', 'drycough', 'sorethroat', 'runningnose', 'asthma', 'headache', 'heartdisease', 'diabetes', 'hypertension', 'fatigue', 'abroad', 'contact', 'attended', 'visited', 'fam']
    length = len(list)

    # Get all values of on checkboxes
    if request.method == 'POST':
        checked_symptoms = request.POST.getlist('checks')

    # Check if the list of symptoms exists in the checked boxes
    for i in range(length):
        if list[i] in checked_symptoms:
            symptoms_values.append(1)
        else:
            symptoms_values.append(0)

    new_input = [symptoms_values]

    predictedval = reloadCovidModel.predict(new_input)[0]

    #converting predicted val to the results name
    if(predictedval == 1):
        covidval = "COVID Positive"
    else:
        covidval = "COVID Negative"
    context = {'covidval': covidval, 'predictedval': predictedval, 'new_input':new_input}#but still recording the predicted val (0,1,2)
    return render(request, 'index.html', context)


def updateCovidDatabase(request):
    covid = request.POST.get('covidVal')
    obj = CovidList()
    obj.BreathingProblem = symptoms_values[0]
    obj.Fever = symptoms_values[1]
    obj.DryCough = symptoms_values[2]
    obj.Sorethroat = symptoms_values[3]
    obj.RunningNose = symptoms_values[4]
    obj.Asthma = symptoms_values[5]
    obj.Headache = symptoms_values[6]
    obj.HeartDisease = symptoms_values[7]
    obj.Diabetes = symptoms_values[8]
    obj.Hypertension = symptoms_values[9]
    obj.Fatigue = symptoms_values[10]
    obj.AbroadTravel = symptoms_values[11]
    obj.ContactCovidPatient = symptoms_values[12]
    obj.AttendedLargeGathering = symptoms_values[13]
    obj.VisitedPublic = symptoms_values[14]
    obj.FamilyWorkingPublic = symptoms_values[15]
    obj.covid = covid
    obj.save()

    return render(request, 'thankyou.html')