import glob
import json

for fn in glob.glob('*.json'):
    with open(fn) as f:
        print(fn)
        v = json.loads(f.read())
        title = v['title']

        event_tag = " (Pyohio 2019)"
        if title[len(title)-len(event_tag):] == event_tag:
            title = title[:len(title)-len(event_tag)]
        try:
            title, speakers = title.rsplit(' - ', 1)
        except ValueError:
            title = title.rstrip(' - ')
            speakers = None
        title = title.strip('\"')
        title = title.rstrip('\"')

        if speakers:
            speakers = speakers.split(', ')

        print('Title was: ' + v['title'])
        print('\tTitle is: ' + title)
        print('\tAuthor is: ' + str(speakers))

        v['title'] = title
        v['speakers'] = speakers

    with open(fn, 'w') as f:
        f.write(json.dumps(v))
