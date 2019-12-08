# TagSearcher

### Start service:

`docker-compose up tag_searcher`

### Usage:

`curl -XPOST http://127.0.0.1:2000/text --header "Content-Type: application/json" -d '{"text": "test text"}'`


### Tests:

`docker-compose run pytest`