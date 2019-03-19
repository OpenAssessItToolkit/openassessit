from __future__ import print_function
import argparse
import jinja2
import os
import io
import sys
import logging
import markdown2
from .utils import initialize_logger, readable_dir
from .templates import template_path

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def get_args():
    example_text = '''
    examples:

    python openassessit/to_html -i /tmp/assessment.md -o /tmp/assessment.html

    python openassessit/to_html -i /tmp/assessment.md -o /tmp/assessment.html -t /your/templates

    '''

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='Provide a the path to an input file', default=sys.stdin)
    parser.add_argument('-o', '--output-file', help='Provide a path to where to save the html ')
    parser.add_argument('-t', '--user-template-path',
                        action=readable_dir,
                        help='Provide filepath to custom user templates')
    return parser.parse_args()


def read_input(input_file):
    """ Read OpenAssessIt .md file  """
    if input_file:
        if type(input_file) is str:
            with io.open(input_file, encoding='utf-8') as stream:
                return stream.read()


def write_output(output_file, rendered, force_stdout=False):
    """ Write HTML output file """
    if output_file:
        with io.open(output_file, 'w', encoding='utf-8') as stream:
            stream.write(rendered)

    if force_stdout:
        print(rendered)


def main():
    """ Convert to Markdown to HTML """
    args = get_args()
    input_file = args.input_file
    output_file = args.output_file
    paths = list()
    if args.user_template_path:
        user_template_path = args.user_template_path
        paths.append(user_template_path)
    else:
        paths.append(template_path)
    loader = jinja2.FileSystemLoader(paths)
    env = jinja2.Environment(loader=loader)
    header = loader.load(env, 'to_html_header.html')
    footer = loader.load(env, 'to_html_footer.html')

    md = read_input(input_file)
    html = markdown2.markdown(md, extras={"fenced-code-blocks": None, "toc": {"depth": 2}})
    toc_html = html.toc_html
    TOC_MARKER = '<!--TOC-->'
    html = html.replace(TOC_MARKER, toc_html)
    output = "".join([header.render(), html, footer.render()])
    output_dir = os.path.dirname(input_file)
    initialize_logger('html', output_dir)
    write_output(output_file, output)

    logging.info('HTML conversion complete in: ' + output_file)


if __name__ == '__main__':
    main()
