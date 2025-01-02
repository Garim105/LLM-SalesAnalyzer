import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_and_clean_data(file_path):
    
    data = pd.read_csv(file_path)
    data = data.drop_duplicates()

    for col in data.columns:
        if 'date' in col.lower():
            data[col] = pd.to_datetime(data[col], errors='coerce')  
            data[col] = data[col].dt.date  
    
    data = data.fillna(0) 

    if 'Unnamed: 0' in data.columns:
        data = data.drop(columns=['Unnamed: 0'])

    return data

def detect_dimensions_and_measures(data):
    
    dimensions = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    datetime_columns = data.select_dtypes(include=['datetime', 'datetime64']).columns.tolist()
    dimensions.extend(datetime_columns)
    
    measures = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print("Dimensions:", dimensions)
    print("Measures:", measures)
    return dimensions, measures

def perform_descriptive_analysis(data, dimensions, measures):
    analysis_results = {}
    
    measure_stats = data[measures].describe()
    analysis_results['measure_stats'] = measure_stats
    
    grouped_analysis = {}
    for dim in dimensions:
        grouped_data = {}
        for measure in measures:
            grouped_data[measure] = data.groupby(dim)[measure].agg(['mean', 'sum', 'count'])
        grouped_analysis[dim] = grouped_data
    
    analysis_results['grouped_analysis'] = grouped_analysis
    
    return analysis_results

def visualize_data(data, dimensions, measures, max_unique_values=30):

    for dim in dimensions:
        unique_dim_values = data[dim].nunique()
        for measure in measures:
    
            if unique_dim_values > 500: #500 can be done dynamic based on the total data in the sheet
                print(f"Skipping visualization of {measure} by {dim}: {measure} is not a meaningful measure.")
                continue  
            
            print(f"Visualizing {measure} by {dim}")
            
            if unique_dim_values > max_unique_values:
                print(f"Splitting {dim} into chunks since it has too many unique values: {unique_dim_values} unique values")

                unique_values = data[dim].unique()
                chunks = [unique_values[i:i + max_unique_values] for i in range(0, len(unique_values), max_unique_values)]
                
                for chunk_idx, chunk in enumerate(chunks):
                    plt.figure(figsize=(10, 6))
                    subset = data[data[dim].isin(chunk)]
                    sns.barplot(x=dim, y=measure, data=subset)
                    plt.title(f'{measure} by {dim} (Chunk {chunk_idx+1}/{len(chunks)})')
                    plt.xticks(rotation=45)
                    plt.show()
            else:
                
                plt.figure(figsize=(10, 6))
                try:
                    sns.barplot(x=dim, y=measure, data=data)
                    plt.title(f'{measure} by {dim}')
                    plt.xticks(rotation=45)
                    plt.show()
                except Exception as e:
                    print(f"Error visualizing {measure} by {dim}: {e}")

def analyze_sales_data(file_path):

    data = load_and_clean_data(file_path)
    dimensions, measures = detect_dimensions_and_measures(data)
    analysis_results = perform_descriptive_analysis(data, dimensions, measures)
    
    visualize_data(data, dimensions, measures)
    
    return analysis_results

file_path = "Sales Data.csv"
analysis_results = analyze_sales_data(file_path)
print(analysis_results['measure_stats'])
