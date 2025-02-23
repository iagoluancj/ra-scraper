import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import os


class ReclameAquiScraper:
    def __init__(self, url):
        # Inicializador do WebDriver.
        options = uc.ChromeOptions()

        # Necessário desabilitar o pop-up por estar abrindo uc.chrome.
        options.add_argument("--disable-popup-blocking")

        self.driver = uc.Chrome(options=options)
        self.driver.get(url)
        self.wait = WebDriverWait(self.driver, 2)

    def extrair_numero(self, texto):
        # Função para extrair apenas os números das tag's
        match = re.search(r"\d+(\.\d+)?", texto)
        return match.group() if match else "0"

    def capturar_dados_empresas(self, tipo="BEST"):
        # Pega os dados das três primeiras empresas, de acordo com a seleção da página (melhores e piores).
        if tipo == "WORST":
            self.abrir_piores_empresas()

        empresas = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[data-testid="ranking-item-company-name"]')
        ))[:3]  

        urls = [empresa.get_attribute("href") for empresa in empresas]

        dados_empresas = []
        for url in urls:
            self.driver.execute_script("window.open(arguments[0]);", url)  # Abre nova aba
            self.driver.switch_to.window(self.driver.window_handles[-1])  # Alterna para a nova aba

            self.driver.implicitly_wait(1) 

            try:
                dados_empresas.append(self.extrair_dados_empresa())
            except Exception as e:
                print(f"Erro ao capturar dados da empresa: {url}\nErro: {e}")

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        return dados_empresas

    def abrir_piores_empresas(self):
        # Clica no botão para mostrar as piores empresas
        botao_piores = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-testid="ranking-button-WORST"]')
        ))
        botao_piores.click()

        self.driver.implicitly_wait(1)

    def extrair_dados_empresa(self):
        # Extrai os dados da empresa na página em aberto

        # Identifiquei que o melhor local para extrair o nome da empresa é em seu H1 na nova guia aberta.
        nome = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, '/empresa')]/h1"))
        ).text

        # Para os campos abaixo, tentei obter os dados através da API, via URL ou interceptando no navegador, mas o Reclame Aqui bloqueia essas tentativas.
        respostas = self.extrair_numero(self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Respondeu')]/strong"))
        ).text)

        voltaria = self.extrair_numero(self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'avaliaram,')]/strong"))
        ).text)

        resolucao = self.extrair_numero(self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'A empresa resolveu')]/strong"))
        ).text)

        # Diferente dos campos anteriores, esse foi necessário trata-lo com try, pois, durante os testes, identifiquei que ocorria exception ao buscar a nota media das piores empresas, 
        # o problema acontece pois as piores empresas não possui nota, e com isso não possui os caractres "nota média"
        try:
            nota_media = self.extrair_numero(self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'nota média')]/b"))
            ).text)
        except:
            nota_media = "0"

        try:
            reputacao = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.go2868740670 > span.go2441042915, span.go240704099"))
            ).text
        except:
            reputacao = "Desconhecido"

        return {
            "Nome da empresa": nome,
            "Reclamações respondidas": f"{respostas}%",
            "Voltariam a fazer negócio": f"{voltaria}%",
            "Índice de solução": f"{resolucao}%",
            "Nota do consumidor": nota_media,
            "Recomendação do RA": reputacao
        }

    def fechar(self):
        self.driver.quit()


class ExcelExporter:

    @staticmethod
    def salvar(nome_arquivo, melhores_empresas, piores_empresas):
        # Salva os dados em um arquivo do excel, separado em três abas, pensando na manipulação de ambos em conjunto ou separados.

        with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
            df_melhores = pd.DataFrame(melhores_empresas)
            df_melhores.to_excel(writer, sheet_name="Melhores Empresas", index=False)

            df_piores = pd.DataFrame(piores_empresas)
            df_piores.to_excel(writer, sheet_name="Piores Empresas", index=False)

            df_todas = pd.concat([df_melhores, df_piores], ignore_index=True)
            df_todas.to_excel(writer, sheet_name="Todas Empresas", index=False)

        print(f"📂 Dados salvos com sucesso em '{nome_arquivo}'.")


def main():
    url = "https://www.reclameaqui.com.br/segmentos/servicos-essenciais/energia-eletrica/"
    scraper = ReclameAquiScraper(url)

    try:
        print("\n🔹 Capturando as melhores empresas...")
        melhores_empresas = scraper.capturar_dados_empresas("BEST")

        print("\n🔹 Capturando as piores empresas...")
        piores_empresas = scraper.capturar_dados_empresas("WORST")

        for tipo, empresas in [("Melhores", melhores_empresas), ("Piores", piores_empresas)]:
            print(f"\n🔹 **{tipo} Empresas:**")
            for i, empresa in enumerate(empresas, 1):
                print(f"\n📌 Empresa {i}:")
                for chave, valor in empresa.items():
                    print(f"   {chave}: {valor}")

        ExcelExporter.salvar("empresas_ranking.xlsx", melhores_empresas, piores_empresas)

    finally:
        scraper.fechar()
        os._exit(0)


if __name__ == "__main__":
    main()