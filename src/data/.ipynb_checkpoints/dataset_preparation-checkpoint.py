import pandas as pd
import os
from datetime import datetime

class DatasetPreparation:
    def __init__(self, s3_bucket):
        self.s3_bucket = s3_bucket
        self.s3 = boto3.client('s3')
    
    def prepare_training_data(self, companies=['AAPL', 'GOOGL', 'MSFT']):
        """Prepare dataset from multiple sources"""
        
        dataset = []
        
        for company in companies:
            # Get SEC filings
            filing_url = get_sec_filing(company)
            
            # Get financial news
            news = get_financial_news(os.environ['NEWS_API_KEY'], company)
            
            # Get stock data
            stock_data = get_stock_data(company)
            
            # Combine data
            combined_data = self.process_company_data(
                filing_url, 
                news, 
                stock_data
            )
            
            dataset.append(combined_data)
        
        # Save to S3
        df = pd.concat(dataset)
        self.save_to_s3(df, 'training_data.csv')
        
        return df
    
    def save_to_s3(self, df, filename):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        self.s3.put_object(
            Bucket=self.s3_bucket,
            Key=f'datasets/{filename}',
            Body=csv_buffer.getvalue()
        )