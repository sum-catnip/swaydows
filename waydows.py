#!/usr/bin/env python3

import subprocess
import itertools
import json

def run(*cmd):
    return subprocess \
        .run(cmd, capture_output=True)  \
        .stdout \
        .decode('utf-8')


def deepflat(head):
    for i in head.get('nodes') or []:
        yield from deepflat(i)
        yield i


def format_window(w):
    id = w['id']
    name = w['name'] or ''
    app = w['app_id'] or w.get('window_properties').get('class') or ''
    return(f"{id} {app}: {name}")


windows = list(
    filter(lambda w: not w['focus'],
        deepflat(json.loads(run('swaymsg', '-t', 'get_tree'))))
)

print('\n'.join(map(format_window, filter(lambda w: 'app_id' in w.keys(),
    windows))))
