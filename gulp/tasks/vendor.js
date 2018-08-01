const gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglifyjs = require('gulp-uglify'),
    uglifycss = require('gulp-uglifycss'),
    replace = require('gulp-replace'),
    noop = require('gulp-noop')

const { LIBS } = require('../config')


function buildVendor(done) {
    return gulp.parallel(buildVendorCss, buildVendorJs)(done)
}

function buildVendorCss() {
    const tasks = Object.keys(LIBS.CSS).map(app => getBuildVendorCssPromise(app))
    return Promise.all(tasks)
}

function buildVendorJs() {
    const tasks = Object.keys(LIBS.JS).map(app => getBuildVendorJsPromise(app))
    return Promise.all(tasks)
}

function getBuildVendorCssPromise(app) {
    return new Promise(function(resolve) {
        gulp.src(LIBS.CSS[app])
            .pipe(concat('vendor.min.css'))
            .pipe(app === 'commons' ? replace('../webfonts', 'webfonts') : noop())
            .pipe(uglifycss())
            .pipe(gulp.dest(`static/.tmp/${app}`))
            .on('end', resolve)
    })
}

function getBuildVendorJsPromise(app) {
    return new Promise(function(resolve) {
        gulp.src(LIBS.JS[app])
            .pipe(concat('vendor.min.js'))
            .pipe(uglifyjs())
            .pipe(gulp.dest(`static/.tmp/${app}`))
            .on('end', resolve)
    })
}


module.exports =  {
    buildVendor
}