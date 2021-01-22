import csv
import random
import uuid
import json
import http
import requests
import datetime


def getName():
    with open ("./Names.csv") as filecsv:
        csv_reader = csv.reader(filecsv)    
        lista = []
        for row in csv_reader:        
            lista.append(row[0])
    return lista

def getSurname():
    with open ("./engwales_surnames.csv", encoding='ISO-8859-1') as filecsv:
        csv_reader = csv.reader(filecsv)    
        lista = []
        for row in csv_reader:        
            lista.append(row[0])
    return lista

def getTitle():
    with open ("./movies_title_words.csv") as filecsv:
        csv_reader = csv.reader(filecsv)  
        lista = []
        for row in csv_reader:        
            lista.append(row[0])
        return lista
def getTitleFromList(lista):
    parole = random.randint(2,5)
    i = 0
    while i < parole:
        if i ==0:
            titolo = '' + random.choice(lista)
            i += 1
             
        else:
            titolo = titolo + ' ' + random.choice(lista)
            i += 1
    return titolo   

def reverseTitle(title):
    arr = []
    arr = title.rsplit(' ')    
    i = 1
    while i <= len(arr):
        if i == 1:
            reverse = arr[len(arr)-i]
            i += 1
        else:
            reverse = reverse + ' ' + arr[len(arr)-i]
            i += 1
    return reverse

def getYear():
    return(random.randint(1950,2020))

def invertDirector(director):
    lista = []
    lista = director.rsplit(' ')    
    return lista[1] + ' ' + lista[0]

def cutDirector (director):
    lista = []
    lista = director.rsplit(' ')
    return director[0] + '. ' + lista[1]

def sendFile (outputFile):
   url = "https://search-matching-engine-uv2ckzsmrpytmltjko7x5jf4ra.eu-west-1.es.amazonaws.com/massive_test_index/_bulk"
   header = {'content-type': 'application/json'}
   r= requests.post(url, headers=header, data=outputFile)
   return r.status_code
   


    
#### file
iterator = 0 
bulk = ''
bulkNumber = 0
maxNum = 12000
titoli = getTitle()
nomi = getName()
cognomi = getSurname()
start = datetime.datetime.now()
print('Start: ' + str(start))
while iterator < maxNum:
    testaCroce = [0,1]
    masterId = str(uuid.uuid4())    
    providerDataList = []
    
    ######### header file
    outputFile = {'masterUUID': masterId}
    prov = random.randint(1,2)
    y = 0
    while y < prov :
        providerDataDict = {'UUID' : masterId, 'entitySubType' : 'programme'}
        if y == 0:
            providerInfo = {'providerName' : 'DataTV', 'providerID' : 'DATATV_' + str(random.randint(10,500))}
        else:
            providerInfo = {'providerName' : 'Mediaset', 'providerID' : 'MS_' + str(random.randint(10,500))}
        providerDataDict['providerInfo'] = providerInfo

        ######### titles
        title = getTitleFromList(titoli)    
        alternative1 = 'The ' + title    
        alternative2 = reverseTitle(title)
        alternative3 = title + ' - ' + random.choice(titoli)        
        listaTitoli = [title,alternative1,alternative2,alternative3]
        titleList = []
        titleDict = {}
        sched = random.randint(1,3)
        i = 0
        lista = listaTitoli[:]
        while i < sched : 
            scelta = random.choice(lista)
            titleDict = {'title': scelta, 'type':'sched'}
            titleList.append(titleDict)
            lista.remove(scelta)
            i += 1    
        enrich = random.randint(0,4)
        x = 0
        while x < enrich :    
            scelta = random.choice(listaTitoli)
            titleDict = {'title': scelta, 'type':'enrich'}
            titleList.append(titleDict)
            listaTitoli.remove(scelta)     
            x += 1
        providerDataDict['titles'] = titleList  

        ######### directors
        nameSurname = random.choice(nomi) + ' ' + random.choice(cognomi)
        listaDirectors = [nameSurname,invertDirector(nameSurname),cutDirector(nameSurname)]
        directorsList = []
        directorsDict = {}      
        sched = random.randint(1,2)
        i = 0
        lista = listaDirectors[:]
        while i < sched : 
            scelta = random.choice(lista)
            directorsDict = {'director': scelta, 'type':'sched'}
            directorsList.append(directorsDict)
            lista.remove(scelta)
            i += 1        
        enrich = random.randint(0,2)
        x = 0
        while x < enrich :    
            if x ==0:                
                directorsDict = {'director':listaDirectors[x], 'type':'enrich'}
                directorsList.append(directorsDict)     
                x += 1
            else:
                directorsDict = {'director':random.choice(nomi) + ' ' + random.choice(cognomi), 'type':'enrich'}
                directorsList.append(directorsDict)     
                x += 1
        providerDataDict['directors'] = directorsList

        ######### years
        year = getYear()
        productionYearList = [{'productionYear': year, 'type':'sched'}]
        if (random.choice(testaCroce) == 1):
            productionYearDict = {'productionYear': year, 'type':'enrich'}
            productionYearList.append(productionYearDict)
        providerDataDict['productionYears'] = productionYearList

        ######### aggiungo alla lista il dizionario appena creato
        providerDataList.append(providerDataDict)
        y +=1

    ######### ultime operazioni prima di inviare il file 
    outputFile['providerData'] = providerDataList       
    bulk += '{"index": {"_index": "massive_test_index"}}' + '\n' + str(json.dumps(outputFile)) + '\n'
    bulkNumber += 1
    if bulkNumber == 500:
        print(sendFile(bulk))
        #print(bulk)
        bulk = ''        
        bulkNumber = 0    
    iterator += 1
end = datetime.datetime.now()
print('End: ' + str(end))
print('Duration: ' + str(end - start))   

