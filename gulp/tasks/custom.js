import fs from 'fs'
import gulp from 'gulp'
import rename from 'gulp-rename'
import uglifyjs from 'gulp-uglify'
import uglifycss from 'gulp-uglifycss'
import sass from 'gulp-sass'
import babel from 'gulp-babel'
import rollup from 'rollup-stream'
import rollupResolve from 'rollup-plugin-node-resolve'
import source from 'vinyl-source-stream'
import vinylBuffer from 'vinyl-buffer'
import tildeImporter from 'node-sass-tilde-importer'

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
    gulp.src(`apps/${app}/static/${app}/css/main.scss`, { allowEmpty: true })
      .pipe(sass({importer: tildeImporter}))
      .pipe(rename('custom.min.css'))
      .pipe(modifyCustomCssUrlPath(app))
      .pipe(uglifycss())
      .pipe(gulp.dest(`static/.tmp/${app}`))
      .on('end', resolve)
  })
}

function getBuildCustomJsPromise(app) {
  return new Promise(function (resolve) {
    const input = `apps/${app}/static/${app}/js/main.js`

    if (!fs.existsSync(input)) {
      resolve()
      return
    }

    rollup({
      input: input,
      format: 'iife',
      plugins: [
        rollupResolve(),
      ],
    })
      .pipe(source('custom.min.js'))
      .pipe(vinylBuffer())
      .pipe(babel())
      .pipe(uglifyjs())
      .pipe(gulp.dest(`static/.tmp/${app}`))
      .on('end', resolve)
  })
}


export {
  buildCustom
}
