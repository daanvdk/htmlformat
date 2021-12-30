import html

from .constants import SELF_CLOSING_TAGS


def render(nodes):
    return ''.join(render_nodes(nodes, '', False))


def render_nodes(nodes, indent, inline):
    for i, node in enumerate(nodes):
        node_type, (line, column), *data = node

        if not inline and (i == 0 or nodes[i - 1][1][0] != line):
            yield indent

        if node_type == 'text':
            content, = data
            yield html.escape(content, False)

        elif node_type == 'tag':
            tag, attrs, children = data

            yield f'<{tag}'

            for key, value in attrs:
                if value is None:
                    yield f' {key}'
                else:
                    yield f' {key}="{html.escape(value)}"'

            if tag not in SELF_CLOSING_TAGS or children:
                node_inline = inline or is_inline(node)
                yield '>'
                if not node_inline:
                    yield '\n'
                yield from render_nodes(children, indent + '  ', node_inline)
                if not node_inline:
                    yield indent
                yield f'</{tag}>'
            else:
                yield ' />'

        elif node[0] == 'declaration':
            content, = data
            yield f'<!{content}>'

        elif node[0] == 'comment':
            content, = data
            yield f'<!--{content}-->'

        else:
            raise ValueError(f'unknown node: {node_type}')

        if not inline and (i == len(nodes) - 1 or nodes[i + 1][1][0] != line):
            yield '\n'


def is_inline(node):
    node_type, (line, column), *data = node

    if node_type == 'text':
        return True

    elif node_type == 'tag':
        _, _, children = data
        return all(
            child[1][0] == line and is_inline(child)
            for child in children
        )

    elif node_type == 'declaration':
        return False

    elif node_type == 'comment':
        return True

    else:
        raise ValueError(f'unknown node: {node[0]}')
