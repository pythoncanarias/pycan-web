var gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglifyjs = require('gulp-uglify'),
    uglifycss = require('gulp-uglifycss'),
    rev = require('gulp-rev'),
    sass = require('gulp-sass'),
    rewrite = require('gulp-rev-rewrite'),
    replace = require('gulp-replace');

const APPS = ['commons', 'events', 'homepage'];

const VENDOR_CSS = [
    'node_modules/bootstrap/dist/css/bootstrap.css',
    'node_modules/@fortawesome/fontawesome-free/css/all.css'
]

const VENDOR_JS = [
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.js',
    'node_modules/popper.js/dist/umd/popper.js',
    'node_modules/holderjs/holder.js'
]

gulp.task('default', ['make']);

gulp.task('watch', ['make'], function() {
    gulp.watch('apps/**/static/**/*.{scss,js}', ['build-custom', 'rev-files']);
});

gulp.task('make', ['build-vendor', 'build-custom', 'rev-files', 'move-fonts'])

gulp.task('build-vendor', ['build-vendor-css', 'build-vendor-js']);

gulp.task('build-vendor-css', function() {
    return gulp.src(VENDOR_CSS)
        .pipe(concat('vendor.min.css'))
        .pipe(replace('../webfonts', 'webfonts'))
        .pipe(uglifycss())
        .pipe(gulp.dest('static/.tmp/commons'));
})

gulp.task('build-vendor-js', function() {
    return gulp.src(VENDOR_JS)
        .pipe(concat('vendor.min.js'))
        .pipe(uglifyjs())
        .pipe(gulp.dest('static/.tmp/commons'));
})

gulp.task('build-custom', async function() {
    for (let app of APPS) {
        await Promise.all([
            buildCustomCss(app),
            buildCustomJs(app),
            moveImages(app)
        ])
    }
})

gulp.task('rev-files', ['build-vendor', 'build-custom'], function() {
    return gulp.src('static/.tmp/**/*')
        .pipe(rev())
        .pipe(rewrite())
        .pipe(gulp.dest('static/'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('static/'))
})

gulp.task('move-fonts', function() {
    return gulp.src('node_modules/@fortawesome/fontawesome-free/webfonts/**/*')
        .pipe(gulp.dest('static/commons/webfonts'))
})

function buildCustomCss(app) {
    return new Promise(function(resolve) {
        gulp.src(`apps/${app}/static/${app}/css/**/*.scss`)
            .pipe(sass())
            .pipe(concat('custom.min.css'))
            .pipe(uglifycss())
            .pipe(gulp.dest(`static/.tmp/${app}`))
            .on('end', resolve)
    })
}

function buildCustomJs(app) {
    return new Promise(function(resolve) {
        gulp.src(`apps/${app}/static/${app}/js/**/*.js`)
            .pipe(concat('custom.min.js'))
            .pipe(uglifyjs())
            .pipe(gulp.dest(`static/.tmp/${app}`))
            .on('end', resolve)
    })
}

function moveImages(app) {
    return new Promise(function(resolve) {
        gulp.src(`apps/${app}/static/${app}/img/**/*`)
            .pipe(gulp.dest(`static/.tmp/${app}/img`))
            .on('end', resolve)
    })
}
