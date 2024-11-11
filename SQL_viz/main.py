import pandas as pd
import psycopg2
from psycopg2 import Error
import json
from pathlib import Path
from datetime import datetime

class RealEstateExporter:
    def __init__(self):
        # Configurações de conexão com o banco de dados
        self.db_params = {
            "host": "localhost",
            "database": "real_estate_db",
            "user": "postgres",
            "password": "Bb121973820@"
        }
        
        # Configurar diretórios
        self.base_dir = Path('SQL_viz')
        self.sql_dir = self.base_dir / 'sql'
        self.results_dir = self.base_dir / 'results'
        
        # Criar diretórios
        for directory in [self.base_dir, self.sql_dir, self.results_dir]:
            directory.mkdir(exist_ok=True, parents=True)

    def save_queries(self):
        """Salva as queries em arquivos SQL"""
        queries = {
            'premium_analysis.sql':"""
                WITH premium_properties AS (
                    SELECT *,
                        NTILE(10) OVER (ORDER BY price) as price_decile
                    FROM properties
                )
                SELECT 
                    COUNT(*) as total_premium_properties,
                    ROUND(AVG(area_util)::numeric, 2) as avg_area,
                    ROUND(AVG(bedrooms)::numeric, 1) as avg_bedrooms,
                    ROUND(AVG(bathrooms)::numeric, 1) as avg_bathrooms,
                    ROUND(AVG(parking_spots)::numeric, 1) as avg_parking_spots,
                    ROUND(AVG(price)::numeric, 2) as avg_price,
                    ROUND(AVG(price_per_m2)::numeric, 2) as avg_price_per_m2
                FROM premium_properties
                WHERE price_decile = 10;

        """,
            'regional_analysis.sql': """
                WITH regional_stats AS (
                    SELECT 
                        CASE 
                            WHEN l.state IN ('sp', 'rj', 'mg', 'es') THEN 'Sudeste'
                            WHEN l.state IN ('pr', 'sc', 'rs') THEN 'Sul'
                            WHEN l.state IN ('ba', 'ce', 'pe', 'pb', 'ma', 'pi', 'rn', 'se', 'al') THEN 'Nordeste'
                            WHEN l.state IN ('mt', 'ms', 'go', 'df') THEN 'Centro-Oeste'
                            ELSE 'Norte'
                        END as region,
                        COUNT(*) as total_properties,
                        ROUND(AVG(price)::numeric, 2) as avg_price,
                        ROUND(AVG(price_per_m2)::numeric, 2) as avg_price_per_m2,
                        ROUND(AVG(area_util)::numeric, 2) as avg_area
                    FROM properties p
                    JOIN locations l ON p.location_id = l.location_id
                    GROUP BY region
                )
                SELECT 
                    region,
                    total_properties,
                    avg_price,
                    avg_price_per_m2,
                    avg_area,
                    ROUND(100.0 * total_properties / SUM(total_properties) OVER (), 2) as market_share_percentage
                FROM regional_stats
                ORDER BY avg_price DESC;
            """,
            
            'top_neighborhoods.sql': """
                WITH neighborhood_stats AS (
                    SELECT 
                        l.city,
                        l.state,
                        l.neighborhood,
                        COUNT(*) as listing_count,
                        ROUND(AVG(p.price)::numeric, 2) as avg_price,
                        ROUND(AVG(p.price_per_m2)::numeric, 2) as avg_price_per_m2,
                        ROUND(AVG(p.area_util)::numeric, 2) as avg_area
                    FROM properties p
                    JOIN locations l ON p.location_id = l.location_id
                    WHERE l.neighborhood IS NOT NULL
                    GROUP BY l.city, l.state, l.neighborhood
                    HAVING COUNT(*) > 5
                )
                SELECT *,
                    ROUND(100.0 * listing_count / SUM(listing_count) OVER (PARTITION BY city), 2) 
                    as market_share
                FROM neighborhood_stats
                ORDER BY listing_count DESC
                LIMIT 20;
            """,
            
            'investment_score.sql': """
                WITH investment_metrics AS (
                    SELECT 
                        l.city,
                        l.state,
                        COUNT(*) as total_listings,
                        AVG(p.price_per_m2) as avg_price_per_m2,
                        STDDEV(p.price_per_m2) as price_std,
                        percentile_cont(0.5) WITHIN GROUP (ORDER BY p.price_per_m2) as median_price_per_m2,
                        AVG(p.area_util) as avg_area,
                        AVG(p.bedrooms) as avg_bedrooms,
                        AVG(p.bathrooms) as avg_bathrooms,
                        AVG(p.parking_spots) as avg_parking,
                        COUNT(*) / MAX(COUNT(*)) OVER () as market_density_score
                    FROM properties p
                    JOIN locations l ON p.location_id = l.location_id
                    GROUP BY l.city, l.state
                    HAVING COUNT(*) > 20
                )
                SELECT 
                    city,
                    state,
                    total_listings,
                    ROUND(avg_price_per_m2::numeric, 2) as avg_price_per_m2,
                    ROUND(median_price_per_m2::numeric, 2) as median_price_per_m2,
                    ROUND((
                        (0.4 * (avg_price_per_m2 / MAX(avg_price_per_m2) OVER ())) +
                        (0.2 * (1 - (price_std / avg_price_per_m2))) +
                        (0.2 * market_density_score) +
                        (0.2 * (
                            (avg_bedrooms / 4) + 
                            (avg_bathrooms / 3) + 
                            (avg_parking / 2)
                        ) / 3)
                    ) * 100::numeric, 2) as investment_score
                FROM investment_metrics
                WHERE city IS NOT NULL
                ORDER BY investment_score DESC
                LIMIT 20;
            """
        }
        
        # Salvar queries em arquivos SQL
        for filename, query in queries.items():
            with open(self.sql_dir / filename, 'w', encoding='utf-8') as f:
                f.write(query.strip())
        
        return queries

    def execute_and_save_results(self):
        """Executa as queries e salva os resultados"""
        queries = self.save_queries()
        timestamp = datetime.now().strftime("%Y%m%d")
        
        try:
            with psycopg2.connect(**self.db_params) as conn:
                results = {}
                
                # Executar queries e salvar resultados
                for name, query in queries.items():
                    print(f"\nExecutando query: {name}")
                    
                    # Executar query
                    df = pd.read_sql_query(query, conn)
                    base_name = name.replace('.sql', '')
                    results[base_name] = df
                    
                    # Salvar resultados
                    csv_file = self.results_dir / f'{base_name}_{timestamp}.csv'
                    json_file = self.results_dir / f'{base_name}_{timestamp}.json'
                    
                    df.to_csv(csv_file, index=False)
                    df.to_json(json_file, orient='records', indent=4)
                    
                    print(f"Resultados salvos em:")
                    print(f"- CSV: {csv_file}")
                    print(f"- JSON: {json_file}")
                
                # Criar relatório simples
                report = {
                    "analysis_date": timestamp,
                    "queries_executed": list(queries.keys()),
                    "summary": {
                        name: {
                            "records": len(df),
                            "columns": list(df.columns)
                        }
                        for name, df in results.items()
                    }
                }
                
                # Salvar relatório
                report_file = self.results_dir / f'analysis_report_{timestamp}.json'
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=4)
                
                print(f"\nRelatório salvo em: {report_file}")
                print("\nProcesso de exportação concluído com sucesso!")
                
                return results
                
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return None

if __name__ == "__main__":
    exporter = RealEstateExporter()
    results = exporter.execute_and_save_results()
