import argparse
import csv

import logging.handlers

import asyncio
import uvloop
from aiohttp import web

from tag_searcher.app import request_handler
from tag_searcher.tag_tree import TagTreeService

log = logging.getLogger(__name__)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=2000)
    ap.add_argument("--host", default='0.0.0.0')
    ap.add_argument("--tag_file_path", default='tags.csv')
    return ap.parse_args()


async def create_app(args):
    app = web.Application()
    with open(args.tag_file_path) as file:
        csv_reader = csv.reader(file, delimiter='\n')
        tags = (title[0] for title in csv_reader)
        app['tag_tree_service'] = TagTreeService(tags=tags)
    app.router.add_route(
        'POST', '/text', request_handler
    )
    return app


def main():
    args = parse_args()
    host = args.host
    port = args.port
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    log.info(f"Listening {host}:{port}")
    web.run_app(create_app(args), host=host, port=port)


if __name__ == '__main__':
    main()
