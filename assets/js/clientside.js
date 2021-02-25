window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        collapse_function: function (n_clicks, actual_state) {
            if (actual_state == false) {
                return [true, 'far fa-minus-square mr-2 align-self-center'];
            }else{
                return [false, 'far fa-plus-square mr-2 align-self-center'];
            }
        }
    }
});