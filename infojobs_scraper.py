import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from excel_utils import salvar_dados_no_excel
from utils import remover_acentos, similaridade

# Função para abrir o navegador, buscar os dados e salvar em Excel
def abrir_navegador_e_interagir_com_site(url: str, nome_empresa: str):
    # Configuração do Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    try:
        # Aceitar cookies
        aceitar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Aceitar']"))
        )
        aceitar_button.click()

        # Inserir o nome da empresa na barra de pesquisa
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtCompany"))
        )
        search_box.clear()
        search_box.send_keys(nome_empresa)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)  # Aguarda o carregamento da página com os resultados

        # Localizar todos os resultados com nomes de empresas
        resultados_empresas = driver.find_elements(By.XPATH, "//div[@class='h3 text-body font-weight-bold']")

        # Normalizar o nome da empresa buscada
        nome_empresa_normalizado = remover_acentos(nome_empresa.lower())

        # Iterar pelos resultados e calcular a similaridade
        melhor_correspondencia = None
        maior_similaridade = 0

        for resultado in resultados_empresas:
            nome_empresa_resultado = resultado.text
            nome_resultado_normalizado = remover_acentos(nome_empresa_resultado.lower())

            similaridade_atual = similaridade(nome_empresa_normalizado, nome_resultado_normalizado)

            # Verificar se a similaridade é maior que a anterior
            if similaridade_atual > maior_similaridade:
                maior_similaridade = similaridade_atual
                melhor_correspondencia = resultado

        # Clicar no nome da empresa com maior similaridade
        if melhor_correspondencia and maior_similaridade > 0.9:  # Definindo um limite de similaridade (ex.: 70%)
            melhor_correspondencia.click()
        else:
            print("Nenhuma empresa correspondente encontrada com alta similaridade.")
            return
        time.sleep(3)  # Aguarda a página da empresa carregar

        # Coletar os dados necessários
        try:
            nome_da_empresa = driver.find_element(By.XPATH, "//h1[@class='header-name']").text
        except NoSuchElementException:
            nome_da_empresa = ""
        try:
            nota_empresa = driver.find_element(By.ID, "ctl00_phMasterPage_cHeader_spanAnswer1_Average").text
        except NoSuchElementException:
            nota_empresa = ""
        try:
            total_avaliacoes = driver.find_element(By.XPATH, "//span[@class='advisor-tabs-num']").text
        except NoSuchElementException:
            total_avaliacoes = ""
        try:
            salario = driver.find_elements(By.XPATH, "//span[@class='advisor-tabs-num']")[1].text
        except NoSuchElementException:
            salario = ""
        try:
            vagas = driver.find_elements(By.XPATH, "//span[@class='advisor-tabs-num']")[2].text
        except NoSuchElementException:
            vagas = ""
        try:
            entrevistas = driver.find_elements(By.XPATH, "//span[@class='advisor-tabs-num']")[3].text
        except NoSuchElementException:
            entrevistas = ""
        try:
            beneficios = driver.find_elements(By.XPATH, "//span[@class='advisor-tabs-num']")[4].text
        except NoSuchElementException:
            beneficios = ""

        # Exibir os valores coletados
        print(f"Nome da Empresa: {nome_da_empresa}")
        print(f"Avaliação: {nota_empresa}")
        print(f"Total de Avaliações: {total_avaliacoes}")
        print(f"Salário: {salario}")
        print(f"Vagas: {vagas}")
        print(f"Entrevistas: {entrevistas}")
        print(f"Benefícios: {beneficios}")

        time.sleep(3)  # Aguardar o carregamento da página da empresa

        # Clicar no botão "Avaliações"
        avaliacao_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_phMasterPage_cHeader_cTabs_cTabsDetailed_lnkReviews"))
        )
        avaliacao_button.click()

        time.sleep(3)  # Aguardar o carregamento da página de avaliações

        # Coletar as cinco primeiras avaliações
        avaliacao = []
        score = []
        comentarios = []
        pros_contras = []

        # Loop para pegar as cinco primeiras avaliações (ctl02 a ctl06)
        for i in range(2, 7):
            prefixo_xpath = f"//*[@id='ctl00_phMasterPage_cGrid_rptGrid_ctl0{i}_"

            # Coletar título da avaliação
            try:
                titulo_avaliacao_element = driver.find_element(By.XPATH, prefixo_xpath + "cItemTitle']")
                titulo_avaliacao = titulo_avaliacao_element.text
            except NoSuchElementException:
                titulo_avaliacao = ""
            avaliacao.append(titulo_avaliacao)

            # Coletar score de estrelas
            try:
                estrelas = driver.find_elements(By.XPATH, prefixo_xpath + "starsTitle']/i[contains(@class, 'zmdi-star')]")
                num_estrelas = len(estrelas)
            except NoSuchElementException:
                num_estrelas = 0  # Caso não encontre, considerar zero estrelas
            score.append(num_estrelas)

            # Coletar comentários
            try:
                comentario_geral = driver.find_element(By.XPATH, prefixo_xpath + "cIsTopEvaluation']/div/div[4]").text
            except NoSuchElementException:
                comentario_geral = ""
            comentarios.append(comentario_geral)

            # Coletar prós, contras e melhorias
            try:
                pros = driver.find_element(By.XPATH, prefixo_xpath + "cPros']").text
            except NoSuchElementException:
                pros = ""
            try:
                contras = driver.find_element(By.XPATH, prefixo_xpath + "cCons']").text
            except NoSuchElementException:
                contras = ""
            try:
                melhorias = driver.find_element(By.XPATH, prefixo_xpath + "cCeoComment']").text
            except NoSuchElementException:
                melhorias = ""
            pros_contras.append((pros, contras, melhorias))

        # Construir o dicionário com os detalhes das avaliações
        detalhes = {
            'avaliacao': avaliacao,
            'score': score,
            'comentarios': comentarios,
            'pros': [p[0] if p[0] else "" for p in pros_contras],  # Garantir que prós, contras e melhorias estejam vazios se não encontrados
            'contras': [p[1] if p[1] else "" for p in pros_contras],
            'melhorias': [p[2] if p[2] else "" for p in pros_contras]
        }

        # Exibir os valores coletados
        for idx in range(len(avaliacao)):
            print(f"Avaliação {idx+1}: {avaliacao[idx]}")
            print(f"Score (estrelas): {score[idx]}")
            print(f"Comentário: {comentarios[idx]}")
            print(f"Prós: {pros_contras[idx][0]}")
            print(f"Contras: {pros_contras[idx][1]}")
            print(f"Melhorias: {pros_contras[idx][2]}")
            print("\n")

        # Salvar os dados em um arquivo Excel
        salvar_dados_no_excel(nome_da_empresa, nota_empresa, total_avaliacoes, salario, vagas, entrevistas, beneficios, detalhes)

    except NoSuchElementException as e:
        print(f"Erro ao buscar dados no site: {e}")
    finally:
        driver.quit()