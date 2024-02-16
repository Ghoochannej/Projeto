from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
ATIVO = ''
contadorAtivos = 1 # ex: BHIA3, RZAT11, GRWA11, etc...
contadorProdutos = 1 # ex: Bens Industriais, Consumo Cíclico, etc... 
temp_lista = []
driver = webdriver.Chrome()
driver.get("https://www.infomoney.com.br/cotacoes/empresas-b3/")
driver.implicitly_wait(10)
driver.maximize_window()
assert "Empresas B3" in driver.title

for item in driver.find_elements(By.CLASS_NAME, 'list-companies'):
# for para todos a lista de 'tipos de cia', ex: Bens Industriais, Consumo Cíclico, etc...    
    while(1):
        # loop para ele pegar todos as empresas daquele grupo, até que ele não ache e solte uma exception
        # Quando a exception acontece o contador é incrementado +1 e volta a buscar as empresas, só que do prox grupo
        try:
            EMPRESA = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div['+str(contadorProdutos)+']/div[2]/table/tbody/tr['+str(contadorAtivos)+']/td[1]').text
            temp_ATIVO = driver.find_elements(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div["+str(contadorProdutos)+"]/div[2]/table/tbody/tr["+str(contadorAtivos)+"]/td[@class='strong']")

            for i in temp_ATIVO:
                ATIVO = ATIVO + ' '+i.text
            
            # Aqui foi necessário utilizar uma lógica específica para a coluna 'ATIVO'
            # Em alguns casos a empresa possui mais de um 'ATIVO' (Karsten, CTKA4F CTKA3F CTKA4 CTKA3)
            # Como esses ativos estavam todos eles numa unica classe 'strong' então eu peguei uma lista deles e depois concatenei

            print(EMPRESA+ ' | ' +ATIVO)
            # print para mostrar alguma coisa durante a execução

            tabela = {
                'EMPRESA': EMPRESA,
                'ATIVO':ATIVO
            }
            # obj que vai virar um dataframe e depois .csv

            temp_lista.append(tabela)
            df = pd.DataFrame(temp_lista)

    
            contadorAtivos = contadorAtivos + 1
            ATIVO = ''
        except Exception as error:
            contadorAtivos = 1
            break
    contadorProdutos = contadorProdutos + 1

df.to_csv('arquivo.csv', index=False)
# momento de criação do .csv com base no dataframe populado
driver.close()