import os
import subprocess
import pandas as pd
from datetime import datetime
import re

os.chdir(r'd:\_workspaces\Python\ping.py')
path = "data"
try:
    os.mkdir(path)
except OSError:
	None

result = subprocess.run(['python', 'ping.py','-c','100'], stdout=subprocess.PIPE)
#print(result.stdout)
p = re.compile('\\/(\\d+).+ - jitter: (\\d+)', re.DOTALL)
m = p.findall(result.stdout.decode('utf-8'))
d = {'datetime': datetime.now(), 'latency': [m[0][0]], 'jitter': [m[0][1]]}
df = pd.DataFrame(d)
output_path = 'data/data.csv'
fileExists = os.path.exists(output_path)
df.to_csv(output_path, mode='a', header=not fileExists)

#latency (MIN/MAX/AVG): 78/125/93\r\n - jitter: 10.4273\r\n
#datetime	latency	jitter
#2020-07-17	09:00	100	10

