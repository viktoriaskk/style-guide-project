import unittest
from scripts.check_docs import check_instruction

BASE = '''# Инструкция

## Перед началом

Время UTC+3.

## Порядок действий

1. Откройте **Консультации**.

## Результат

Запись подтверждена.

## Если возникла проблема

Проверьте список.
'''

class EditorialChecks(unittest.TestCase):
    def test_valid_instruction(self):
        self.assertEqual(check_instruction(BASE, 'example'), [])

    def test_catches_missing_result(self):
        errors = check_instruction(BASE.replace('## Результат', '## Итог'), 'example')
        self.assertTrue(any('Результат' in item for item in errors))

    def test_catches_inflected_term(self):
        errors = check_instruction(BASE + '\nВыберите слотами и аккаунт.\n', 'example')
        self.assertTrue(any('учётная запись' in item for item in errors))
        errors = check_instruction(BASE + '\nВыберите слот.\n', 'example')
        self.assertTrue(any('интервал' in item for item in errors))

    def test_catches_timezone_omission(self):
        self.assertTrue(any('UTC+3' in item for item in check_instruction(BASE.replace('UTC+3', ''), 'example')))

    def test_catches_link_and_image(self):
        errors = check_instruction(BASE + '\n[здесь](x.md)\n![](x.png)\n', 'example')
        self.assertEqual(len(errors), 2)

    def test_does_not_confuse_substrings(self):
        self.assertEqual(check_instruction(BASE + '\nСлово «кислота» не является термином интерфейса.\n', 'example'), [])

if __name__ == '__main__':
    unittest.main()
