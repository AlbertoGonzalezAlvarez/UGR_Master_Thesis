from config import PAGE_ROUTES


def rgb_to_rgba(rgb_value, alpha):
    return f"rgba{rgb_value[3:-1]}, {alpha})"


def get_page_name(id):
    for page in PAGE_ROUTES:
        if page['id'] == id:
            return page['name']


def get_page_route(id):
    for page in PAGE_ROUTES:
        if page['id'] == id:
            return page['route']


def decompose_callback(callback):
    decomposed_callback = []

    for component in callback:
        component_parts = component.split('.')
        component_id, component_property = component_parts[0], component_parts[1]
        property_value = callback[component]

        if len(callback) > 1:
            decomposed_callback.append({
                'id': component_id,
                'property': component_property,
                'value': property_value
            })
        else:
            decomposed_callback = {
                'id': component_id,
                'property': component_property,
                'value': property_value
            }

    return decomposed_callback
