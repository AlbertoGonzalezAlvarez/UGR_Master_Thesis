import unidecode


def camel_case_deputy_name(name):
	return name.replace('-', ' ').title()


def filter_special_characters(chain):
	return unidecode.unidecode(chain.replace(' ', ''))