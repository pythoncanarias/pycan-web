import replace from 'gulp-replace'

function modifyCustomCssUrlPath(app) {
  /*
   * Examples (from a css file on events app):
   * url(./img/keyboard.jpg) => url("/static/events/img/keyboard.jpg")
   * url(../commons/img/logo.jpg) => url("/static/commons/img/logo.jpg")
   * url(events/img/keyboard.jpg) => url("/static/events/img/keyboard.jpg")
   * url(/events/img/keyboard.jpg) => url("/static/events/img/keyboard.jpg")
   *
   * External urls are not modified:
   * url(http://google.com/img.jpg)
   * url(https://google.com/img.jpg)
   *
   * It works with singles quotes, with double quotes or without quotes.
   */
  return replace(/url\(["']?\/?([\w\/\-\.]+)["']?\)/ig, function (match, path) {
    let absolute_path = path.replace('../', '').replace('./', `${app}/`)
    return `url("/static/${absolute_path}")`
  })
}

export default modifyCustomCssUrlPath
