# 🏠 Brazilian Real Estate Market ETL Pipeline

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.0+-green.svg)](https://www.postgresql.org/)
[![Scrapy](https://img.shields.io/badge/Scrapy-2.5+-orange.svg)](https://scrapy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Um pipeline ETL completo para análise do mercado imobiliário brasileiro, com coleta automatizada de dados do OLX, processamento, armazenamento e visualização.

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Visualizações](#visualizações)
- [Banco de Dados](#banco-de-dados)
- [Análises Geradas](#análises-geradas)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

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

## 🛠️ Tecnologias

- **Python 3.8+**
- **PostgreSQL 14+**
- **Frameworks & Bibliotecas:**
  - Scrapy
  - Pandas
  - NumPy
  - Matplotlib
  - Seaborn
  - psycopg2
  - CloudScraper

## 📁 Estrutura do Projeto

```
olx-real-estate-etl/
├── data/
│   ├── interim/                    # Dados intermediários
│   ├── processed/                  # Dados processados
│   └── raw/                       # Dados brutos
│
├── extract/
│   └── realstate/
│       ├── spiders/               # Spiders Scrapy
│       │   ├── realstatespider.py
│       │   └── settings.py
│       └── scraper/              # Web Scraper
│
├── transform/
│   ├── clean_data.py             # Limpeza de dados
│   ├── clean_location.py         # Processamento de localização
│   └── outliers.py              # Tratamento de outliers
│
├── load/
│   └── database.py              # Scripts PostgreSQL
│
├── visualizations/
│   ├── viz.py                   # Gerador de visualizações
│   └── outputs/                 # Visualizações geradas
│
├── requirements.txt
├── README.md
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

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
