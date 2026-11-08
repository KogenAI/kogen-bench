#!/usr/bin/env python3
from datetime import datetime
for name, start, end in [('Studio', '05:10:51', '06:45:09'), ('MacBook', '05:04:51', '06:42:45')]:
    fmt = '%H:%M:%S'
    seconds = int((datetime.strptime(end, fmt) - datetime.strptime(start, fmt)).total_seconds())
    print(f'{name}: {seconds // 60}m {seconds % 60}s; blocking call unresolved')
