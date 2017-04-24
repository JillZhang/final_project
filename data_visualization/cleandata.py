import sys
import json

for line in sys.stdin:
    try:
	i = line.strip()
	o = json.loads(i)
	p = o.strip()
	q = json.loads(p)
	
	if 'text' not in q.keys():
	    continue
	else:
	    #print q['user']['location']
	    print q['text']
    except:
	continue
