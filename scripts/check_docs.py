"""Check repository-relative Markdown links; remote and anchor checks are separate."""
from pathlib import Path
import re
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
errors = []
for page in root.rglob('*.md'):
    if any(part in {'.git', '.venv', 'build', 'outputs'} for part in page.relative_to(root).parts):
        continue
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', page.read_text()):
        target = target.split('#', 1)[0]
        if not target or '://' in target or target.startswith('mailto:'):
            continue
        path = page.parent / unquote(target)
        if not path.exists():
            errors.append(f'{page.relative_to(root)}: {target}')
if errors:
    raise SystemExit('Missing local links:\n' + '\n'.join(errors))
print('Local Markdown links passed.')
