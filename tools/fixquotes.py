# -*- coding: utf-8 -*-
"""把正文中的 ASCII 双引号成对替换为中文引号 “ ”，跳过代码环境。"""
import io
import re

FILES = [
    'chapters/ch01_overview.tex',
    'chapters/ch02_math.tex',
    'chapters/ch03_sensors.tex',
    'chapters/ch23_zlocalization.tex',
    'chapters/ch24_frontier.tex',
    'chapters/chapters_preface_tmp.tex',
    'chapters/preface.tex',
]


def convert_paragraph(p):
    if p.count('"') % 2 != 0:
        return p, 0
    out = []
    opening = True
    n = 0
    for ch in p:
        if ch == '"':
            out.append('\u201c' if opening else '\u201d')
            opening = not opening
            n += 1
        else:
            out.append(ch)
    return ''.join(out), n


def convert(text):
    parts = re.split(r'(\\begin\{lstlisting\}.*?\\end\{lstlisting\})', text, flags=re.S)
    total = 0
    new_parts = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            new_parts.append(part)
            continue
        subparts = re.split(r'(\\lstinline\{[^{}]*\})', part)
        for j, sp in enumerate(subparts):
            if j % 2 == 1:
                new_parts.append(sp)
                continue
            paras = sp.split('\n\n')
            new_paras = []
            for p in paras:
                np_, n = convert_paragraph(p)
                total += n
                new_paras.append(np_)
            new_parts.append('\n\n'.join(new_paras))
    return ''.join(new_parts), total


if __name__ == '__main__':
    for f in FILES:
        try:
            text = io.open(f, encoding='utf-8').read()
        except FileNotFoundError:
            continue
        new, n = convert(text)
        if n:
            io.open(f, 'w', encoding='utf-8', newline='\n').write(new)
        print(f, 'converted', n)
