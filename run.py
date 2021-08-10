import os

from winterhut import create_app
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', type=str, required=True,
                        help="JSON config file to use for the app configuration.")
    args = parser.parse_args()
    if args.config:
        config = args.config
        if os.path.exists(config) and os.path.isfile(config):
            app = create_app(config=config)
            app.run()
        else:
            raise ValueError('Provided configuration file is invalid')
