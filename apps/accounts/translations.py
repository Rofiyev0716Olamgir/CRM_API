from modeltranslation.translator import TranslationOptions, translator
from .models import Group


class GroupTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(Group, GroupTranslationOptions)