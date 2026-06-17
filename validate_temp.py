from html.parser import HTMLParser

class Validator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.stack = []
        self.ids = set()
        self.void_elements = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def handle_starttag(self, tag, attrs):
        if tag not in self.void_elements:
            self.stack.append((tag, self.getpos()))
        for name, value in attrs:
            if name == 'id':
                if value in self.ids:
                    self.errors.append(f'Duplicate id="{value}" at line {self.getpos()[0]}')
                self.ids.add(value)
            if value and '&' in value and '&amp;' not in value and '&#' not in value and '&nbsp;' not in value:
                self.errors.append(f'Possibly unencoded & in attribute {name} at line {self.getpos()[0]}')
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif self.stack:
            self.errors.append(f'Mismatched </{tag}> at line {self.getpos()[0]}')
    def handle_data(self, data):
        if '&' in data:
            lines = data.split('\n')
            for i, line in enumerate(lines):
                if '&' in line and not any(e in line for e in ['&amp;', '&lt;', '&gt;', '&quot;', '&#37;']):
                    lineno = self.getpos()[0]
                    self.errors.append(f'Possibly unencoded & in text at line {lineno}: {line.strip()[:80]}')
    def done(self):
        for tag, pos in self.stack:
            self.errors.append(f'Unclosed <{tag}> at line {pos[0]}')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

v = Validator()
v.feed(content)
v.done()
print(f'Total issues: {len(v.errors)}')
for e in v.errors[:50]:
    print(e)
if len(v.errors) > 50:
    print(f'... and {len(v.errors)-50} more')
