# 📌 ReclameAqui Scraper

> Este script faz a captura automatizada de informações do site ReclameAqui usando Selenium e undetected_chromedriver para evitar bloqueios.

---
<br/>

## 🛠 Pré-requisitos

Antes de rodar o script, certifique-se de que você tenha:

- ✔ **Python 3.8+** instalado.
- ✔ **Google Chrome** atualizado.

---
<br/>

## 📥 Passo 1: Clone o repositório

Abra o terminal ou PowerShell e execute:

```sh
git clone https://github.com/iagoluancj/ra-scraper
```

```sh
cd ra-scraper
```


---
<br/>

## 📦 Passo 2: Crie e ative o ambiente virtual
```sh
python -m venv venv
```

### No Windows: 
- (PowerShell ou VS Code)
```sh
venv\Scripts\Activate.ps1
```

- (cmd)
```sh
venv\Scripts\activate.bat
```

### No Linux/macOS:
```sh
source venv/bin/activate
```

---
<br/>

## 📌 Passo 3: Instale as dependências
```sh
pip install undetected-chromedriver selenium pandas xlsxwriter
```

---
<br/>

## 🚀 Passo 4: Execute o scraper

Para iniciar a captura dos dados, rode o seguinte comando:
```sh
python scraper.py
```
O script abrirá o Chrome, coletará os dados e salvará um arquivo XLSX com as informações capturadas.

---
<br/>

## 📊 Saída esperada

Após a execução, será gerado um arquivo **empresas_reclameaqui.xlsx** no mesmo diretório do script.:

| Empresas |
|---------------|
| Empresa A     |
| Empresa B     |
| Empresa C     |

---
<br/>

## 🛠 Erros comuns e soluções

🔹 **Erro:** `PermissionError: [WinError 5]` ao ativar o ambiente virtual  
➡ **Solução:** Execute `Set-ExecutionPolicy Unrestricted -Scope Process` no PowerShell.

🔹 **Erro:** Chrome fecha imediatamente ao rodar o script  
➡ **Solução:** Remova `--headless=new` do código para depurar o erro.

🔹 **Erro:** Demora ao capturar dados  
➡ **Solução:** Aumente `time.sleep(3)` para `time.sleep(5)`.

---
