"""Local branding module for CodeRefinery Sphinx projects
"""
from dateutil.parser import parse
from dateutil import tz
from docutils import nodes
from sphinx.util.docutils import SphinxRole

__version__ = '0.1.0'

class LocalTimezoneNode(nodes.Element):
    pass

def visit_lt_html(self, node):
    #self.body.append(self.starttag(node, 'math'))
    print('x'*50)
    self.body.append('TZ')
    self.body.append(node.text)
def depart_lt_html(self, node):
    self.body.append('/TZ>')



class LocalTimezoneRole(SphinxRole):
    """A role to say hello!"""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        #node = nodes.inline(text=f'Hello {self.text}!')
        node = LocalTimezoneNode(text=f'Hello {self.text}!')
        return [node], []

def ltz_role(name, rawtext, text, lineno, inliner,
             options=None, content=None):
    print(rawtext)
    print(text)
    dt = parse(text)
    dt_utc = dt.astimezone(tz.UTC)
    js = f"""\
  <script>
    var ts = dayjs("{ dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ") }").utc();
    document.write(ts.local().format('HH:mm'));
  </script>
"""
    print(js)

    html_node = nodes.raw('', js, format='html')

    # Return nodes, error_messages
    return [html_node], []


def setup(app):

    app.add_node(LocalTimezoneNode, html=(visit_lt_html, depart_lt_html))
    #app.add_role('local-timezone', LocalTimezoneRole())
    app.add_role('local-timezone', ltz_role)
    app.add_js_file("https://cdn.jsdelivr.net/npm/dayjs@1.11.7/dayjs.min.js",
#                    integrity="sha256-EfJOqCcshFS/2TxhArURu3Wn8b/XDA4fbPWKSwZ+1B8=",
                    crossorigin="anonymous")
    app.add_js_file("https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/utc.js",
#                    integrity="sha256-qDfIIxqpRhYWa543p6AHZ323xT3B8O6iLZFUAWtEQJw=",
                    crossorigin="anonymous")

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
