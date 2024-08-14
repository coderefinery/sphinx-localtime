"""Local branding module for CodeRefinery Sphinx projects
"""
import collections
import re

from dateutil.parser import parse
from dateutil import tz
from docutils import nodes
from sphinx.util.docutils import SphinxRole

__version__ = '0.1.0'

# Formats using https://day.js.org/docs/en/display/format
TIME_FORMAT = "HH:mm"
FORMAT_RE = re.compile(r'(.*)\((.*)\)')

class LocalTimezoneNode(nodes.abbreviation):
    classes = ['local-timezone']

#def visit_lt_html(self, node):
#    #self.body.append(self.starttag(node, 'math'))
#    #print('x'*50)
#    self.body.append('TZ')
#    #self.body.append(node.text)
#def depart_lt_html(self, node):
#    self.body.append('/TZ>')


# pylint: disable=unused-argument
def ltz_role(name, rawtext, text, lineno, inliner,
             options=None, content=None):
    """Docutils role to insert local timezones"""
    # I don't know if there is a better way to automatically detect any
    # timezone string.

    time_format = TIME_FORMAT
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    m = FORMAT_RE.match(text)
    if m:
        text, time_format = m.group(1), m.group(2)

    tzinfos = collections.defaultdict(tz.gettz)
    try:
        dt = parse(text, tzinfos=tzinfos)
    except ValueError:
        msg = inliner.reporter.error(
                f"Could not parse date {text}, lineno={lineno}"
            )
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb, msg]
    dt_utc = dt.astimezone(tz.UTC)
    # There must be a better way than embedding this everywhere.  Also this
    # only works for HTML which isn't very Sphinx-like.  It should become a
    # node and then the node inserts whatever is appropriate for the builder.
    js = f"""\
  <script>
    dayjs.extend(window.dayjs_plugin_utc);
    var ts = dayjs("{ dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ") }").utc();
    document.write(ts.local().format('{time_format}'));
  </script>
"""
    html_node = nodes.raw("", js, format='html')

    abbrev_options = {'explanation': f'This is your detected local time converted from {text.strip()}'}
    abbrev = LocalTimezoneNode(rawtext, "", classes=['local-timezone'], **abbrev_options)
    abbrev.children.append(html_node)

    # Return nodes, error_messages
    return [abbrev], []



def remove_scripts_if_not_needed(app, pagename, templatename, context, doctree):
    """Remove the scripts from the page if they aren't needed.

    From https://github.com/sphinx-doc/sphinx/issues/6241#issuecomment-705070598
    """
    if not doctree:
        return

    if not doctree.traverse(LocalTimezoneNode):
        # Remove thebe JS files
        new_script_files = []
        for ii in context["script_files"]:
            if ii.filename in [
                "https://cdn.jsdelivr.net/npm/dayjs@1.11.7/dayjs.min.js",
                "https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/utc.js"]:
                continue
            if ii.attributes.get('body', '') == 'dayjs.extend(window.dayjs_plugin_utc)':
                continue
            new_script_files.append(ii)
        context["script_files"] = new_script_files


def setup(app):

    #app.add_node(LocalTimezoneNode, html=(visit_lt_html, depart_lt_html))
    app.add_role('local-timezone', ltz_role)
    app.add_js_file("https://cdn.jsdelivr.net/npm/dayjs@1.11.7/dayjs.min.js",
                    integrity="sha256-EfJOqCcshFS/2TxhArURu3Wn8b/XDA4fbPWKSwZ+1B8=",
                    crossorigin="anonymous")
    app.add_js_file("https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/utc.js",
                    integrity="sha256-qDfIIxqpRhYWa543p6AHZ323xT3B8O6iLZFUAWtEQJw=",
                    crossorigin="anonymous")
    app.add_js_file(None, body='dayjs.extend(window.dayjs_plugin_utc)')
    # Remove unneeded scripts files
    app.connect('html-page-context', remove_scripts_if_not_needed)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
