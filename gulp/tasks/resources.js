const gulp = require('gulp'),
    rename = require('gulp-rename')


function moveResources(done) {
    return gulp.parallel(moveImages, moveFonts)(done)
}

function moveImages() {
    return gulp.src('apps/*/static/*/img/**/*')
        .pipe(rename(function(path) {
            path.dirname = path.dirname.split('/static/')[1]
        }))
        .pipe(gulp.dest('static/.tmp'))
}

function moveFonts() {
    return gulp.src('node_modules/@fortawesome/fontawesome-free/webfonts/**/*')
        .pipe(gulp.dest('static/commons/webfonts'))
}


module.exports =  {
    moveResources
}