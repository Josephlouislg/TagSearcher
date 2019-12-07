import logging


log = logging.getLogger(__name__)


class TagTreeService(object):
    def __init__(self, tags):
        self.tags_tree = {}
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
        tags = []
        max_text_words_beetwen_tag_words = 2
        text_words = [word.strip() for word in text.split(' ') if word.strip()]
        for index, word in enumerate(text_words, start=0):
            word_tags = []
            current_text_word = word
            current_word_index = index
            current_subtree = self.tags_tree

            while current_subtree and current_text_word:
                tag = current_subtree.get(current_text_word, None)
                if not tag:
                    break

                word_tags.append(current_text_word)
                if tag['is_leaf']:
                    tags.append(' '.join(word_tags))
                current_subtree = tag['childs']
                current_text_word = None

                possible_next_tags_words = (
                    text_words[current_word_index + i]
                    for i in range(1, max_text_words_beetwen_tag_words + 1)
                    if len(text_words) >= i + current_word_index + 1
                )
                for possible_tag_index, tag_word in enumerate(possible_next_tags_words):
                    tag = current_subtree.get(tag_word, None)
                    if tag:
                        word_tags.append(tag_word)
                        if tag['is_leaf']:
                            tags.append(' '.join(word_tags))
                        current_text_word = tag_word
                        current_word_index = current_word_index + possible_tag_index + 1
                        current_subtree = tag['childs']
                        break
        return tags

