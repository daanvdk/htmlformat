import htmlformat


INPUT = (
    '<!doctype html>\n'
    '    <html>\n'
    '  <head>\n'
    '       <title>Hello, World!</title>\n'
    '  <link rel="stylesheet" href="main.css" />\n'
    '    </head>\n'
    '  <body>\n'
    '    <h1>Hello, World!</h1>\n'
    '   <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>\n'
    '    <p>Pellentesque eros purus, vehicula a urna nec, efficitur posuere '
    'lacus.</body>\n'
)
NODES = (
    ('declaration', (1, 1), 'doctype html'),
    ('tag', (2, 5), 'html', (), (
        ('tag', (3, 3), 'head', (), (
            ('tag', (4, 8), 'title', (), (
                ('text', (4, 15), 'Hello, World!'),
            )),
            ('tag', (5, 3), 'link', (
                ('rel', 'stylesheet'),
                ('href', 'main.css'),
            ), ()),
        )),
        ('tag', (7, 3), 'body', (), (
            ('tag', (8, 5), 'h1', (), (
                ('text', (8, 9), 'Hello, World!'),
            )),
            ('tag', (9, 4), 'p', (), (
                ('text', (9, 7), (
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                )),
            )),
            ('tag', (10, 5), 'p', (), (
                ('text', (10, 8), (
                    'Pellentesque eros purus, vehicula a urna nec, efficitur '
                    'posuere lacus.'
                )),
            )),
        )),
    )),
)
OUTPUT = (
    '<!doctype html>\n'
    '<html>\n'
    '  <head>\n'
    '    <title>Hello, World!</title>\n'
    '    <link rel="stylesheet" href="main.css" />\n'
    '  </head>\n'
    '  <body>\n'
    '    <h1>Hello, World!</h1>\n'
    '    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>\n'
    '    <p>Pellentesque eros purus, vehicula a urna nec, efficitur posuere '
    'lacus.</p>\n'
    '  </body>\n'
    '</html>\n'
)


def test_parse():
    assert htmlformat.parse(INPUT) == NODES


def test_render():
    assert htmlformat.render(NODES) == OUTPUT


def test_format():
    assert htmlformat.format(INPUT) == OUTPUT
