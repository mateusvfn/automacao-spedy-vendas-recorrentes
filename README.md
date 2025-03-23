# Automação de Planilhas de Vendas para SPEDY

Este projeto automatiza a geração de planilhas de vendas no formato compatível para upload no [SPEDY](https://spedy.com), um sistema de emissão de notas fiscais utilizado em diversas prefeituras brasileiras.

## Visão Geral

O sistema integra e processa dados de vendas provenientes de três fontes diferentes:

- **Vendas Recorrentes**: Gerenciadas pelo site [app.recorrente](https://apprecorrente.com/), que realiza a gestão de cobrança recorrente no cartão de crédito via Cielo Ecommerce. Como o app.recorrente não possui API, o Selenium é utilizado para baixar automaticamente as planilhas de vendas.
- **Vendas Maquininha**: Dados baixados em formato CSV a partir do site da Cielo (Maquininha).
- **Vendas Ecommerce**: Dados baixados em formato Excel do site da Cielo.

Além disso, o sistema utiliza uma planilha online (Google Sheets) para registrar novos endereços e o código de venda (DOC), que devem ser informados pela equipe de vendas.

## Funcionalidades

- **Automação do Download**: Utiliza Selenium para efetuar login no app.recorrente e baixar a planilha de vendas recorrentes.
- **Importação e Processamento de Dados**:
  - Processa planilhas de vendas recorrentes, de maquininha (CSV) e de ecommerce (Excel).
  - Filtra as vendas com base em um intervalo de datas informado pelo usuário.
- **Consolidação de Vendas**:
  - Unifica os dados das três fontes, somando os valores das vendas por CPF.
  - Atribui automaticamente o endereço correto para cada venda, consultando uma base de endereços e incorporando novos endereços registrados via Google Sheets.
- **Geração de Planilhas para SPEDY**:
  - Organiza e formata os dados para atender ao modelo de upload do SPEDY.
  - Atribui um código sequencial para cada venda.
- **Atualização da Base de Endereços**:
  - A cada execução, a base de endereços é atualizada com os novos dados informados pela equipe.

## Requisitos

- **Python 3.x**
- **Bibliotecas Python**:
  - pandas
  - selenium
  - numpy
  - unidecode
  - openpyxl
  - python-dotenv
- **ChromeDriver**: Compatível com a versão do Google Chrome instalada.
- **Acesso à Internet**: Necessário para baixar planilhas e acessar o Google Sheets.

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/automacao-vendas-recorrentes.git
   cd automacao-vendas-recorrentes


2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**:
   - Renomeie o arquivo `.env.example` para `.env`.
   - Edite o arquivo `.env` com seu login e senha do app.recorrente:
     ```env
     EMAIL=seuemail@dominio.com
     SENHA=suasenha123
     ```

## Uso

O usuário deverá informar:

- O **código da venda SPEDY** da próxima venda.
- O **intervalo de datas** para filtrar as vendas para emissão das notas fiscais.
- As credenciais de acesso ao app.recorrente (via arquivo `.env`).

O fluxo do programa é o seguinte:

1. **Download Automático**: O Selenium (no módulo `chromedriver_automation.py`) efetua o login no app.recorrente e baixa a planilha de vendas recorrentes. Essa etapa demora 4 minutos para garantir que a página carregue e o download seja concluído.
2. **Processamento dos Dados**:
   - Vendas recorrentes (módulo `recorrente.py`).
   - Vendas Maquininha (módulo `maquininha.py`, entrada CSV). Baixe o seu relatório de vendas na cielo.
   - Vendas Ecommerce (módulo `ecommerce.py`, entrada Excel). Baixe o seu relatório de vendas ecommerce na cielo.
   - Os arquivos devem estar habilitados para edição, abra os arquivos no excel e salve para habilitar a edição e possibilitar a leitura correta.
3. **Unificação e Consolidação**:
   - As vendas são unificadas e somadas por CPF (módulo `consolidacao.py`).
   - Os dados são filtrados pelo intervalo de datas e os valores de vendas para o mesmo cliente são somados.
4. **Atribuição de Endereços**:
   - O sistema associa o endereço correto para cada venda com base no CPF, consultando uma base de endereços que é atualizada com os novos dados do Google Sheets.
5. **Geração da Planilha Final**:
   - São geradas duas planilhas:
     - `Vendas_Unificadas.xlsx`: Planilha consolidada.
     - `Vendas_Spedy.xlsx`: Planilha formatada para upload no SPEDY.

## Estrutura do Projeto

```
automacao-vendas-recorrentes/
├── main.py                      # Orquestra a execução do pipeline
├── recorrente.py                # Processamento das vendas recorrentes
├── ecommerce.py                 # Processamento dos dados de ecommerce
├── maquininha.py                # Processamento da maquininha (CSV)
├── consolidacao.py              # Unificação, consolidação e transformação dos dados para SPEDY
├── endereco.py                  # Carregamento e tratamento de endereços (base e Google Sheets)
├── utils.py                     # Funções auxiliares (limpeza de CPF, texto, valor, geração de códigos)
├── chromedriver_automation.py   # Automação do download via Selenium
├── .env.example                 # Modelo de arquivo de variáveis de ambiente
├── .gitignore                   # Arquivo para ignorar arquivos sensíveis e temporários
├── requirements.txt             # Lista de dependências
├── README.md                    # Documentação deste projeto
└── LICENSE                      # Licença MIT
```

## Exemplo de Execução

Execute o programa principal:
```bash
python main.py
```
Após a execução, serão geradas as planilhas:
- **Vendas_Unificadas.xlsx**: Dados consolidados de todas as fontes.
- **Vendas_Spedy.xlsx**: Dados formatados conforme o modelo exigido pelo SPEDY.

## Considerações

- Certifique-se de que os **caminhos dos arquivos** (Excel, CSV, ChromeDriver) estejam corretos no `main.py`.
- Verifique se o **ChromeDriver** está instalado e compatível com sua versão do Chrome.
- O app.recorrente utiliza Selenium para automação; mantenha suas credenciais atualizadas no arquivo `.env`.
- A planilha de Google Sheets com os endereços e códigos DOC deve estar acessível para que o sistema possa fazer o merge corretamente.

## Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Mateus Nunes
https://www.linkedin.com/in/mateusvfn/
mateusvfn@hotmail.com

