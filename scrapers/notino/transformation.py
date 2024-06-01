import pandas as pd
from datetime import datetime

class NotinoTransformation:
    def __init__(self, country: str, retailer: str):
        self.country = country
        self.retailer = retailer


    def transform_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        transformed_df = raw_df.copy()

        #Filter out rows where 'Price' is "not_available"
        valid_price_mask = transformed_df['Price'] != 'not_available'

        #Apply transformations only to rows with valid prices
        transformed_df.loc[valid_price_mask, 'Price'] = transformed_df.loc[valid_price_mask, 'Price'].str.replace(',', '.').astype(float)
        transformed_df.loc[valid_price_mask, 'Promo'] = transformed_df.loc[valid_price_mask, 'Promo'].str.replace('%', '').str.replace('-', '').astype(float)
        # Calculate 'Price_After_Discount' only for valid rows
        transformed_df.loc[valid_price_mask, 'Price_After_Discount'] = transformed_df.loc[valid_price_mask, 'Price'] - (transformed_df.loc[valid_price_mask, 'Price'] * transformed_df.loc[valid_price_mask, 'Promo'] / 100)
        
        return transformed_df

def main(raw_df: pd.DataFrame, country: str, retailer: str):
    transformation = NotinoTransformation(country=country, retailer=retailer)
    transformed_df = transformation.transform_data(raw_df)
    return transformed_df

if __name__ == "__main__":
    raw_df = pd.read_csv("notino_raw.csv")
    transformed_df = main(raw_df, country="it", retailer="notino")
    transformed_df.to_csv("notino_transformed.csv", index=False)
