import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd



def findContentByClass(atributo, clase, arrayData, soup):
    if(atributo == ''):
        items = soup.find_all(class_=clase, partial=False)
    else:
        items = soup.find_all(atributo, class_=clase, partial=False)
    for item in items:
        arrayData.append(str(item.text))

def findProfile(item,item2,arrayData):
    match_senior=re.search(r'Senior',item)
    match_junior=re.search(r'Junior',item)
    match_intership=re.search(r'Internship',item)
    
    try:
    
        if match_senior:
            profileArray.append(str(match_senior.group()))
            return
        else:
            match_senior_des=re.search(r'Senior',item2)
            if match_senior_des:    
                arrayData.append(str(match_senior_des.group()))
                return
        if match_intership:
            arrayData.append(str(match_intershit.group()))
        else:
            match_intership_des=re.search(r'Intership',item2)
            if match_intership_des:
                arrayData.append(str(match_intershit_des.group()))
                return
        if match_junior:
            arrayData.append(str(match_junior.group()))
        else:
            match_junior_des=re.search(r'Junior',item2)
            if match_junior_des:
                arrayData.append(str(match_junior_des.group()))
            else:
                arrayData.append("Undefined")
                return
    except:
        arrayData.append("Not found")
    
    
def findHrefByClass(clase, arrayData, soup):
    items = soup.find_all('a', class_=clase, partial=False)
    for item in items:
        href = item.get('href')
        href = 'https://es.indeed.com' + str(href)
        arrayData.append(href)
    

def getCompanyName(clase, arrayData, soup):
    items = soup.find_all(class_="jobsearch-SerpJobCard", partial=False)

    for item in items:
        name = item.find(class_=clase)
        s = str(name)
        cleanHtml = re.sub('<[^>]+>', '', s).strip()
        arrayData.append(cleanHtml)
    

def fecha_publicacion(item,arrayData):
    match=re.search(r'hace [0-9]{1,} días',item)
    if match:
        literal=str(match.group())
        ss=(literal[5:7])
        final=ss.strip()
        arrayData.append(final)
    else:
        arrayData.append("not found")

def get_jobs():
    error="Ninguno"
    try:
        CompanyArray = []
        locationArray = []
        linkArray = []
        jobtitleArray = []
        fechasArray=[]
        descriptionArray=[]
        profileArray=[]

        
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(10)
        browser.get('https://es.indeed.com/ofertas?q=data+scientist&l=Barcelona%2C+Barcelona+provincia')
        browser.maximize_window()
        soup=BeautifulSoup(browser.page_source,'html5lib')
        #Obtenemos el numero de paginas de nuestro navegador
        paginas = soup.find(id='searchCountPages')
        res = str(paginas).split()
        numElements = int(res[5])
        numPages = numElements/14 * 10
        # print(URL[75:]) substring from "start" to final
        start = 0
        while start < 5:
            soup=BeautifulSoup(browser.page_source,'html5lib')
            tabla=soup.find("table",id="resultsBody")
            body=tabla.find('td',id='resultsCol')
            nombre_empleo=body.find_all("a",class_='jobtitle')
            getCompanyName("company", CompanyArray, soup)
            findContentByClass('', "accessible-contrast-color-location", locationArray, soup)
            findHrefByClass("jobtitle", linkArray, soup)
            iterator=1
            for item in nombre_empleo:
                try:
                    WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.XPATH,f"//div[contains(@class,'clickcard')][{iterator}]"))).click()
                    detalles =  WebDriverWait(browser,20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label  ='Detalles del empleo']"))).text
                    if(detalles not in descriptionArray):
                        cabecera = str(item.text)
                        jobtitleArray.append(cabecera.replace('\n',""))
                        descripcion = detalles.rstrip('\n')
                        descriptionArray.append(descripcion.replace('\n'," "))
                        fecha_publicacion(detalles,fechasArray)
                        findProfile(cabecera.replace('\n',""),descripcion.replace('\n'," "),profileArray)
                    iterator+=1
                    time.sleep(2)
                except:
                    error="No soy un robot"
                    break
                    
                if(iterator<len(nombre_empleo)):
                    next_element=browser.find_element_by_xpath(f"//div[contains(@class,'clickcard')][{iterator}]")
                    browser.execute_script("return arguments[0].scrollIntoView();", next_element)
                    time.sleep(2)
            if error=="No soy un robot":
                break
                       
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.XPATH,'//ul[@class="pagination-list"]//li/a[contains(@aria-label,"Siguiente")]'))).click()
            time.sleep(4)
            #Buscamos el boton de cerrar y hacemos un try catch para cerrar el pop up si aparece.
            try:
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Cerrar"]'))).click()
            except:
                print("No pop up encontrado.")
            iterator=1
            start+=1
            
        data = {'title': jobtitleArray, 'company': CompanyArray, 'location': locationArray, 'URL': linkArray, 'Date':fechasArray , 'Descripcion' : descriptionArray,'Profile':profileArray}
        df = pd.DataFrame(data)
        df.to_csv('indeedScrap.csv', index=False)
        print(df)
        print("Finalizado, se han obtenido " % str(len(jobtatitleArray)) + " empleos mediante Selenium.") 
        
    except:
        print("No soy un robot ha saltado.")
        #if start==0:
        #    return
        
        print(len(jobtitleArray))
        print(len(CompanyArray))
        print(len(locationArray))
        print(len(linkArray))
        print(len(fechasArray))
        print(len(descriptionArray))
        print(len(profileArray))
        
        if(len(jobtitleArray)<len(CompanyArray)):
            CompanyArray=CompanyArray[0:len(jobtitleArray)]
            locationArray=locationArray[0:len(jobtitleArray)]
            linkArray=linkArray[0:len(jobtitleArray)]
        
        data = {'title': jobtitleArray, 'company': CompanyArray, 'location': locationArray, 'URL': linkArray, 'Date':fechasArray , 'Descripcion' : descriptionArray, 'Profile':profileArray }
        df = pd.DataFrame(data)
        df.to_csv('indeedScrap.csv', index=False)
        print(df)
        
if __name__ == '__main__':
    
    trabajos = get_jobs()
    

