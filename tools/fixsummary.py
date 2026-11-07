# -*- coding: utf-8 -*-
"""修复 summary 环境闭合位置：应闭合在 problemset / reading 之前。"""
import glob
import io


def fix(path):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    starts = [i for i, l in enumerate(lines) if l.strip() == '\\begin{summary}']
    ends = [i for i, l in enumerate(lines) if l.strip() == '\\end{summary}']
    if not starts or not ends:
        return False
    s, e = starts[0], ends[-1]
    if s > e:
        return False
    # 找到 summary 内部的第一个结束标记
    close = None
    for k in range(s + 1, e):
        if lines[k].strip() in ('\\begin{problemset}', '\\begin{reading}'):
            close = k
            break
    if close is None:
        return False
    del lines[e]
    lines.insert(close, '\\end{summary}')
    lines.insert(close + 1, '')
    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    return True


if __name__ == '__main__':
    for f in sorted(glob.glob('chapters/*.tex')):
        if fix(f):
            print('fixed', f)
