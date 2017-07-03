import spacy

def parse(doc, lemmatize=False):
	return get_parse_tree(get_document_root(doc), lemmatize)

def get_parse_tree(root, lemmatize=False):
	if not root.children:
		return root.lemma_ if lemmatize else root.text

	ret = []
	for i in root.lefts:
		ret.append('[' + i.dep_)
		ret += get_parse_tree(i)
		ret.append(']' + i.dep_)

	ret.append(root.lemma_ if lemmatize else root.text)

	for i in root.rights:
		ret.append('[' + i.dep_)
		ret += get_parse_tree(i)
		ret.append(']' + i.dep_)

	return ret

def get_document_root(document):
	return [w for w in document if w.head is w][0]

if __name__ == '__main__':
	nlp = spacy.load('en')
	doc = nlp("red Label is confused with Python and Java")

	print(parse(doc))

