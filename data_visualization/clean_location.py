import pandas as pd
import sys
import numpy as np

local_df = pd.read_table(sys.argv[1], names=['location'], header=None)



temp = []
for i in range(0, local_df.shape[0]):
    if local_df.location[i] in ['Los Angeles', 'San Diego, CA','California','California, USA', 'California', 'San Mateo, CA','Los Angeles', 'Los Angeles, CA', 'San Francisco','San Francisco, CA']:
	local_df.location[i] = 'CA'
    elif local_df.location[i] in ['New York City', 'New York, USA', 'New York','New York, NY', 'NYC', 'Brooklyn, NY']:
	local_df.location[i] = 'NY'
    elif local_df.location[i] in ['Houston, TX', 'Austin, TX', 'Dallas, TX', 'Texas','San Antonio, TX', 'Texas, USA']:
	local_df.location[i] = 'TX'
    elif local_df.location[i] in ['Chicago', 'Chicago, IL', 'Illinois','Illinois, USA']:
	local_df.location[i] = 'IL'
    elif local_df.location[i] in ['Florida, USA', 'Florida', 'Tampa, FL','Miami, FL', 'Jacksonville, FL']:
	local_df.location[i] = 'FL'
    elif local_df.location[i] in ['Washington, DC']:
	local_df.location[i] = 'DC'
    elif local_df.location[i] in ['Boston, MA', 'Massachusetts', 'Boston','Massachusetts, USA']:
	local_df.location[i] = 'MA'
    elif local_df.location[i] in ['Atlanta, GA', 'Georgia', 'Georgia, USA', 'Atlanta']:
	local_df.location[i] = 'GA'
    elif local_df.location[i] in ['Seattle, WA', 'Seattle', 'Washington, USA','Washington']:
	local_df.location[i] = 'WA'
    elif local_df.location[i] in ['Philadelphia, PA', 'Philadelphia','Pennsylvania, USA', 'Pennsylvania']:
	local_df.location[i] = 'PA'
    elif local_df.location[i] in ['Virginia, USA', 'Virginia','Virginia Beach, VA','Virginia Beach']:
	local_df.location[i] = 'VA'
    elif local_df.location[i] in ['Michigan, USA', 'Michigan', 'Detroit, MI','Detroit']:
	local_df.location[i] = 'MI'
    elif local_df.location[i] in ['Phoenix, AZ', 'Arizona, USA', 'Arizona', 'Phoenix']:
	local_df.location[i] = 'AZ'
    elif local_df.location[i] in ['Oregon, USA', 'Portland, Oregon', 'Portland', 'Oregon']:
	local_df.location[i] = 'OR'
    elif local_df.location[i] in ['Denver, CO', 'Denver', 'Colorado, USA', 'Colorado']:
	local_df.location[i] = 'CO'
    elif 'CA' in str(local_df.location[i]):
	local_df.location[i] = 'CA'
    elif 'NY' in str(local_df.location[i]):
	local_df.location[i] = 'NY'
    elif 'TX' in str(local_df.location[i]):
        local_df.location[i] = 'TX'
    elif 'FL' in str(local_df.location[i]):
        local_df.location[i] = 'FL'
    elif 'IL' in str(local_df.location[i]):
        local_df.location[i] = 'IL'
    elif 'PA' in str(local_df.location[i]):
        local_df.location[i] = 'PA'
    elif 'MA' in str(local_df.location[i]):
        local_df.location[i] = 'MA'
    elif 'GA' in str(local_df.location[i]):
        local_df.location[i] = 'GA'
    elif 'MI' in str(local_df.location[i]):
        local_df.location[i] = 'MI'
    elif 'DC' in str(local_df.location[i]):
        local_df.location[i] = 'DC'
    elif 'CO' in str(local_df.location[i]):
        local_df.location[i] = 'CO'
    elif 'AZ' in str(local_df.location[i]):
        local_df.location[i] = 'AZ'
    elif 'VA' in str(local_df.location[i]):
        local_df.location[i] = 'VA'
    elif 'OR' in str(local_df.location[i]):
        local_df.location[i] = 'OR'
    else:
	local_df.location[i] = 'nan'

print local_df.location.value_counts()[:80]
print len(local_df.location.value_counts())
local_df.location.value_counts().to_csv('final_location.csv')
