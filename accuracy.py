import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def calculate_and_save_scraping_report():
    # Contar URLs dos JSONs
    json_dir = Path(r'C:\Users\berna\etl_project\extract\realstate\clean_urls')
    total_urls = 0
    state_counts = {}
    
    # Ler cada arquivo JSON
    for json_file in json_dir.glob('*_clean.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            urls_count = len(data['urls'])
            state_counts[data['state']] = urls_count
            total_urls += urls_count
    
    # Contar registros no CSV
    csv_path = r'C:\Users\berna\etl_project\data\processed\merged_properties.csv'
    df = pd.read_csv(csv_path)
    total_scraped = len(df)
    
    # Calcular taxa de sucesso
    success_rate = (total_scraped / total_urls) * 100
    
    # Criar relatório
    report = {
        "report_metadata": {
            "date_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_name": "OLX Real Estate Scraper"
        },
        "scraping_results": {
            "total_urls_collected": total_urls,
            "total_records_scraped": total_scraped,
            "success_rate": round(success_rate, 2),
            "failed_urls": total_urls - total_scraped
        },
        "state_distribution": {
            state: count for state, count in sorted(
                state_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
        },
        "state_statistics": {
            "highest_coverage": {
                "state": max(state_counts, key=state_counts.get),
                "urls": max(state_counts.values())
            },
            "lowest_coverage": {
                "state": min(state_counts, key=state_counts.get),
                "urls": min(state_counts.values())
            },
            "average_urls_per_state": round(total_urls / len(state_counts), 2)
        }
    }
    
    # Criar diretório para relatórios se não existir
    report_dir = Path(r'C:\Users\berna\etl_project\reports')
    report_dir.mkdir(exist_ok=True)
    
    # Salvar relatório com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f'scraping_report_{timestamp}.json'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    
    # Exibir resultados
    print("=== Análise de Taxa de Sucesso do Scraper ===")
    print(f"\nTotal de URLs coletadas: {total_urls:,}")
    print(f"Total de registros extraídos: {total_scraped:,}")
    print(f"\nTaxa de sucesso: {success_rate:.2f}%")
    
    # Estatísticas por estado
    print("\n=== URLs por Estado ===")
    df_states = pd.DataFrame.from_dict(state_counts, orient='index', columns=['urls'])
    df_states = df_states.sort_values('urls', ascending=False)
    print(df_states.to_string())
    
    print(f"\nRelatório salvo em: {report_path}")
    
    return report

if __name__ == "__main__":
    report = calculate_and_save_scraping_report()
