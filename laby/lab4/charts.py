import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    df = pd.read_csv('results.csv')
except FileNotFoundError:
    print("Błąd: Nie znaleziono pliku results.csv")
    exit()

df['File Size (MB)'] = (df['File Size (bytes)'] / (1024 * 1024)).round(0)

modes = df['Mode'].unique()
file_sizes = sorted(df['File Size (MB)'].unique())

def create_plot(metric_column, title, ylabel):
    plt.figure(figsize=(12, 7))
    
    bar_width = 0.2
    index = np.arange(len(modes))
    
    for i, size in enumerate(file_sizes):
        subset = df[df['File Size (MB)'] == size]
        subset = subset.set_index('Mode').reindex(modes).reset_index()
        
        plt.bar(index + i * bar_width, subset[metric_column], 
                bar_width, label=f'Plik {size} MB')

    plt.title(title, fontsize=14)
    plt.xlabel('Tryb Szyfrowania', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(index + bar_width * (len(file_sizes) - 1) / 2, modes)
    plt.legend(title='Rozmiar pliku')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    filename = metric_column.replace(' ', '_').replace('(', '').replace(')', '').lower() + '.png'
    plt.savefig(filename)
    print(f"Wygenerowano wykres: {filename}")
    plt.show()

create_plot('Encryption Time (s)', 
            'Porównanie czasu szyfrowania w zależności od trybu i rozmiaru pliku', 
            'Czas [s]')

create_plot('Decryption Time (s)', 
            'Porównanie czasu deszyfrowania w zależności od trybu i rozmiaru pliku', 
            'Czas [s]')