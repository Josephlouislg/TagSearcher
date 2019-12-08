import pytest

from tag_searcher.tag_tree import TagTreeService


@pytest.fixture
def tags_tree_service():
    return TagTreeService(
        tags=[
            'tag1',
            'tag1 tag2',
            'tag2 tag3',
            'tag2 tag3 tag4',
            'tag5 tag6'
        ]
    )


def test_tags_tree_build():
    tags_tree_service = TagTreeService(
        tags=[
            'tag1',
            'tag1 tag2',
            'tag2 tag3',
            'tag2 tag4',
            'tag2 tag3 tag4',
            'tag5 tag6'
        ]
    )
    assert tags_tree_service.tags_tree == {
        'tag1': {
            'is_leaf': True,
            'childs': {'tag2': {'is_leaf': True, 'childs': {}}}
        },
        'tag2': {
             'is_leaf': False,
             'childs': {
                 'tag3': {
                      'is_leaf': True,
                      'childs': {
                          'tag4': {
                              'is_leaf': True,
                              'childs': {}
                          }
                      }
                 },
                 'tag4': {
                     'is_leaf': True,
                     'childs': {}
                 }
             }
        },
        'tag5': {
             'is_leaf': False,
             'childs': {
                 'tag6': {
                     'is_leaf': True,
                     'childs': {}
                 }
             }
        }
    }


def test_tag_search(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='test test tag1 tag2 test test'
    )
    assert set(tags) == {'tag1', 'tag1 tag2'}


def test_tag_search_with_one_word_beetween_tags(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='test tag1 test tag2'
    )
    assert set(tags) == {'tag1', 'tag1 tag2'}


def test_tag_search_with_two_word_beetween_tags(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='test tag1 test test tag2'
    )
    assert set(tags) == {'tag1', 'tag1 tag2'}


def test_finding_multiple_tags_with(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='tag2 tag3 tag4'
    )
    assert set(tags) == {'tag2 tag3 tag4', 'tag2 tag3'}


def test_no_tags_text_search(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='test test test test'
    )
    assert set(tags) == set()


def test_all_tags_search(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='tag1 tag2 tag3 tag4 tag2'
    )
    assert set(tags) == {
        'tag1',
        'tag1 tag2',
        'tag2 tag3',
        'tag2 tag3 tag4'
    }


def test_nested_tags_search(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='tag1 tag5 tag6 tag2'
    )
    assert set(tags) == {
        'tag1',
        'tag1 tag2',
        'tag5 tag6'
    }


def test_upper_case(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='Tag1 tAg5 taG6 TAG2'
    )
    assert set(tags) == {
        'Tag1',
        'Tag1 TAG2',
        'tAg5 taG6'
    }


def test_special_chars_removing(tags_tree_service: TagTreeService):
    tags = tags_tree_service.get_tags_by_text(
        text='tag1 \n tag5, tag6. \r\t\n tag2'
    )
    assert set(tags) == {
        'tag1',
        'tag1 tag2',
        'tag5 tag6'
    }


def test_special_chars_removing_from_tag_tree():
    tags_tree_service = TagTreeService(
        tags=[
            'tAg1',
            'tAg1,\n\r\ttag2',
            'tag2.\ntag3',
        ]
    )
    text = 'tag1 tag2 tag3'
    assert set(tags_tree_service.get_tags_by_text(text=text)) == {
        'tag1',
        'tag1 tag2',
        'tag2 tag3'
    }
