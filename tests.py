import re

from kazakh_tagger import KazakhTagger
from rules import SUB_SUFFIXES

kz = KazakhTagger()

assert kz.is_plural('фзарбда')
text = 'Тест гегтар аeeлар'.split()
assert kz.is_tagged_sub(text) is text[1]

text = 'Тест гетаркіш аeeлаауцпкуаракцкц'.split()
assert kz.is_tagged_sub(text) is text[0]

text = 'Тест ныыыыыыыаааане суеды'.split()
assert kz.is_tagged_obj(text) is text[1]
text = 'Тест отырбыз суеып'.split()
assert kz.is_pred_a(text) is text[1]
text = 'Тест отырбыз суеыпаербыз'.split()
assert kz.is_pred_b(text, text[-1]) is text[2]
text = 'Тест отырбыз ебыз суеыпаербep'.split()
assert kz.is_pred_c(text, text[-1]) is text[-1]

text = 'Тест отырбыз едібын дер суеыпаербepғыла'.split()
assert kz.is_pred_d(text, text[-1]) is text[-1]

