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

class LocalTimeNode(nodes.abbreviation):
    classes = ['localtime']

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
    abbrev = LocalTimeNode(rawtext, "", classes=['localtime'], **abbrev_options)
    abbrev.children.append(html_node)

    # Return nodes, error_messages
    return [abbrev], []



def remove_scripts_if_not_needed(app, pagename, templatename, context, doctree):
    """Remove the scripts from the page if they aren't needed.

    From https://github.com/sphinx-doc/sphinx/issues/6241#issuecomment-705070598
    """
    if not doctree:
        return

    if not doctree.traverse(LocalTimeNode):
        # Remove thebe JS files
        new_script_files = []
        for ii in context["script_files"]:
            if ii.filename in JAVASCRIPT_FILES:
                continue
            if ii.attributes.get('body', '') in JS_BODY:
                continue
            new_script_files.append(ii)
        context["script_files"] = new_script_files


JAVASCRIPT_FILES = {
    "https://cdn.jsdelivr.net/npm/dayjs@1.11.7/dayjs.min.js": "sha256-EfJOqCcshFS/2TxhArURu3Wn8b/XDA4fbPWKSwZ+1B8=",
    "https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/utc.js": "sha256-qDfIIxqpRhYWa543p6AHZ323xT3B8O6iLZFUAWtEQJw=",
    "https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/advancedFormat.js": "sha256-b5ymCcSvYPKgMDPnLexXFPT457JAOBk0BA9UegKCRj8=",
    "https://cdn.jsdelivr.net/npm/dayjs@1.11.7/plugin/timezone.js": "sha256-BM6DY5CUw78IJCgJ5v246oz4tD7ON4r7gmV3AzuzvBY=",
    }
JS_BODY = {
    "dayjs.extend(window.dayjs_plugin_utc)",
    "dayjs.extend(window.dayjs_plugin_advancedFormat)",
    "dayjs.extend(window.dayjs_plugin_timezone)",
    }


def setup(app):

    #app.add_node(LocalTimezoneNode, html=(visit_lt_html, depart_lt_html))
    app.add_role('localtime', ltz_role)
    for jsfile, integrity in JAVASCRIPT_FILES.items():
        app.add_js_file(jsfile, integrity=integrity, crossorigin="anonymous")
    for jsbody in JS_BODY:
        app.add_js_file(None, body=jsbody)
    # Remove unneeded scripts files
    app.connect('html-page-context', remove_scripts_if_not_needed)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
