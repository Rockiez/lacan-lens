#!/usr/bin/env python3
"""Offline release checks; stdlib only. No network, writes or imports of package code."""
from pathlib import Path
from collections import Counter
import re
import sys
from urllib.parse import urlsplit, unquote

FILES = {
    'SKILL.md', 'README.md', 'CHANGELOG.md', 'NOTICE.md', 'LICENSE.md',
    'references/source-audit.md', 'references/comprehensive-audit.md',
    'references/acceptance-cases.md', 'scripts/validate.py',
}
IDS = {f'{letter}{n:02}' for letter, count in [('A', 7), ('B', 7), ('C', 7), ('D', 4)] for n in range(1, count + 1)}
COUNTS = {'支持': 5, '需限定': 19, '未核实': 1}
ROWS = {
    '主人': ['S₁', 'S₂', 'S̸', 'a'],
    '大学': ['S₂', 'a', 'S₁', 'S̸'],
    '癔症者': ['S̸', 'S₁', 'a', 'S₂'],
    '分析家': ['a', 'S̸', 'S₂', 'S₁'],
}
COMMIT = '1aa086a47da0465f1ed46551b5510a29c60ad557'
PROJECT = 'kotoba-rin/Lacan-Chinese-Translation-Project'
GITHUB_PATHS = {
    '/' + PROJECT,
    '/' + PROJECT + '/blob/' + COMMIT + '/NOTICE.md',
    '/' + PROJECT + '/tree/' + COMMIT + '/texts',
    '/Liber1917/lacan-perspective-skill',
    '/Rockiez/lacan-lens',
}


def validate(documents):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    check(set(documents) == FILES, 'unexpected or missing package files')
    skill = documents.get('SKILL.md', '')
    check(skill.startswith('---\n'), 'frontmatter opening')
    parts = skill.split('\n---\n', 1)
    check(len(parts) == 2 and bool(parts[-1].strip()), 'frontmatter closing/body')
    fm = parts[0]
    for key, value in [('name', 'lacan-lens'), ('version', '1.1.0'), ('license', 'CC-BY-4.0')]:
        check(f'{key}: {value}' in fm.splitlines(), 'frontmatter ' + key)
    match = re.search(r'^description: "([^"\n]+)"$', fm, re.M)
    check(bool(match) and len(match[1]) <= 60 and match[1].endswith('.'), 'description format')
    check('platforms: [linux, macos, windows]' in fm, 'platforms')
    check('author:' in fm, 'public attribution missing')
    for phrase in ['不是没有情感、爱', '排他类别', '跨期统一终点', '升级表', '整理性名称', '首次课次仍未核实', '不声称完整校勘']:
        check(phrase in skill, 'missing boundary: ' + phrase)
    rows = {}
    for line in skill.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells and cells[0] in ROWS:
            check(cells[0] not in rows, 'duplicate discourse row')
            rows[cells[0]] = cells[1:]
    check(rows == ROWS, 'four discourse positions')
    check('| 话语 | 左上：施动者 | 右上：他者 | 左下：真理 | 右下：产物 |' in skill, 'position headings')
    audit = documents.get('references/comprehensive-audit.md', '')
    groups = re.findall(r'^## ([A-D]\d{2}) .+\n+\*\*结论：(支持|需限定|未核实)\*\*', audit, re.M)
    check(len(groups) == 25 and {g[0] for g in groups} == IDS, '25 unique audit groups')
    check(dict(Counter(g[1] for g in groups)) == COUNTS, 'audit status counts')
    check('不等于全部原典已证实' in audit and '未逐字对校' in audit, 'audit scope disclaimer')
    for block in re.split(r'^## [A-D]\d{2} ', audit, flags=re.M)[1:]:
        check('**定位：**' in block and '**限定与处置：**' in block, 'audit evidence/boundary missing')
    notice = documents.get('NOTICE.md', '')
    check('kotoba-rin' in notice and '贡献者' in notice and 'creativecommons.org/licenses/by/4.0/' in notice, 'attribution/license')
    # Personal context is reviewed separately before publication.
    sensitive = ['PRIVATE_' + 'CONTEXT_SENTINEL']
    path_pattern = r'/(?:opt|home|Users|root|workspace|volume\d|tmp|var)/(?:[^\s<>]+)'
    for name, text in documents.items():
        # Scan script too; URLs are removed only for machine-path detection.
        plain = re.sub(r'https?://[^\s<>`\)]+', '', text)
        check(not re.search(path_pattern, plain), name + ': internal absolute path')
        check(not re.search(r'[A-Za-z]:\\(?:Users|data)\\', plain), name + ': machine path')
        check(not re.search(r'\b(?:192\.168\.|10\.\d+\.)\d+', plain), name + ': private address')
        for term in sensitive:
            check(term.lower() not in text.lower(), name + ': private-context clue')
        check(not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text), name + ': personal email')
        check(not re.search(r'(?<![\w])@[A-Za-z][A-Za-z0-9_]{2,}', text), name + ': personal handle')
        check(not re.search(r'(?:username|user_id|chat_id)\s*[:=]\s*[\w@.-]+', text, re.I), name + ': private identifier')
        for url in re.findall(r'https?://[^\s<>`\)]+', text):
            parsed = urlsplit(url.rstrip('。，；'))
            if parsed.hostname in {'github.com', 'raw.githubusercontent.com'}:
                check(parsed.hostname == 'github.com' and unquote(parsed.path).rstrip('/') in GITHUB_PATHS,
                      name + ': unapproved or malformed GitHub path')
        if name.endswith('.md'):
            targets = re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)
            targets += re.findall(r'`((?:references|scripts)/[^`\s]+\.(?:md|py))`', text)
            for target in targets:
                if '://' in target or target.startswith('#'):
                    continue
                target = unquote(target.split('#')[0])
                check(not target.startswith('/') and '..' not in Path(target).parts, name + ': unsafe link')
                # References are relative to the referring document; inline root paths are supported.
                resolved = (Path(name).parent / target).as_posix()
                check(resolved in documents or target in documents, name + ': missing reference ' + target)
    return errors


def self_test(documents):
    tests = [
        ('missing file', 'NOTICE.md', None),
        ('missing reference', 'README.md', documents['README.md'] + '\n[bad](missing.md)'),
        ('missing group', 'references/comprehensive-audit.md', documents['references/comprehensive-audit.md'].replace('## D04 ', '## Z99 ')),
        ('wrong status', 'references/comprehensive-audit.md', documents['references/comprehensive-audit.md'].replace('**结论：未核实**', '**结论：支持**')),
        ('wrong position', 'SKILL.md', documents['SKILL.md'].replace('| 主人 | S₁ | S₂ | S̸ | a |', '| 主人 | a | S₂ | S̸ | S₁ |')),
        ('private path', 'README.md', documents['README.md'] + '\n/' + 'home/' + 'example/private'),
        ('private clue', 'README.md', documents['README.md'] + '\n' + 'PRIVATE_' + 'CONTEXT_SENTINEL'),
        ('bad GitHub path', 'README.md', documents['README.md'] + '\nhttps:' + '//github.com/' + PROJECT + '/blob/main/' + 'missing.md'),
        ('missing boundary', 'SKILL.md', documents['SKILL.md'].replace('不是没有情感、爱', '可能有关')),
    ]
    failed = []
    for label, path, value in tests:
        altered = dict(documents)
        if value is None:
            altered.pop(path)
        else:
            altered[path] = value
        if not validate(altered):
            failed.append(label)
    return failed, len(tests)


def main():
    root = Path(__file__).resolve().parents[1]
    documents = {}
    for path in root.rglob('*'):
        if '.git' in path.relative_to(root).parts or '__pycache__' in path.relative_to(root).parts:
            continue
        if path.is_symlink():
            print('FAIL: symlink in package')
            return 1
        if path.is_file():
            try:
                documents[path.relative_to(root).as_posix()] = path.read_text(encoding='utf-8')
            except (UnicodeError, OSError):
                print('FAIL: unreadable or binary file')
                return 1
    errors = validate(documents)
    if errors:
        print('\n'.join('FAIL: ' + e for e in errors))
        return 1
    failed, count = self_test(documents)
    if failed:
        print('FAIL: negative self-tests: ' + ', '.join(failed))
        return 1
    print(f'PASS: {len(documents)} files; 25 groups; 5 supported / 19 qualified / 1 unverified; four discourse positions; references; privacy clues; URL structure.')
    print(f'PASS: {count} negative self-tests detected intentionally introduced faults (memory only).')
    print('LIMIT: offline/static only; no live links, model behavior or primary-text re-verification.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
