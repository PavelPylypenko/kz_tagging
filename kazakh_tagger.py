from rules import SUB_ONE_SUF, SUB_PLURAL_SUFFS, SUB_SUFFIXES, OBJ_SUFFIXES, \
    OBJ_ENDS, PRED_A_ENDS, \
    PRED_A_STARTS, PRED_A_SUFFIXES, PRED_B_SUFFIXES, PRED_B_SUFFIX_ENDS, \
    PRED_C_SUFFIXES, PRED_C_POSS_SUFFIXES, PRED_C_ADD, PRED_D_SUFFIXES, \
    PRED_D_POSS_SUFFIXES, PRED_D_ADD, PRED_SUFFIXES


class KazakhTagger:
    tagged_list_of_words = []
    sentences = []

    def clear_word(self, word):
        """Remove first and last symbols if it's not a character"""
        if not word[0].isalpha():
            word = word[1:]
        if not word[-1].isalpha():
            word = word[:-1]
        return word

    def write_results(self):
        with open('output.txt', 'w') as file:
            for word in self.tagged_list_of_words:
                file.write(f'{word[0]}: {word[1]} \n')

    def tag(self, text: list):
        for idx, sentence in enumerate(text):
            self.sentences.append(sentence)
            sentence = sentence.split()
            if not sentence:
                continue
            sentence = [self.clear_word(word) for word in sentence]
            sub_word = self.is_tagged_sub(sentence)
            if sub_word:
                self.tagged_list_of_words.append([sub_word, 'SUB', idx])
            obj_word = self.is_tagged_obj(sentence)
            if obj_word:
                self.tagged_list_of_words.append([obj_word, 'OBJ', idx])
            pred_word = self.is_tagged_pred(sentence)
            if pred_word:
                self.tagged_list_of_words.append([pred_word, 'PRED', idx])
        self.write_results()

    def get_suffix(self, word: str, suffixes: list):
        for suffix in suffixes:
            index = word.find(suffix)
            if index != -1:
                return suffix

    def get_suffixes(self, word: str, suffixes: list):
        output = []
        for suffix in suffixes:
            index = word.find(suffix)
            if index != -1:
                output.append(suffix)
        return output

    def is_sub(self, sentence, size):
        word = None
        if len(sentence) > size:
            word = sentence[size]
            suffix = self.get_suffix(word, SUB_ONE_SUF)
            if not suffix and size < 4:
                word = self.is_sub(sentence, size + 1)
            if suffix:
                word_without_suffix = word[:word.index(suffix)]
                is_plural = self.is_plural(word_without_suffix)
                if not is_plural:
                    return word
                if size < 4:
                    word = self.is_sub(sentence, size + 1)
        return word

    def is_sub2(self, sentence):
        for word in sentence:
            for suff in SUB_SUFFIXES:
                index = word.find(suff)
                if index != -1:
                    return word, suff
        return None, None

    def is_plural(self, word: str):
        for plural_suff in SUB_PLURAL_SUFFS:
            if plural_suff in word:
                idx = word.rfind(plural_suff)
                size = len(plural_suff)
                if idx + size == len(word):
                    return True
        return False

    def is_tagged_sub(self, sentence):
        word = self.is_sub(sentence, 0)
        if word:
            return word
        word, suffix = self.is_sub2(sentence)
        if suffix:
            word_after_suffix = word[word.index(suffix):]
            suffix = self.get_suffix(word_after_suffix, SUB_ONE_SUF)
            if not suffix:
                return word

    def is_tagged_obj(self, sentence):
        for word in sentence:
            suffixes = self.get_suffixes(word, OBJ_SUFFIXES)
            for suffix in suffixes:
                if suffix:
                    last_chars = word.rindex(suffix) + len(suffix)

                    if last_chars == len(word) or \
                            word[:last_chars] in OBJ_ENDS:
                        return word

    def is_pred_a(self, sentence, last_word):
        for end in PRED_A_ENDS:
            if last_word.find(end) != -1 and \
                    last_word.find(end) + len(end) == len(last_word):
                break
        else:
            return
        for word in sentence:  # type: str
            for start in PRED_A_STARTS:
                if word.startswith(start):
                    for suff in PRED_A_SUFFIXES:
                        if word[len(start):].find(suff) == 0:
                            return word

    def is_pred_b(self, sentence, last_word):
        for suffix in PRED_B_SUFFIXES:
            if last_word.find(suffix) != -1:
                word = last_word[last_word.rindex(suffix) + len(suffix):]
                for start in PRED_B_SUFFIX_ENDS:
                    if word.startswith(start):
                        return last_word

    def is_pred_c(self, sentence, last_word):
        for suffix in PRED_C_SUFFIXES:
            if last_word.find(suffix) != -1:
                for word in sentence:
                    for suff in PRED_C_POSS_SUFFIXES:
                        for add_word in PRED_C_ADD:
                            lookup_word = add_word + suff
                            if word == lookup_word:
                                return last_word

    def is_pred_d(self, sentence, last_word):
        for suffix in PRED_D_SUFFIXES:
            if last_word.endswith(suffix):
                for word in sentence:
                    for suff in PRED_D_POSS_SUFFIXES:
                        for add_word in PRED_D_ADD:
                            lookup_word = add_word + suff
                            if word == lookup_word:
                                return last_word

    def is_pred_last(self, sentence, last_word):
        for suff in PRED_SUFFIXES:
            if last_word.find(suff) != -1:
                return last_word

    def is_tagged_pred(self, sentence):
        word = self.is_pred_a(sentence, sentence[-1])
        if not word:
            word = self.is_pred_b(sentence, sentence[-1])
            if not word:
                word = self.is_pred_c(sentence, sentence[-1])
                if not word:
                    word = self.is_pred_last(sentence, sentence[-1])
                    if not word:
                        word = None
        return word
