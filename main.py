from infojobs_scraper import abrir_navegador_e_interagir_com_site
from utils import consultar_empresa

# Função principal que executa o fluxo completo
def executar_busca():
    empresa = consultar_empresa()
    url_site = f"https://www.infojobs.com.br/ranking-melhores-empresas.aspx"
    # executar função de consulta da empresa no infojobs
    abrir_navegador_e_interagir_com_site(url_site, empresa)

# Execução do código
if __name__ == "__main__":
    executar_busca()
