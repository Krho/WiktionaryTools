import json

import functions
import logger


LOG = logger.logger()


def main():
    from argparse import ArgumentParser
    description = 'Tools for the wiktionary.'
    parser = ArgumentParser(description=description)
    parser.add_argument('-t', '--thesaurus',
                        type=str,
                        dest='thesaurus',
                        required=False,
                        default=u'femme',
                        help='thesaurus to work on')
    args = parser.parse_args()
    thesaurus = args.thesaurus.lower()
    functions.harvest(thesaurus)
    result = functions.analyse(thesaurus)
    LOG.info("Results:\n%s", json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
