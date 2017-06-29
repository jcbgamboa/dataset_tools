# -*- coding: utf-8 -*-

# Example file explaining how to add a sentiment analysis module to the spaCy
# pipeline. You can plug in any code into `get_sentiment()`. Notice that
# `token` is a spaCy Token, which means it has access to the Document it came
# from (you can access it through `token.doc`), its PoS tags (through token.pos_
# and token.tag_), its dependencies, etc.. Look at the documentation of spaCy
# for more details.

import sys
import os

existing_analysers = {}

def get_sentiment(token):
    return 0

def add_sentiment_hook(doc, language, consider_modifiers=True):
    doc.user_token_hooks['sentiment'] = get_sentiment
    return doc

