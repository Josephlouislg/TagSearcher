import logging.handlers

from aiohttp import web, WSMsgType

from tag_searcher.tag_tree import TagTreeService

log = logging.getLogger(__name__)


async def request_handler(request):
    data = await request.json()
    tag_tree_service: TagTreeService = request.app['tag_tree_service']

    return web.json_response(
        status=200,
        data={
            "tags": tag_tree_service.get_tags_by_text(data['text'])
        }
    )
