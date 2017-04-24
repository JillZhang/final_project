import pandas as pd
import sys
import numpy as np
from datetime import datetime

# time variable
time_df = pd.read_table(sys.argv[1], header=None, names=['time'])


temp = []
for i in range(0, len(time_df)):
    try:
        d = datetime.strptime(time_df.time[i], '%a %b %d %H:%M:%S +0000 %Y')
        temp.append(d.strftime('%Y-%m-%d-%H-%M'))
    except:
	continue

output = pd.DataFrame(temp, columns=['time'])
print output.sort_values('time')
output['sort_time'] = output.sort_values('time')
output.sort_time.value_counts(sort=False).sort_index().to_csv('final_time.csv')
print output.sort_time.value_counts(sort=False).sort_index()
