import pandas as pd
import openai
import seaborn as sns
import matplotlib.pyplot as plt

#an encountering quota limitations with the OpenAI API,
openai.api_key = 'Dummy Token'

def load_and_clean_data(file_path):
    data = pd.read_csv(file_path)
    data = data.drop_duplicates()
    data = data.fillna(0)
    return data

def use_llm_for_analysis(data):

    data_dict = data.to_dict(orient='list')
    
    
    prompt = f"""
    You are given a dataset in this format: {data_dict}. 
    Please identify the categorical variables (dimensions) and numerical variables (measures) automatically. 
    Then, decide which analyses (descriptive statistics) should be done for this data. 
    Also, suggest the appropriate charts to visualize the data and trends based on its structure.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    analysis = response.choices[0].message['content']
    return analysis

def generate_visualizations(data, llm_analysis):
    
    if "sales by region" in llm_analysis:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='region', y='sales', data=data)
        plt.title('Sales by Region')
        plt.xticks(rotation=45)
        plt.show()

    if "sales over time" in llm_analysis:
        plt.figure(figsize=(10, 6))
        sns.lineplot(x='date', y='sales', data=data)
        plt.title('Sales Over Time')
        plt.xticks(rotation=45)
        plt.show()

# Step 4: Main function to execute the full process
def analyze_sales_data(file_path):
    # Load and clean the data
    data = load_and_clean_data(file_path)
    
    # Step 2: Use LLM to generate insights on dimensions, measures, and analyses
    llm_analysis = use_llm_for_analysis(data)
    
    # Step 3: Based on LLM's recommendations, generate visualizations automatically
    generate_visualizations(data, llm_analysis)

    # Print out LLM's recommendations and insights
    print("LLM Analysis and Recommendations:")
    print(llm_analysis)

# Example usage
file_path = "Sales Data.csv"
analyze_sales_data(file_path)
