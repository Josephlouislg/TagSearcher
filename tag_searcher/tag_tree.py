import csv
import logging


log = logging.getLogger(__name__)


class TagTreeService(object):
    def __init__(self, tag_file_path):
        self.tags_tree = {}
        with open(tag_file_path) as file:
            csv_reader = csv.reader(file, delimiter='\n')
            tags = (title[0] for title in csv_reader)
            self._load_tree(tags)

    def _load_tree(self, tags):
        for tag in tags:
            words = tag.strip().split(' ')
            words = tuple(word for word in words if word.strip())
            current_subtree = self.tags_tree
            for level, tag_word in enumerate(words, start=1):
                current_tag_subtree = current_subtree.get(tag_word, None)
                if current_tag_subtree:
                    current_tag_subtree['is_leaf'] = current_tag_subtree['is_leaf'] or len(words) == level
                else:
                    current_subtree[tag_word] = {'childs': {}, "is_leaf": len(words) == level}
                current_subtree = current_subtree[tag_word]['childs']

    def get_tags_by_text(self, text: str)-> list:
        return [self.tags_tree['toyota']]
