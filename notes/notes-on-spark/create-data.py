import pandas as pd
import json
import numpy as np
import string

N = 1000

df = pd.DataFrame({
    'order_id': np.arange(N),
    'customer_id': np.random.choice(np.arange(1, N), N),
    'item': np.random.choice(list(string.ascii_lowercase), N)
}).to_dict(orient='recods')

with open('fake-orders.json', 'w') as f:
    for line in df:
        f.write(json.dumps(line) + '\n')
