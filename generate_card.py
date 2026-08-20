"""
Regenerates light_mode.svg and dark_mode.svg from the config below.

Edit CONFIG, run `python3 generate_card.py`, commit. The next Actions run
(or `python3 today.py`) fills in the live numbers; the placeholder values
here only matter until then.

Layout is adapted from https://github.com/Andrew6rant/Andrew6rant
"""

# ── everything you'd want to edit lives here ──────────────────────────────
CONFIG = {
    'prompt': 'ishan@buyyanapragada',
    'info': [
        ('OS', 'macOS 26, Ubuntu 24.04'),
        ('Uptime', None),  # None -> live counter, filled by today.py
        ('Host', 'University of Illinois Urbana-Champaign'),
        ('Kernel', 'B.S. Computer Science'),
        ('IDE', 'VSCode, Neovim, Claude Code'),
        None,  # blank row
        ('Languages.Programming', 'C++, Python, TypeScript, JavaScript'),
        ('Languages.Computer', 'HTML, CSS, SQL, LaTeX, YAML'),
        ('Languages.Real', 'English'),
        None,
        ('Hobbies.Software', 'Storage engines, browser extensions'),
        ('Hobbies.Research', 'Health infodemics, applied ML'),
    ],
    'contact': [
        ('Email.Personal', 'ishanpragada@gmail.com'),
        ('Email.School', 'ibuyy@illinois.edu'),
        ('Website', 'ishankr.com'),
        ('LinkedIn', 'ishanpragada'),
        ('X', 'ishanbuy'),
    ],
    'banner': [
        '██╗███████╗██╗  ██╗ █████╗ ███╗   ██╗',
        '██║██╔════╝██║  ██║██╔══██╗████╗  ██║',
        '██║███████╗███████║███████║██╔██╗ ██║',
        '██║╚════██║██╔══██║██╔══██║██║╚██╗██║',
        '██║███████║██║  ██║██║  ██║██║ ╚████║',
        '╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝',
    ],
    'subtitle': 'B U Y Y A N A P R A G A D A',
    'terminal': [
        ('$ whoami', None),
        (None, '> cs @ illinois'),
        None,
        ('$ cat stack.txt', None),
        (None, '> c++ · python · typescript'),
        None,
        ('$ ls ~/interests', None),
        (None, '> systems/  latency/  ml/'),
        None,
        ('$ █', None),
    ],
}

THEMES = {
    'dark_mode.svg': {
        'bg': '#161b22', 'fg': '#c9d1d9', 'key': '#ffa657', 'value': '#a5d6ff',
        'add': '#3fb950', 'del': '#f85149', 'cc': '#616e7f', 'dim': '#8b949e',
        'swatch': ['#f85149', '#ffa657', '#e3b341', '#3fb950', '#39c5cf', '#58a6ff', '#bc8cff'],
    },
    'light_mode.svg': {
        'bg': '#f6f8fa', 'fg': '#24292f', 'key': '#953800', 'value': '#0a3069',
        'add': '#1a7f37', 'del': '#cf222e', 'cc': '#c2cfde', 'dim': '#57606a',
        'swatch': ['#cf222e', '#bc4c00', '#9a6700', '#1a7f37', '#1b7c83', '#0969da', '#8250df'],
    },
}

# ── geometry ──────────────────────────────────────────────────────────────
WIDTH = 985
ART_X, INFO_X = 15, 390
ROW_0, ROW_H = 30, 20
BANNER_Y, BANNER_H = 72, 17   # banner sits on a tighter rhythm, see build_art_lines
BOX_Y = 230                   # top border of the terminal box
LINE_W = 60          # every info line is padded to exactly this many chars
ART_W = 37           # banner width, also the terminal box width


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def info_row(key, value, dots_id=None, value_id=None):
    """'. Key: ....... Value' padded so the line ends at column LINE_W."""
    dots_len = LINE_W - (2 + len(key) + 1 + len(value))
    dots = ' ' + '.' * (dots_len - 2) + ' ' if dots_len > 2 else ' ' * dots_len
    key_spans = '.'.join('<tspan class="key">%s</tspan>' % esc(part)
                         for part in key.split('.'))
    return (
        '<tspan class="cc">. </tspan>%s:'
        '<tspan class="cc"%s>%s</tspan>'
        '<tspan class="value"%s>%s</tspan>' % (
            key_spans,
            ' id="%s"' % dots_id if dots_id else '', dots,
            ' id="%s"' % value_id if value_id else '', esc(value)))


def header_row(title):
    """'- Title -————————…' filling the full line width."""
    return '<tspan x="%d" y="%%d">- %s</tspan> -%s-—-' % (
        INFO_X, esc(title), '—' * (LINE_W - len(title) - 7))


def build_info_lines():
    """Returns the right-hand column as a list of inner-XML strings."""
    lines = ['<tspan x="%d" y="%%d">%s</tspan> -%s-—-' % (
        INFO_X, esc(CONFIG['prompt']), '—' * (LINE_W - len(CONFIG['prompt']) - 5))]

    def section(entries):
        for entry in entries:
            if entry is None:
                lines.append('<tspan class="cc">. </tspan>')
                continue
            key, value = entry
            if key == 'Uptime':
                lines.append(info_row(key, '00 years, 00 months, 00 days',
                                      'age_data_dots', 'age_data'))
            else:
                lines.append(info_row(key, value))

    section(CONFIG['info'])
    lines.append('')                    # gap above a section header
    lines.append(header_row('Contact'))
    section(CONFIG['contact'])
    lines.append('')
    lines.append(header_row('GitHub Stats'))
    lines += [
        '<tspan class="cc">. </tspan><tspan class="key">Repos</tspan>:'
        '<tspan class="cc" id="repo_data_dots"> .... </tspan>'
        '<tspan class="value" id="repo_data">00</tspan>'
        ' {<tspan class="key">Contributed</tspan>: '
        '<tspan class="value" id="contrib_data">000</tspan>}'
        ' | <tspan class="key">Stars</tspan>:'
        '<tspan class="cc" id="star_data_dots"> ........... </tspan>'
        '<tspan class="value" id="star_data">000</tspan>',

        '<tspan class="cc">. </tspan><tspan class="key">Commits</tspan>:'
        '<tspan class="cc" id="commit_data_dots"> .................. </tspan>'
        '<tspan class="value" id="commit_data">0,000</tspan>'
        ' | <tspan class="key">Followers</tspan>:'
        '<tspan class="cc" id="follower_data_dots"> ....... </tspan>'
        '<tspan class="value" id="follower_data">000</tspan>',

        '<tspan class="cc">. </tspan>'
        '<tspan class="key">Lines of Code on GitHub</tspan>:'
        '<tspan class="cc" id="loc_data_dots">. </tspan>'
        '<tspan class="value" id="loc_data">000,000</tspan>'
        ' ( <tspan class="addColor" id="loc_add">000,000</tspan>'
        '<tspan class="addColor">++</tspan>, '
        '<tspan id="loc_del_dots"> </tspan>'
        '<tspan class="delColor" id="loc_del">00,000</tspan>'
        '<tspan class="delColor">--</tspan> )',
    ]
    return lines


def build_art_lines(theme):
    """
    Returns the left column as (y, inner-XML) pairs.

    The banner rows sit on their own 17px rhythm rather than the 20px grid:
    U+2588 FULL BLOCK is about 18.7px tall at this size, so 20px spacing
    leaves a hairline seam through every letter stem. 17px overlaps instead,
    which reads as solid in any monospace font.
    """
    rows = []
    y = BANNER_Y
    for row in CONFIG['banner']:
        rows.append((y, esc(row)))
        y += BANNER_H
    rows.append((y + 25, '<tspan class="dim">%s</tspan>' % esc(
        CONFIG['subtitle'].center(ART_W).rstrip())))

    box = lambda l, body, r: '<tspan class="dim">%s</tspan>%s<tspan class="dim">%s</tspan>' % (l, body, r)
    y = BOX_Y
    rows.append((y, box('╭', '<tspan class="dim">%s</tspan>' % ('─' * (ART_W - 2)), '╮')))
    for entry in CONFIG['terminal']:
        y += ROW_H
        if entry is None:
            rows.append((y, box('│', ' ' * (ART_W - 2), '│')))
            continue
        cmd, out = entry
        text = cmd or out
        body = ' <tspan class="%s">%s</tspan>%s' % (
            'key' if cmd else 'value', esc(text), ' ' * (ART_W - 3 - len(text)))
        rows.append((y, box('│', body, '│')))
    rows.append((y + ROW_H, box('╰', '<tspan class="dim">%s</tspan>' % ('─' * (ART_W - 2)), '╯')))

    swatch = '     ' + ' '.join(
        '<tspan class="sw%d">███</tspan>' % i for i in range(len(theme['swatch'])))
    rows.append((y + ROW_H * 3, swatch))
    return rows


def render(theme):
    art = build_art_lines(theme)
    info = [(ROW_0 + i * ROW_H, line) for i, line in enumerate(build_info_lines())]
    height = max(y for y, _ in art + info) + ROW_H

    def column(x, rows):
        return '\n'.join(
            line % y if '%d' in line else
            '<tspan x="%d" y="%d">%s</tspan>' % (x, y, line)
            for y, line in rows)

    swatches = '\n'.join('.sw%d {fill: %s;}' % (i, c)
                         for i, c in enumerate(theme['swatch']))
    return '''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{w}px" height="{h}px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {key};}}
.value {{fill: {value};}}
.addColor {{fill: {add};}}
.delColor {{fill: {del_};}}
.cc {{fill: {cc};}}
.dim {{fill: {dim};}}
{swatches}
text, tspan {{white-space: pre;}}
</style>
<rect width="{w}px" height="{h}px" fill="{bg}" rx="15"/>
<text x="{ax}" y="{y0}" fill="{fg}" class="ascii">
{art}
</text>
<text x="{ix}" y="{y0}" fill="{fg}">
{info}
</text>
</svg>'''.format(w=WIDTH, h=height, ax=ART_X, ix=INFO_X, y0=ROW_0,
                 art=column(ART_X, art), info=column(INFO_X, info),
                 swatches=swatches, del_=theme['del'], **{
                     k: theme[k] for k in ('bg', 'fg', 'key', 'value', 'add', 'cc', 'dim')})


if __name__ == '__main__':
    for filename, theme in THEMES.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(render(theme))
        print('wrote', filename)
