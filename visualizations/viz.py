import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import os

class RealEstateVisualizer:
    def __init__(self, df):
        self.df = df
        # Set style for all plots
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['figure.max_open_warning'] = 50  # Increase max figure warning
        self.vis_path = r'C:\Users\berna\etl_project\visualizations'
        os.makedirs(self.vis_path, exist_ok=True)
        
    def save_plot(self, filename, dpi=200, bbox_inches='tight'):
        """Helper method to save plots with consistent settings"""
        try:
            plt.savefig(
                os.path.join(self.vis_path, filename),
                dpi=dpi,
                bbox_inches=bbox_inches,
                pad_inches=0.3,
                format='png'
            )
        finally:
            plt.close('all')  # Ensure all figures are closed
        
    def plot_price_distribution_by_state(self):
        """Creates a box plot showing price distribution by state"""
        plt.figure(figsize=(15, 8))
        ax = sns.boxplot(data=self.df, x='price', y='state', showfliers=False)
        plt.xticks(rotation=45)
        plt.title('Price Distribution by State')
        plt.xlabel('Price(R$)')
        plt.ylabel('Estado')
        
        # Format price values for better readability
        def format_price(x):
            if x >= 1e6:
                return f'R${x/1e6:.1f}M'
            return f'R${x/1e3:.0f}K'
        
        medians = self.df.groupby('state')['price'].median()
        for i, median in enumerate(medians):
            ax.text(median, i, format_price(median), 
                   ha='left', va='center', fontsize=10)
        
        # Adjust layout with specific margins
        plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
        self.save_plot('price_distribution_by_state.png')

    def plot_price_per_m2_heatmap(self):
        """Creates a heatmap of average price per m² by state and number of rooms"""
        pivot_table = self.df.pivot_table(
            values='price_per_m2',
            index='state',
            columns='quartos',
            aggfunc='median'
        )
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Price per m² (R$)'})
        plt.title('Median Price per m² by State and Number of Rooms')
        plt.xlabel('Number of Rooms')
        plt.ylabel('State')
        plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.1)
        self.save_plot('price_per_m2_heatmap.png')
    
    def plot_property_type_distribution(self):
        """Creates a bar plot showing the distribution of properties by price category"""
        fig = plt.figure(figsize=(15, 12))
        gs = GridSpec(2, 1, height_ratios=[1, 1.2], hspace=0.3)
        
        ax1 = fig.add_subplot(gs[0])
        sns.countplot(data=self.df, x='price_category', ax=ax1, 
                     order=['Econômico', 'Médio', 'Alto padrão', 'Luxo', 'Não informado'])
        ax1.set_title('Distribution of Properties by Price Category')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        
        ax2 = fig.add_subplot(gs[1])
        category_counts = pd.crosstab(self.df['state'], self.df['price_category'], 
                                    normalize='index') * 100
        category_counts.plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title('Property Distribution by Price Category and State')
        ax2.set_ylabel('Percentage')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.subplots_adjust(left=0.1, right=0.85, top=0.95, bottom=0.1)
        self.save_plot('property_type_distribution.png')
    
    
    def plot_area_vs_price_scatter(self):
        """Creates a plot showing average prices by area ranges for each state"""
        bins = [0, 50, 100, 150, 200, 300, 500, 1000]
        labels = ['0-50', '51-100', '101-150', '151-200', '201-300', '301-500', '500+']
        
        df_analysis = self.df.copy()
        df_analysis['area_range'] = pd.cut(df_analysis['area_util'], 
                                        bins=bins, 
                                        labels=labels, 
                                        right=False)
        
        avg_prices = df_analysis.groupby(['state', 'area_range'])['price'].agg([
            'mean',
            'count',
            'std'
        ]).reset_index()
        
        significant_states = df_analysis.groupby('state')['price'].count()
        significant_states = significant_states[significant_states > 50].index
        avg_prices = avg_prices[avg_prices['state'].isin(significant_states)]
        
        plt.figure(figsize=(15, 10))
        
        for state in significant_states:
            state_data = avg_prices[avg_prices['state'] == state]
            
            plt.plot(state_data['area_range'], 
                    state_data['mean'], 
                    marker='o', 
                    label=state,
                    linewidth=2,
                    markersize=8)
            
            plt.fill_between(range(len(state_data['area_range'])),
                            state_data['mean'] - state_data['std'],
                            state_data['mean'] + state_data['std'],
                            alpha=0.1)
        
        plt.title('Average Property Price by Area Range and State', pad=20, size=14)
        plt.xlabel('Area Range (m²)', size=12)
        plt.ylabel('Average Price (R$)', size=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.legend(title='State',
                bbox_to_anchor=(1.05, 1),
                loc='upper left',
                borderaxespad=0.)
        
        def millions_formatter(x, pos):
            return f'R${x/1e6:.1f}M'
        
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))
        
        sample_sizes = df_analysis.groupby('state')['price'].count()
        text = "Sample sizes:\n" + \
            "\n".join([f"{state}: {count:,}" for state, count in 
                        sample_sizes[significant_states].items()])
        
        plt.figtext(1.25, 0.5, text,
                    bbox=dict(facecolor='white', alpha=0.8),
                    verticalalignment='center')
        
        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.85, top=0.95, bottom=0.1)
        self.save_plot('area_vs_price_scatter.png')
        
    def plot_amenities_analysis(self):
        """Creates a grid of plots analyzing property amenities"""
        fig = plt.figure(figsize=(15, 12))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, 0])
        sns.boxplot(data=self.df, x='quartos', y='price', ax=ax1)
        ax1.set_title('Price by Number of Bedrooms')
        ax1.set_ylabel('Price (R$)')
        
        ax2 = fig.add_subplot(gs[0, 1])
        sns.boxplot(data=self.df, x='banheiros', y='price', ax=ax2)
        ax2.set_title('Price by Number of Bathrooms')
        ax2.set_ylabel('Price (R$)')
        
        ax3 = fig.add_subplot(gs[1, 0])
        sns.boxplot(data=self.df, x='vagas', y='price', ax=ax3)
        ax3.set_title('Price by Number of Parking Spots')
        ax3.set_ylabel('Price (R$)')
        
        ax4 = fig.add_subplot(gs[1, 1])
        amenities = pd.DataFrame({
            'Bedrooms': self.df['quartos'].value_counts(),
            'Bathrooms': self.df['banheiros'].value_counts(),
            'Parking': self.df['vagas'].value_counts()
        })
        amenities.plot(kind='bar', ax=ax4)
        ax4.set_title('Distribution of Property Amenities')
        ax4.legend()
        
        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
        self.save_plot('amenities_analysis.png')
    
    def plot_price_distribution(self):
        """Creates plots showing price distribution"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        sns.histplot(data=self.df, x='price', ax=ax1, bins=50)
        ax1.set_title('Price Distribution')
        ax1.set_xlabel('Price (R$)')
        
        sns.histplot(data=self.df, x='price_per_m2', ax=ax2, bins=50)
        ax2.set_title('Price per m² Distribution')
        ax2.set_xlabel('Price per m² (R$)')
        
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1, wspace=0.3)
        self.save_plot('price_distribution.png')
    
    def generate_market_report(self):
        """Generates and saves a comprehensive market analysis report as JSON"""
        report = {
            "title": "Brazilian Real Estate Market Analysis",
            "property_size_distribution": self.df.groupby('quartos')['price'].agg([
                'count', 'mean', 'median'
            ]).round(2).to_dict('index'),
            
            "top_10_expensive_cities": self.df.groupby('city')['price_per_m2'].agg([
                'count', 'median'
            ]).query('count >= 10').sort_values('median', ascending=False).head(10).to_dict('index')
        }
        
        # Save report as JSON
        with open(os.path.join(self.vis_path, 'market_report.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
    
    def plot_all(self):
        """Generates all visualizations and saves them to files"""
        try:
            print("Generating visualizations...")
            self.plot_price_distribution()
            print("✓ Price distribution plots saved")
            self.plot_price_distribution_by_state()
            print("✓ Price distribution by state plot saved")
            self.plot_price_per_m2_heatmap()
            print("✓ Price per m² heatmap saved")
            self.plot_property_type_distribution()
            print("✓ Property type distribution plots saved")
            self.plot_area_vs_price_scatter()
            print("✓ Area vs price scatter plot saved")
            self.plot_amenities_analysis()
            print("✓ Amenities analysis plots saved")
            self.generate_market_report()
            print("✓ Market report saved")
            print(f"\nAll files have been saved to: {self.vis_path}")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            plt.close('all')  # Ensure cleanup on error

# Usage
df = pd.read_csv(r'C:\Users\berna\etl_project\data\interim\properties_cleaned_no_outliers.csv')
visualizer = RealEstateVisualizer(df)
visualizer.plot_all()