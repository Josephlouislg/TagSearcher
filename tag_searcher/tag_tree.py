import re
import logging


log = logging.getLogger(__name__)


MAX_TEXT_WORDS_BEETWEN_TAGS = 2


class TagTreeService(object):
    def __init__(self, tags):
        self.spec_chars_regex = '[\t|\n|\r|,|.]'
        self.tags_tree = {}
        print("Building tags tree...")
        self._load_tree(tags)

    def _load_tree(self, tags):
        for tag in tags:
            words = re.sub(self.spec_chars_regex, ' ', tag).strip().split(' ')
            words = tuple(
                word.strip().lower()
                for word in words if word.strip()
            )
            current_subtree = self.tags_tree
            for level, tag_word in enumerate(words, start=1):
                current_tag_subtree = current_subtree.get(tag_word, None)
                if current_tag_subtree:
                    current_tag_subtree['is_leaf'] = current_tag_subtree['is_leaf'] or len(words) == level
                else:
                    current_subtree[tag_word] = {'childs': {}, "is_leaf": len(words) == level}
                current_subtree = current_subtree[tag_word]['childs']

    def get_tags_by_text(self, text: str)-> list:
        tags = set()
        text = re.sub(self.spec_chars_regex, ' ', text)
        text_words = [word.strip() for word in text.split(' ') if word.strip()]
        for index, word in enumerate(text_words):
            word_tags = []
            current_text_word = word
            current_word_index = index
            current_subtree = self.tags_tree

            while current_subtree and current_text_word:
                tag = current_subtree.get(current_text_word.lower(), None)
                if not tag:
                    break
                word_tags.append(current_text_word)
                if tag['is_leaf']:
                    tags.add(' '.join(word_tags))
                current_subtree = tag['childs']
                current_text_word = None

                for i in range(1, MAX_TEXT_WORDS_BEETWEN_TAGS + 2):
                    current_text_word = len(text_words) >= i + current_word_index + 1 and text_words[current_word_index + i]
                    tag = current_subtree.get(current_text_word.lower(), None) if current_text_word else None
                    if tag:
                        word_tags.append(current_text_word)
                        if tag['is_leaf']:
                            tags.add(' '.join(word_tags))
                        current_word_index = current_word_index + i + 1
                        current_text_word = len(text_words) >= current_word_index + 1 and text_words[current_word_index]
                        current_subtree = tag['childs']
                        break
        return list(tags)
