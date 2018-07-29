var gulp = require('gulp'),
    concat = require('gulp-concat'),
    uglifyjs = require('gulp-uglify'),
    uglifycss = require('gulp-uglifycss'),
    rev = require('gulp-rev'),
    rename = require('gulp-rename'),
    sass = require('gulp-sass'),
    rewrite = require('gulp-rev-rewrite'),
    replace = require('gulp-replace');

VENDOR_CSS = [
    'node_modules/bootstrap/dist/css/bootstrap.css',
    'node_modules/@fortawesome/fontawesome-free/css/all.css'
]

VENDOR_JS = [
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.js',
    'node_modules/popper.js/dist/umd/popper.js',
    'node_modules/holderjs/holder.js'
]

gulp.task('default', ['make']);

gulp.task('make', ['build-vendor', 'build-custom', 'move-fonts'])

gulp.task('build-vendor', function() {
    gulp.src(VENDOR_CSS)
        .pipe(concat('vendor.css'))
        .pipe(replace('../webfonts', 'webfonts'))
        .pipe(uglifycss())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest('static/.tmp/commons'));
    return gulp.src(VENDOR_JS)
        .pipe(concat('vendor.js'))
        .pipe(uglifyjs())
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest('static/.tmp/commons'));
})

gulp.task('build-custom', async function() {
    var apps = ['commons', 'events', 'homepage'];
    for (let app of apps) {
        await buildCustom(app);
        await moveImages(app);
        await revFiles(app);
    }
})

gulp.task('move-fonts', function() {
    return gulp.src('node_modules/@fortawesome/fontawesome-free/webfonts/**/*')
        .pipe(gulp.dest('static/commons/webfonts'))
})

function buildCustom(app) {
    return Promise.all([
        new Promise(function(resolve) {
            gulp.src('apps/**/static/' + app + '/css/**/*.scss')
                .pipe(sass())
                .pipe(concat('custom.css'))
                .pipe(uglifycss())
                .pipe(rename({ suffix: '.min' }))
                .pipe(gulp.dest('static/.tmp/' + app))
                .on('end', resolve)
        }),
        new Promise(function(resolve) {
            gulp.src('apps/**/static/' + app + '/js/**/*.js')
                .pipe(concat('custom.js'))
                .pipe(uglifyjs())
                .pipe(rename({ suffix: '.min' }))
                .pipe(gulp.dest('static/.tmp/' + app))
                .on('end', resolve)
        })
    ])
}

function moveImages(app) {
    return new Promise(function(resolve) {
        gulp.src('apps/' + app + '/static/' + app + '/img/**/*')
            .pipe(gulp.dest('static/.tmp/' + app + '/img'))
            .on('end', resolve)
        })
}

function revFiles(app) {
    return new Promise(function(resolve) {
        gulp.src('static/.tmp/' + app + '/**/*')
            .pipe(rev())
            .pipe(rewrite())
            .pipe(gulp.dest('static/' + app + '/'))
            .pipe(rev.manifest())
            .pipe(gulp.dest('static/' + app + '/'))
            .on('end', resolve)
        })
}
