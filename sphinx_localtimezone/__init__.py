"""Local branding module for CodeRefinery Sphinx projects
"""
import collections

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


# pylint: disable=unused-argument
def ltz_role(name, rawtext, text, lineno, inliner,
             options=None, content=None):
    """Docutils role to insert local timezones"""
    # I don't know if there is a better way to automatically detect any
    # timezone string.
    tzinfos = collections.defaultdict(tz.gettz)
    dt = parse(text, tzinfos=tzinfos)
    dt_utc = dt.astimezone(tz.UTC)
    # There must be a better way than embedding this everywhere.  Also this
    # only works for HTML which isn't very Sphinx-like.  It should become a
    # node and then the node inserts whatever is appropriate for the builder.
    js = f"""\
  <script>
    dayjs.extend(window.dayjs_plugin_utc);
    var ts = dayjs("{ dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ") }").utc();
    document.write(ts.local().format('HH:mm'));
  </script>
"""
    html_node = nodes.raw('', js, format='html')

    abbrev_options = {'explanation': f'This is your detected local time converted from {text}'}
    abbrev = nodes.abbreviation(rawtext, "", **abbrev_options)
    abbrev.children.append(html_node)

    # Return nodes, error_messages
    return [abbrev], []


def setup(app):

    app.add_node(LocalTimezoneNode, html=(visit_lt_html, depart_lt_html))
    app.add_role('local-timezone', ltz_role)
    app.add_js_file("https://cdn.jsdelivr.net/npm/dayjs@1.11.7/dayjs.min.js",
                    integrity="sha256-EfJOqCcshFS/2TxhArURu3Wn8b/XDA4fbPWKSwZ+1B8=",
                    crossorigin="anonymous")
    app.add_js_file("https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/utc.js",
                    integrity="sha256-qDfIIxqpRhYWa543p6AHZ323xT3B8O6iLZFUAWtEQJw=",
                    crossorigin="anonymous")
    app.add_js_file(None, body='dayjs.extend(window.dayjs_plugin_utc)')
    # TODO: Use this to remove scripts from pages that don't need it:
    # https://github.com/sphinx-doc/sphinx/issues/6241#issuecomment-705070598


    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
