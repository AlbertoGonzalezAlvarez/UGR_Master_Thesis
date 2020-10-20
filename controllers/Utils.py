from config.AppConfig import PAGE_ROUTES


def get_page_name(id):
	for page in PAGE_ROUTES:
		if page['id'] == id:
			return page['name']


def get_page_route(id):
	for page in PAGE_ROUTES:
		if page['id'] == id:
			return page['route']