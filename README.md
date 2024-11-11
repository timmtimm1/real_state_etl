# 🏠 Brazilian Real Estate Market ETL Pipeline

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.0+-green.svg)](https://www.postgresql.org/)
[![Scrapy](https://img.shields.io/badge/Scrapy-2.5+-orange.svg)](https://scrapy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Um pipeline ETL completo para análise do mercado imobiliário brasileiro, com coleta automatizada de dados do OLX, processamento, armazenamento e visualização.

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
  - [Extração de Dados](#-extração-de-dados)
  - [Processamento](#-processamento)
  - [Armazenamento](#-armazenamento)
  - [Visualização](#-visualização)
- [Tecnologias](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Resultados e Métricas](#-resultados-e-métricas)
  - [Estatísticas do Projeto](#estatísticas-do-projeto)
  - [Principais Insights](#-principais-insights)
- [Pipeline de Dados](#-pipeline-de-dados)
  - [Processo ETL](#processo-de-etl)
- [Visualizações](#-visualizações)
- [Banco de Dados](#-banco-de-dados)
- [Análises SQL e Relatórios](#-análises-sql-e-relatórios)
  - [Análises Disponíveis](#-análises-disponíveis)
  - [Relatórios Gerados](#-relatórios-gerados)
  - [Métricas Analisadas](#-principais-métricas-analisadas)
- [Limitações e Considerações](#-limitações-e-considerações)
- [Licença](#-licença
## 🎯 Visão Geral

Este projeto implementa um pipeline de ETL (Extract, Transform, Load) para análise do mercado imobiliário brasileiro, utilizando dados do OLX. O sistema realiza:

- Extração automatizada de dados de imóveis
- Limpeza e normalização dos dados
- Armazenamento em banco PostgreSQL
- Geração de análises e visualizações
- Relatórios de mercado 

## ⭐ Funcionalidades

### 🔍 Extração de Dados
- Web scraping multi-thread
- Cobertura nacional (27 estados)
- Sistema anti-bloqueio
- Gestão de sessões e cookies

### 🔄 Processamento
- Limpeza de dados
- Normalização de valores
- Detecção de outliers
- Enriquecimento de dados

### 💾 Armazenamento
- Banco de dados PostgreSQL
- Modelo relacional otimizado

### 📊 Visualização
- Análises estatísticas
- Gráficos interativos
- Relatórios em JSON
- Mapas de calor

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **PostgreSQL 14+**
- **Frameworks & Bibliotecas:**
  - Scrapy
  - CloudScraper
  - Pandas
  - NumPy
  - Matplotlib
  - Seaborn
  - psycopg2
  - Jupyter Notebooks
  - BeautifulSoup4

## 📁 Estrutura do Projeto
```
etl_project/
├── data/
│   ├── final/                     # Dados finais processados
│   ├── processed/                 # Dados intermediários processados
│   └── raw/                       # Dados brutos coletados
│
├── extract/
│   └── realstate/
│       ├── pycache/            # Cache Python
│       ├── pytest_cache/         # Cache de testes
│       ├── clean_urls/           # URLs limpas
│       ├── property_urls/        # URLs coletadas
│       ├── realstate/           # Módulo principal
│       ├── scrapy.cfg           # Configuração Scrapy
│       ├── test.py             # Testes
│       └── scraper.py          # Scraper principal
│
├── transform/
│   ├── clean_data.ipynb         # Notebook de limpeza
│   ├── clean_location.ipynb     # Processamento de localização
│   ├── clean_urls.py           # Limpeza de URLs
│   └── outliers.ipynb          # Tratamento de outliers
│
├── load/
│   └── load.py                 # Script de carga no banco
│
├── reports/
│   ├── market_report.json
│   └── scraping_report_20241106_171212.json
│
├── SQL_viz/
│   ├── results                # Resultados das análises
│   │   ├── analysis_report_20241111.json
│   │   ├── investment_score_20241111.csv
│   │   ├── investment_score_20241111.json
│   │   ├── premium_analysis_20241111.csv
│   │   ├── premium_analysis_20241111.json
│   │   ├── regional_analysis_20241111.csv
│   │   ├── regional_analysis_20241111.json
│   │   ├── top_neighborhoods_20241111.csv
│   │   └── top_neighborhoods_20241111.json
│   ├── sql/                    # Queries SQL
│   │   ├── investment_score.sql
│   │   ├── premium_analysis.sql
│   │   ├── regional_analysis.sql
│   │   └── top_neighborhoods.sql
│   └── main.py                # Script principal de análise
│
├── visualizations/
│   ├── amenities_analysis.png
│   ├── area_vs_price_scatter.png
│   ├── price_distribution_by_state.png
│   ├── price_distribution.png
│   ├── price_per_m2_heatmap.png
│   ├── property_type_distribution.png
│   └── viz.py
│
├── .gitignore
├── accuracy.py
├── database_import.log
├── README.md
└── requirements.txt
└── LICENSE
```

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/olx-real-estate-etl.git
cd olx-real-estate-etl
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o PostgreSQL**
```bash
# Crie o banco de dados
createdb real_estate_db

# Configure as variáveis de ambiente
export DB_HOST=localhost
export DB_NAME=real_estate_db
export DB_USER=seu_usuario
export DB_PASSWORD=sua_senha
```

## 💻 Como Usar

### 1. Extração de Dados
```bash
# Execute a spider
cd extract/realstate
scrapy crawl realstatespider

# Execute o scraper
python scraper.py
```

### 2. Transformação
```bash
# Execute os scripts de transformação
python transform/clean_data.py
python transform/clean_location.py
python transform/outliers.py
```

### 3. Carga
```bash
# Carregue os dados no PostgreSQL
python load/database.py
```

### 4. Visualização
```bash
# Gere as visualizações
python visualizations/viz.py
```

## 📊 Visualizações

O projeto gera diversas visualizações:

- **Distribuição de Preços**
  - Por estado
  - Por tipo de imóvel
  - Por m²

- **Análises Geográficas**
  - Heatmaps de preços
  - Concentração de ofertas
  - Comparativos regionais

- **Análise de Características**
  - Relação área/preço
  - Impacto de amenidades
  - Distribuição de tipos

## 🗄️ Banco de Dados

### Modelo de Dados
```sql
-- Estrutura principal das tabelas
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    neighborhood VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(2),
    cep VARCHAR(8)
);

CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    price NUMERIC(12,2),
    area_util NUMERIC(8,2),
    bedrooms SMALLINT,
    location_id INTEGER REFERENCES locations(location_id)
);
```

## 📈 Análises Geradas

### Relatório de Mercado
```json
{
    "market_summary": {
        "total_properties": "número total",
        "average_price": "preço médio",
        "price_range": {
            "min": "valor mínimo",
            "max": "valor máximo"
        }
    }
}
```
## 📊 Análises SQL e Relatórios

### 📂 Localização dos Arquivos
As análises SQL e seus resultados podem ser encontrados no diretório `SQL_viz/`:

SQL_viz/
├── results/                # Resultados das análises
│   ├── analysis_report_20241111.json
│   ├── investment_score_20241111.csv
│   ├── premium_analysis_20241111.csv
│   ├── regional_analysis_20241111.csv
│   └── top_neighborhoods_20241111.csv
└── sql/                   # Queries SQL
├── investment_score.sql
├── premium_analysis.sql
├── regional_analysis.sql
└── top_neighborhoods.sql

### 🔍 Análises Disponíveis

#### 1. Score de Investimento (`investment_score.sql`)
- Análise complexa que gera um score de investimento por cidade
- Considera fatores como preço/m², densidade do mercado e amenidades
- **Exemplo de Resultado:**

Balneário Camboriú (SC): 72.25
Nova Lima (MG): 64.21
Manaus (AM): 63.41

#### 2. Análise Premium (`premium_analysis.sql`)
- Identificação e análise de imóveis no segmento premium
- Avaliação de características e distribuição geográfica
- Métricas de valorização por região

#### 3. Análise Regional (`regional_analysis.sql`)
- Comparativo entre diferentes regiões do país
- Indicadores de mercado por estado
- Tendências de preços por localidade

#### 4. Análise de Bairros (`top_neighborhoods.sql`)
- Ranking dos bairros mais valorizados
- Densidade de ofertas por região
- Métricas de preço por m² por bairro

### 📈 Relatórios Gerados

Os relatórios podem ser encontrados em dois formatos:

1. **CSV** (`SQL_viz/results/*.csv`)
 - Dados tabulares para análise
 - Fácil importação em ferramentas de análise
 - Formato ideal para processamento posterior

2. **JSON** (`SQL_viz/results/*.json`)
 - Dados estruturados com metadados
 - Ideal para integração com outras aplicações
 - Inclui métricas e estatísticas agregadas

### 📊 Principais Métricas Analisadas

1. **Métricas de Preço**
 - Preço médio por m²
 - Variação de preços
 - Tendências por segmento

2. **Métricas de Mercado**
 - Densidade de ofertas
 - Distribuição por tipo
 - Concentração geográfica

3. **Métricas de Investimento**
 - Score de investimento
 - Potencial de valorização
 - Indicadores de qualidade

### 💻 Execução das Análises

Para executar as análises SQL e gerar os relatórios:

```bash
cd SQL_viz
python main.py

Os resultados serão salvos em:

CSVs em SQL_viz/results/*.csv
JSONs em SQL_viz/results/*.json
Relatório consolidado em SQL_viz/results/analysis_report_[DATA].json

Para mais detalhes sobre as queries e análises específicas, consulte os arquivos SQL em SQL_viz/sql/.

## 📊 Resultados e Métricas

### Estatísticas do Projeto
- **Cobertura**: 27 estados brasileiros
- **Volume de Dados**: +60.000 imóveis analisados
- **Taxa de Sucesso**: 96.52% na coleta de dados
- **Precisão**: Alta confiabilidade após limpeza e normalização

### 🏆 Principais Insights
1. **Mercados Premium**
   - Ipojuca (PE) lidera com maior preço/m², mais de R$ 15.000,00
   - Nova Lima (MG) destacada no segmento luxo
   - Manaus (AM) apresenta mercado aquecido
   - 

2. **Tendências Identificadas**
   - Concentração de alto valor em capitais
   - Correlação forte entre amenidades e preço
   - Padrões regionais de valorização

## 🔄 Pipeline de Dados

### Processo de ETL
1. **Extract**
   - Coleta distribuída por estado
   - Sistema anti-bloqueio 
   - Validação de dados na origem

2. **Transform**
   - Limpeza e padronização
   - Detecção de anomalias
   - Enriquecimento geográfico, separando uma coluna em 4

3. **Load**
   - Modelagem otimizada
   - Índices eficientes
   - Backup automático

## ⚠️ Limitações e Considerações

- Dados limitados ao período de coleta
- Foco em imóveis à venda (não inclui aluguel)
- Dependência da disponibilidade da fonte
- Possíveis variações sazonais
- Alguns imóveis com dados corrompidos ou mal estruturados
- Demora na extração de dados, por motivos de poder computacional


## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
