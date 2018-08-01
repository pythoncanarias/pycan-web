const APPS = ['commons', 'events', 'homepage']

const LIBS = {
    CSS: {
        commons: [
            'node_modules/@fortawesome/fontawesome-free/css/all.css'
        ],
        events: [
            'node_modules/bootstrap/dist/css/bootstrap.css',
        ]
    },
    JS: {
        commons: [
            'node_modules/jquery/dist/jquery.js',
            'node_modules/bootstrap/dist/js/bootstrap.js',
            'node_modules/popper.js/dist/umd/popper.js',
            'node_modules/holderjs/holder.js'
        ]
    }
}

export {
    APPS,
    LIBS
}