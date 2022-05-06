from __future__ import print_function
import argparse
import jinja2
import markupsafe
import os
import io
from operator import itemgetter
import json
import sys
import re
import logging
from .utils import generate_img_filename, initialize_logger, readable_dir
from .templates import template_path


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def get_args():
    example_text = '''
    examples:

    python  -m openassessit.markdown -i /tmp/lighthouse-report.json -o /tmp/lighthouse-report.md

    python  -m openassessit.markdown -i /tmp/lighthouse-report.json -o /tmp/lighthouse-report.md -t /your/templates

    lighthouse  https://cats.com --output=json | python  -m openassessit.markdown -o lighthouse-report.md

    '''

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='Provide a the path to an input file', default=sys.stdin)
    parser.add_argument('-o', '--output-file', help='Provide a filepath where the markdown result gets written')
    parser.add_argument('-t', '--user-template-path',
                        action=readable_dir,
                        help='Provide filepath to custom user templates')
    parser.add_argument('-e', action='store_true', default=False,
                        help='Echo the output to stdout, even when using the -o option')
    return parser.parse_args()


def preprocess_data(data):
    """ Parse Lighthouse JSON data """
    # Get audit_refs with weights in a nice dict before full pre-processing
    metadata = {}

    for cat in data['categories']:
        for audit_ref in data['categories'][cat]['auditRefs']:
            if 'id' in audit_ref:
                metadata[audit_ref['id']] = {
                    'weight': audit_ref['weight']
                }

    for cat in data['categories']:
        data['categories'][cat]['audits'] = dict()
        for audit_ref in data['categories'][cat]['auditRefs']:
            audit = data['audits'][audit_ref['id']]
            audit['audit_template'] = '%s.md' % audit_ref['id']
            if 'displayValue' in audit and type(audit['displayValue']) is list:
                try:
                    audit['displayValue'] = audit['displayValue'][0] % tuple(audit['displayValue'][1:])
                except TypeError as ex:
                    logging.error('Exception "%s" audit skipped because: %s' % (audit_ref['id'], ex))
            elif 'errorMessage' in audit:
                logging.error('Lighthouse json input-file not valid. ErrorMessage in "%s" check URL and Lighthouse config then re-run.' % (audit_ref['id']))
            data['categories'][cat]['audits'][audit_ref['id']] = audit

            # Add the weight right in to the audit bit, so we can easily sort
            # later
            data['categories'][cat]['audits'][audit_ref['id']]['weight'] = \
                metadata[audit_ref['id']]['weight']

    # Now that the weights are in a spot we can get, let's add a sorted list,
    # and maybe (?) in a future feature, disabled the unsorted dict
    for cat in data['categories']:
        unsorted_audits = []
        for audit_ref in data['categories'][cat]['auditRefs']:
            unsorted_audits.append(
                data['categories'][cat]['audits'][audit_ref['id']])

        # Now that it's in a nice list, let's sort it.  Reverse means highest
        # number first
        sorted_audits = sorted(unsorted_audits, key=itemgetter('weight'),
                               reverse=True)

        data['categories'][cat]['sorted_audits'] = sorted_audits

    return data


def read_input(input_file):
    """ Read Lighthouse JSON file  """
    if type(input_file) is str:
        with io.open(input_file, encoding='utf-8') as stream:
            return json.JSONDecoder().decode(stream.read())
    else:
        return json.JSONDecoder().decode(input_file.read())


def write_output(output_file, rendered, force_stdout=False):
    """ Write Markdown file """
    if output_file:
        with io.open(output_file, 'w', encoding='utf-8') as stream:
            stream.write(rendered)

    if force_stdout:
        print(rendered)


def main():
    """ Parse Lighthouse JSON and convert to Markdown """
    args = get_args()
    input_file = args.input_file
    output_file = args.output_file
    output_dir = os.path.dirname(args.input_file)
    paths = list()
    if args.user_template_path:
        user_template_path = args.user_template_path
        paths.append(user_template_path)
    else:
        paths.append(template_path)
    loader = jinja2.FileSystemLoader(paths)

    env = jinja2.Environment(loader=loader)

    template = loader.load(env, 'index.md')

    rendered = template.render({
        'data': preprocess_data(read_input(input_file)),
        'generate_img_filename': generate_img_filename,
    })

    write_output(output_file, rendered, force_stdout=args.e or not output_file)
    initialize_logger('markdown', output_dir)
    logging.info('Markdown convertion complete in: "%s"' % (output_file))


if __name__ == '__main__':
    main()
