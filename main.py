from infojobs_scraper import abrir_navegador_e_interagir_com_site
from utils import consultar_empresa

"""
Executa o fluxo completo de busca de informações de uma empresa no site InfoJobs.

Esta função consulta o nome da empresa através da função 'consultar_empresa',
constrói a URL para o site InfoJobs e em seguida, utiliza a função 'abrir_navegador_e_interagir_com_site'
para abrir o navegador e realizar a interação com o site.

Retorna:
    None
"""

# Função principal que executa o fluxo completo
def executar_busca():
    empresa = consultar_empresa()
    url_site = f"https://www.infojobs.com.br/ranking-melhores-empresas.aspx"
    # Interage com o site InfoJobs para consultar a empresa
    abrir_navegador_e_interagir_com_site(url_site, empresa)

# Execução do código
if __name__ == "__main__":
    # Inicia o fluxo principal de execução do código
    executar_busca()
