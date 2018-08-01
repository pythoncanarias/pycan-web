import gulp from 'gulp'
import rev from 'gulp-rev'
import rewrite from 'gulp-rev-rewrite'


function revFiles() {
    return gulp.src('static/.tmp/**/*')
        .pipe(rev())
        .pipe(rewrite())
        .pipe(gulp.dest('static/'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('static/'))
}


export {
    revFiles
}