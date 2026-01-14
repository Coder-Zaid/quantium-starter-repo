import pandas as pd
import os

def process_sales_data():
    # Initialize an empty list to store dataframes
    dfs = []
    
    # Directory containing the CSV files
    data_dir = 'data'
    
    # Process each CSV file
    for filename in ['daily_sales_data_0.csv', 'daily_sales_data_1.csv', 'daily_sales_data_2.csv']:
        file_path = os.path.join(data_dir, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Filter for pink morsels only
        df = df[df['product'] == 'pink morsel'].copy()
        
        # Convert price from string to float (remove $ sign and convert)
        df['price'] = df['price'].str.replace('$', '').astype(float)
        
        # Calculate sales (price * quantity)
        df['sales'] = df['price'] * df['quantity']
        
        # Select only the required columns
        df = df[['sales', 'date', 'region']]
        
        # Append to the list
        dfs.append(df)
    
    # Combine all dataframes
    final_df = pd.concat(dfs, ignore_index=True)
    
    # Save to output file
    output_file = 'pink_morsel_sales.csv'
    final_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")
    print(f"Total rows: {len(final_df)}")

if __name__ == "__main__":
    process_sales_data()
