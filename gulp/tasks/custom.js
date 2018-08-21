import gulp from 'gulp'
import concat from 'gulp-concat'
import rename from 'gulp-rename'
import uglifyjs from 'gulp-uglify'
import uglifycss from 'gulp-uglifycss'
import sass from 'gulp-sass'
import babel from 'gulp-babel'

import { APPS } from '../config'
import modifyCustomCssUrlPath from './utils/custom_css_url_path'


function buildCustom() {
  let tasks = []
  for (let app of APPS) {
    tasks.push(getBuildCustomCssPromise(app))
    tasks.push(getBuildCustomJsPromise(app))
  }
  return Promise.all(tasks)
}

function getBuildCustomCssPromise(app) {
  return new Promise(function (resolve) {
    gulp.src(`${app}/static/${app}/css/main.scss`, { allowEmpty: true })
      .pipe(sass())
      .pipe(rename('custom.min.css'))
      .pipe(modifyCustomCssUrlPath(app))
      .pipe(uglifycss())
      .pipe(gulp.dest(`static/.tmp/${app}`))
      .on('end', resolve)
  })
}

function getBuildCustomJsPromise(app) {
  return new Promise(function (resolve) {
    gulp.src(`${app}/static/${app}/js/**/*.js`)
      .pipe(babel())
      .pipe(concat('custom.min.js'))
      .pipe(uglifyjs())
      .pipe(gulp.dest(`static/.tmp/${app}`))
      .on('end', resolve)
  })
}


export {
  buildCustom
}
