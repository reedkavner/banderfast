import json
from operator import itemgetter

def url_cleaner(s):
	s = s.lower()
	return s.lstrip('url(').rstrip(')')

with open('bandersnatch.json') as f:
	j = json.load(f)

p = j['jsonGraph']['videos']['80988062']['interactiveVideoMoments']['value']['choicePointNavigatorMetadata']['choicePointsMetadata']['choicePoints']

points_unordered = []

for k,v in p.iteritems():
	if "fake" not in k.lower():
		d = dict(
		time = v['startTimeMs'],
		point_id = k,
		description = v['description'],
		image = url_cleaner(v['image']['styles']['backgroundImage']))
		points_unordered.append(d)

points= sorted(points_unordered, key=itemgetter('time'), reverse=False)

for p in points:
	#these are the phone number prompts
	if p['point_id'] not in ["6A", "6B"] :
		options = j['jsonGraph']['videos']['80988062']['interactiveVideoMoments']['value']['momentsBySegment'][p['point_id']]
		for i in options:
			#make sure we're in the right dict
			if "scene:" in i["type"].lower():
				choices = []
				for c in i['choices']:
					choice = {}
					choice['text'] = c['text']
					
					try:
						choice['jump_time'] = c['startTimeMs']
					except KeyError:
						choice['jump_time'] = None
					
					try:
						choice['image'] = url_cleaner(c['image']['styles']['backgroundImage'])
					except KeyError:
						choice['image'] = None

					choices.append(choice)

				p['choices'] = choices


#print json.dumps(points, indent=4, sort_keys=True)

with open("banderfast.json","w") as f:
	f.write(json.dumps(points))
