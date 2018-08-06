const APPS = ['commons', 'events', 'homepage']

const LIBS = {
  CSS: {
    commons: [
      'node_modules/@fortawesome/fontawesome-free/css/all.css',
      'apps/commons/static/commons/css/vendor.scss'
    ],
    homepage: [
      'apps/homepage/static/homepage/css/vendor.scss'
    ]
  },
  JS: {}
}

export {
  APPS,
  LIBS
}
