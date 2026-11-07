# -*- coding: utf-8 -*-
"""把章末的“本章小结 / 思考与练习 / 延伸阅读”改成 ElegantBook 风格环境。"""
import glob
import io
import os

SUM = r'\section*{本章小结}'
SUM2 = r'\section{本章小结}'
CH = r'\section*{思考与练习}'
CH2 = r'\section{思考与练习}'
READ = r'\section*{延伸阅读}'
READ2 = r'\section{延伸阅读}'


def convert(path):
    text = io.open(path, encoding='utf-8').read()
    if '\\section' not in text:
        return []
    lines = text.split('\n')
    changed = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()

        if s in (SUM, SUM2):
            j = i + 1
            while j < len(lines):
                t = lines[j].strip()
                if (t.startswith('\\section') or t.startswith('\\begin{problemset}')
                        or t.startswith('\\begin{reading}')
                        or t.startswith('\\end{document}')):
                    break
                j += 1
            lines[i] = '\\begin{summary}'
            lines[j:j] = ['', '\\end{summary}', '']
            changed.append('summary')
            i = j + 3
            continue

        if s in (CH, CH2):
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and lines[j].strip() == '\\begin{enumerate}':
                lines[i] = '\\begin{problemset}'
                del lines[j]
                depth = 1
                k = j
                while k < len(lines):
                    t = lines[k].strip()
                    if t.startswith('\\begin{enumerate}'):
                        depth += 1
                    elif t.startswith('\\end{enumerate}'):
                        depth -= 1
                        if depth == 0:
                            lines[k] = '\\end{problemset}'
                            break
                    k += 1
                changed.append('problemset')
                i = k + 1
                continue
            print('  SKIP exercises (no enumerate):', os.path.basename(path))

        if s in (READ, READ2):
            j = i + 1
            while j < len(lines):
                t = lines[j].strip()
                if t.startswith('\\section') or t.startswith('\\end{document}'):
                    break
                j += 1
            lines[i] = '\\begin{reading}'
            lines[j:j] = ['', '\\end{reading}', '']
            changed.append('reading')
            i = j + 3
            continue

        i += 1

    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    return changed


if __name__ == '__main__':
    total = {}
    for f in sorted(glob.glob('chapters/*.tex')):
        c = convert(f)
        if c:
            print(os.path.basename(f), '->', ','.join(c))
            for x in c:
                total[x] = total.get(x, 0) + 1
    print('TOTAL', total)
