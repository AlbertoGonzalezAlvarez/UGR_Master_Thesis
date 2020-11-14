window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        collapse_function: function (n_clicks) {
            let collapse_icon;
            let open_status;

            if (n_clicks == null) {
                return [true, 'far fa-minus-square mr-2 align-self-center'];
            }

            collapse_icon = n_clicks % 2 == 0 ? 'far fa-minus-square mr-2 align-self-center' :
                'far fa-plus-square mr-2 align-self-center';
            open_status = n_clicks % 2 == 0 ? true : false

            return [open_status, collapse_icon];
        }
    }
});