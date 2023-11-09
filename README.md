# debut-financial-model
Financial P&amp;L Model using Pandas

To use, update the user_parameters.yaml file to set the desired parameters. 
They are described here below: 

Revenues: 
Revenue obtained from pricing model (subscription based)

Costs: 
Cost of creating, maintaining the platform, and hosting it 
Salaries for small team of developers












Decay Factor for Advert Effectiveness: Over time, the same advert may become less effective as the target audience develops "ad fatigue". This can be modeled as a decay factor that reduces the number of new customers acquired each month the advert is active.

Varying Conversion Rates: Conversion rates might fluctuate based on various factors such as changes in the ad creative, platform algorithms, audience behavior changes, seasonality, or market trends.

Word-of-Mouth Effect: Satisfied users may recommend your platform to others, which can be modeled as a growth factor that depends on the current user base size.

Retargeting and Follow-Up Campaigns: If you run follow-up campaigns or retarget those who have shown interest but have not signed up, this could result in additional customer acquisition beyond the initial conversion.

Market Saturation: As you reach a larger portion of your target market, the pool of potential new customers naturally decreases, which should be reflected in a decreasing growth rate over time.

Budget Constraints: Your advertising budget may not be constant. If you have to reduce ad spend in certain months, the model should reflect that with lower customer acquisition in those periods.

Seasonality: Certain times of the year might have higher or lower engagement rates due to holidays, industry events, or other seasonal factors.

Here is an example of how you could implement some of these factors into your model:

python
Copy code
import pandas as pd
import numpy as np

class FacebookAdCampaign:
    
    def __init__(self, market_size, base_conv_rate, no_months, advert_timespan, decay_rate=0.95, word_of_mouth_coeff=0.01):
        self.market_size = market_size
        self.base_conv_rate = base_conv_rate
        self.no_months = no_months
        self.advert_timespan = advert_timespan
        self.decay_rate = decay_rate
        self.word_of_mouth_coeff = word_of_mouth_coeff

    def init_empty_df(self):
        return pd.DataFrame(index=range(self.no_months))

    def customersAquired(self):
        df = self.init_empty_df()
        df['Customers Aquired'] = 0
        df['Cumulative Customers'] = 0

        customers_acquired_last_month = 0

        for month in range(self.no_months):
            if month < self.advert_timespan:
                # Apply decay to the conversion rate over time
                conv_rate = self.base_conv_rate * (self.decay_rate ** month)
            else:
                # After the advert timespan, we might only get residual conversions
                conv_rate = self.base_conv_rate * (self.decay_rate ** self.advert_timespan) * 0.5  # Example of a residual factor

            new_customers = (self.market_size - df['Cumulative Customers'].iloc[max(0, month-1)]) * conv_rate

            # Add word-of-mouth effect based on the customers acquired last month
            wom_customers = customers_acquired_last_month * self.word_of_mouth_coeff
            
            total_new_customers = new_customers + wom_customers
            
            # Ensure we don't exceed the market size
            total_new_customers = min(self.market_size - df['Cumulative Customers'].iloc[max(0, month-1)], total_new_customers)

            df.at[month, 'Customers Aquired'] = total_new_customers
            
            # Keep track of the cumulative customers
            df['Cumulative Customers'] = df['Customers Aquired'].cumsum()
            
            customers_acquired_last_month = total_new_customers

        return df

# Usage example:
This example incorporates decay over the course of the advert timespan and a simple word-of-mouth effect. Adjust the decay_rate, word_of_mouth_coeff, and residual factors to fit your campaign's performance data or industry benchmarks.


Keep in mind that this is still a simplified model. Real-world customer acquisition modeling can be much more complex and may involve machine learning algorithms or sophisticated statistical methods to predict outcomes with higher accuracy.