import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

edge_options = Options()
#edge_options.use_chromium = True    
#edge_options.headless=True
edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')
edge_options.add_argument("--disable-extensions");
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
#edge_options.add_argument('--log-level=3')

#Here you set the path of the profile ending with User Data not the profile folder
edge_options.add_argument("user-data-dir=C:\\Users\\kiko\\AppData\\Local\\Microsoft\\Edge\\User Data"); 

#Here you specify the actual profile folder    
edge_options.add_argument("profile-directory=Default");

edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
nav=webdriver.Edge(options = edge_options)

nav=webdriver.Edge(options = edge_options)
aURL = 'http://estatisticas.cetip.com.br/astec/series_v05/paginas/lum_web_v05_template_informacoes_di.asp?str_Modulo=completo&int_Idioma=1&int_Titulo=6&int_NivelBD=2'
nav.get(aURL)

current_url = nav.current_url

# We want the last day data only
#
To_Day = nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[1]/div[2]/div/div[4]/input').get_attribute("value")
To_Month =nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[1]/div[2]/div/div[5]/input').get_attribute("value")
To_Year=nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[1]/div[2]/div/div[6]/input[1]').get_attribute("value")

From_Day=nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[1]/div[2]/div/div[1]/input')
From_Day.clear()
From_Day.send_keys(To_Day) #, Keys.TAB)

From_Month=nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[1]/div[2]/div/div[2]/input')
From_Month.clear()
From_Month.send_keys(To_Month)

From_Year=nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[1]/div[2]/div/div[3]/input')
From_Year.clear()
From_Year.send_keys(To_Year)

button = nav.find_element(By.XPATH, '//*[@id="col_esq"]/div/form/div[6]/div/a[2]')
button.click() 

WebDriverWait(nav, 15).until(EC.url_changes(current_url))

new_url = nav.current_url

#CDIs = []
CDIs = nav.find_elements(By.CLASS_NAME, 'ConsultaDados_R_02')

CDI_Date = datetime.strptime(CDIs[0].text,'%d/%m/%Y').date()
CDI_Operacoes = int(CDIs[1].text)
CDI_Volume = float(CDIs[2].text.replace('.',''))
CDI_Media = float(CDIs[3].text.replace(',','.'))
CDI_Fator = float(CDIs[4].text.replace(',','.'))
CDI_Minima = CDIs[5].text.strip()
CDI_Minima = CDI_Media if CDI_Minima == '-' else float(CDI_Minima.replace(',','.'))
CDI_Maxima = CDIs[6].text.strip()
CDI_Maxima = CDI_Media if CDI_Maxima == '-' else float(CDI_Maxima.replace(',','.'))
CDI_Moda = CDIs[7].text.strip()
CDI_Moda = CDI_Media if CDI_Moda == '-' else float(CDI_Moda.replace(',','.'))
CDI_DesvPadr = CDIs[8].text.strip()
CDI_DesvPadr = 0.00 if CDI_DesvPadr == '-' else float(CDI_DesvPadr.replace(',','.'))
CDI_TxSelic = float((CDIs[9].text).replace(',','.'))

CDI_Date1 = datetime.today()

CDI_fDate = datetime.strftime(CDI_Date, "%m/%d/%Y")
CDI_fDate1 = datetime.strftime(CDI_Date1, "%m/%d/%Y")

htm = f"""<html><head></head><body><p><b>CDI</b> - Certificado de Depósito Interbancário<br></p><table border='0'>
<tr><td>Data</td><td>Operações</td><td>Volume</td><td>Média</td><td>Fator</td><td>Mínima</td><td>Máxima</td><td>Moda</td><td>DsvPdr</td><td>Taxa Selic</td>
</tr><tr><td>{CDI_fDate}</td>
     <td>{CDI_Operacoes}</td>
     <td>{"{:.0f}".format(CDI_Volume)}</td>
     <td>{CDI_Media}</td>
     <td>{CDI_Fator}</td>
     <td>{CDI_Minima}</td>
     <td>{CDI_Maxima}</td>
     <td>{CDI_Moda}</td>
     <td>{CDI_DesvPadr}</td>
     <td>{CDI_TxSelic}</td>
</tr><tr><td>{CDI_fDate1}</td>
     <td></td>
     <td></td>
     <td>{CDI_Media}</td>
     <td></td>
     <td></td>
     <td></td>
     <td></td>
     <td></td>
     <td></td>
</tr></table></body></html>
"""

print (htm)

nav.quit()


