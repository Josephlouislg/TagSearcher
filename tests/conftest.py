from aiohttp import web


from tag_searcher.app import request_handler
from tag_searcher.tag_tree import TagTreeService


pytest_plugins = [
    'aiohttp.pytest_plugin'
]


def create_app(loop):
    app = web.Application(loop=loop)
    app.router.add_route('POST', '/text', request_handler)
    app['tag_tree_service'] = TagTreeService(
        tags=[
            'test1',
            'test2',
            'test3',
            'test1 test2 test 3'
        ]
    )
    return app
