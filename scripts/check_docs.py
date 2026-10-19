"""Check a deliberately small, documented subset of the editorial rules."""
from pathlib import Path
import re
import sys

REQUIRED = ('Перед началом', 'Порядок действий', 'Результат', 'Если возникла проблема')
FORBIDDEN = {
    r'\bслот(?:а|ы|ов|у|ом|е|ами|ах)?\b': 'SG-10: используйте «интервал»',
    r'\bтаймслот\w*\b': 'SG-10: используйте «интервал»',
    r'\bаккаунт\w*\b': 'SG-10: используйте «учётная запись»',
    r'\bуч[её]тка\w*\b': 'SG-10: используйте «учётная запись»',
    r'\bброн(?:ь|и|ью|ей)\b': 'SG-10: используйте «запись»',
    r'\bбронировани\w*\b': 'SG-10: используйте «запись»',
    r'\[(?:тут|здесь|подробнее)\]\(': 'SG-20: дайте ссылке содержательное название',
    r'!\[\s*\]\(': 'Изображение Markdown должно иметь альтернативный текст',
}

def check_instruction(text, name):
    errors = []
    for heading in REQUIRED:
        if not re.search(r'^## ' + re.escape(heading) + r'\s*$', text, re.M):
            errors.append(f'{name}: отсутствует раздел «{heading}» (SG-12)')
    for number, line in enumerate(text.splitlines(), 1):
        for pattern, explanation in FORBIDDEN.items():
            if re.search(pattern, line, re.I):
                errors.append(f'{name}:{number}: {explanation}')
    if 'UTC+3' not in text:
        errors.append(f'{name}: укажите UTC+3 (SG-25)')
    return errors

def main():
    paths = [Path(p) for p in sys.argv[1:]] or sorted(Path('docs/examples').glob('*.md'))
    if not paths:
        print('Не найдены инструкции для проверки', file=sys.stderr)
        return 2
    errors = []
    for path in paths:
        if not path.is_file():
            errors.append(f'{path}: файл не найден')
            continue
        errors.extend(check_instruction(path.read_text(encoding='utf-8'), str(path)))
    for error in errors:
        print(error)
    print(f'Проверено инструкций: {len(paths)}; замечаний: {len(errors)}')
    return int(bool(errors))

if __name__ == '__main__':
    raise SystemExit(main())
