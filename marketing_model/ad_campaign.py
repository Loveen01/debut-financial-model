import pandas as pd
import numpy as np
from cashflow_model.base_model import BaseModel

class AdCampaign(BaseModel):
    '''Model an ad campaign for a period of time, used to calculate the number of customers aquired'''
    
    def __init__(self, ad_viewers, click_rate=0.5, base_conv_rate=0.2, advert_timeframe=10, conv_decay=1, word_of_mouth_coeff=0.1, viewership_change_rate = 0.1):
        super().__init__()
        self.ad_viewers = ad_viewers 
        self.viewership_change_rate = viewership_change_rate # rate of decrease of ad-viewers monthly
        self.click_rate = click_rate # rate of viewers clicking ad
        self.base_conv_rate = base_conv_rate # month 1 conversion rate (this may be constant for all rates, if conv_decay = 1)
        self.conv_decay = conv_decay # rate at which conversion rate will decrease monthly. base_conv_rate * conv_rate^month 
        self.advert_timeframe = advert_timeframe # period of time to keep advert for
        self.word_of_mouth_coeff = word_of_mouth_coeff # 1 means we have the same wom customers as last months newcomers (very optimistic)

        self.monthly_conv_rates = self.__init_empty_df(1)
        self.monthly_visitors = self.__init_empty_df(1)

        if self.advert_timeframe > self.model_timeframe:
            raise ValueError ("Advert_timeframe is longer than model_timeframe, check configurations")

    def __init_empty_df(self, index_no, row_names = None):
        '''Creates an empty dataframe, filed with zeros'''
        if row_names is None:
            row_names = [f'Row_{i}' for i in range(index_no)]
        elif len(row_names) != index_no:
            raise ValueError("Length of row_names should match index_no")
        df = pd.DataFrame(index = row_names, columns = range(self.model_timeframe))
        return df.fillna(0)

    def __calc_monthly_visitors(self):
        '''converts ad-viewers to number of visitors of debut website, 
        incoorporating viewership ad rate, seasonality + small randomness'''

        self.monthly_visitors = self.__init_empty_df(1)

        seasonality_effect = [1.0, 1.2, 0.8, 1.0]  # A simple pattern repeated for each season or quarter

        # simulate random fluctuations with a small random factor
        random_fluctuation = np.random.normal(1.0, 0.05, self.model_timeframe)  # with mean=1.0, std=0.05

        for month in range(self.advert_timeframe):
            seasonal_index = month % len(seasonality_effect)

            self.monthly_visitors.iloc[0, month] = (self.click_rate * self.ad_viewers 
                                             * self.viewership_change_rate ** month
                                    * seasonality_effect[seasonal_index] * random_fluctuation[month])
            
            self.ad_viewers *= self.viewership_change_rate

        return self.monthly_visitors

    def __calc_monthly_conv_rates(self):
        '''calculates conversion rates over time of the ad, incoorporating a decay into it'''
        self.monthly_conv_rates = self.__init_empty_df(1)
        self.monthly_conv_rates.loc[0,0] = self.base_conv_rate

        for month in range(0, self.advert_timeframe):
            # Apply decay to the conversion rate over time
            self.monthly_conv_rates.loc[0, month+1] = self.base_conv_rate * (self.conv_decay ** month+1)
            # After the advert timespan, we might only get residual conversions
        for month in range(self.advert_timeframe, self.model_timeframe):
            self.monthly_conv_rates.loc[0, month+1] = self.base_conv_rate * (self.conv_decay ** self.advert_timeframe) * 0.5  # Example of a residual factor
        
        return self.monthly_conv_rates

    def calc_customers_acquired_df(self):
        '''Uses conversion rates and visitors model to calculate customers aquired'''

        self.__calc_monthly_conv_rates()
        self.__calc_monthly_visitors()
        
        df = self.__init_empty_df(1, ['Customers Acquired'])
        
        df.loc['Customers Acquired'] = 0
        # df.loc['Cumulative Customers'] = 0

        customers_acquired_last_month = 0

        for month in range(self.model_timeframe):
            # apply conversion rate to new monthly customers, assuming respective models are independent on one another
            new_customers = self.monthly_visitors.iloc[0,month] * self.monthly_conv_rates.iloc[0,month]
            
            # word of mouth customers assumes sole dependence on last months newcomers
            wom_customers = customers_acquired_last_month * self.word_of_mouth_coeff

            total_new_customers = new_customers + wom_customers
            
            # update last months 
            customers_acquired_last_month = total_new_customers

            # new customer aquired through 
            df.loc['Customers Acquired', month] = total_new_customers
        
        # df.loc['Cumulative Customers'] = df.loc['Customers Acquired'].cumsum()

        df_rounded = df.apply(np.round).astype(int)
        
        newly_acquired_customers = df_rounded.loc['Customers Acquired'] 
        # cumulative_customers = df_rounded.loc['Cumulative Customers']

        return newly_acquired_customers