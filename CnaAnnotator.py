#!/usr/bin/python

import argparse
from AnnotatorCore import *
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('CnaAnnotator')


def main(argv):
    if argv.help:
        log.info('\n'
        'CnaAnnotator.py -i <input CNA file> -o <output CNA file> [-p previous results] [-c <input clinical file>] [-s sample list filter] [-t <default tumor type>] [-u oncokb-base-url] [-b oncokb_api_bear_token]\n'
        '  Input CNA file should follow the GISTIC output (https://cbioportal.readthedocs.io/en/latest/File-Formats.html#discrete-copy-number-data)\n'
        '  Essential clinical columns:\n'
        '    SAMPLE_ID: sample ID\n'
        '  Cancer type will be assigned based on the following priority:\n'
        '     1) ONCOTREE_CODE in clinical data file\n'
        '     2) ONCOTREE_CODE exist in MAF\n'
        '     3) default tumor type (-t)\n'
        '  Default OncoKB base url is http://oncokb.org')
        sys.exit()
    if argv.input_file == '' or argv.output_file == '' or argv.oncokb_api_bearer_token == '':
        log.info('for help: python CnaAnnotator.py -h')
        sys.exit(2)
    if argv.sample_ids_filter:
        setsampleidsfileterfile(argv.sample_ids_filter)
    if argv.oncokb_api_url:
        setoncokbbaseurl(argv.oncokb_api_url)
    setoncokbapitoken(argv.oncokb_api_bearer_token)

    cancertypemap = {}
    if argv.input_clinical_file:
        readCancerTypes(argv.input_clinical_file, cancertypemap)

    log.info('annotating %s ...' % argv.input_file)
    processcnagisticdata(argv.input_file, argv.output_file, argv.previous_result_file, argv.default_cancer_type,
                         cancertypemap, False)

    log.info('done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', dest='help', action="store_true", default=False)
    parser.add_argument('-i', dest='input_file', default='', type=str)
    parser.add_argument('-o', dest='output_file', default='', type=str)
    parser.add_argument('-p', dest='previous_result_file', default='', type=str)
    parser.add_argument('-c', dest='input_clinical_file', default='', type=str)
    parser.add_argument('-s', dest='sample_ids_filter', default='', type=str)
    parser.add_argument('-t', dest='default_cancer_type', default='cancer', type=str)
    parser.add_argument('-u', dest='oncokb_api_url', default='', type=str)
    parser.add_argument('-b', dest='oncokb_api_bearer_token', default='', type=str)
    parser.set_defaults(func=main)

    args = parser.parse_args()
    args.func(args)
