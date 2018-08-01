const gulp = require('gulp'),
    rev = require('gulp-rev'),
    rewrite = require('gulp-rev-rewrite')


function revFiles() {
    return gulp.src('static/.tmp/**/*')
        .pipe(rev())
        .pipe(rewrite())
        .pipe(gulp.dest('static/'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('static/'))
}


module.exports =  {
    revFiles
}