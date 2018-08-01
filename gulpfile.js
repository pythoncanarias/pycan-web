const gulp = require('gulp')

const { buildVendor } = require('./gulp/tasks/vendor'),
    { buildCustom } = require('./gulp/tasks/custom'),
    { moveResources } = require('./gulp/tasks/resources'),
    { revFiles } = require('./gulp/tasks/rev')


gulp.task('default', make)

function make(done) {
    return gulp.series(
        gulp.parallel(buildVendor, buildCustom, moveResources),
        revFiles
    )(done)
}

gulp.task('watch', gulp.series(make, watch))

function watch() {
    return gulp.watch('apps/**/static/**/*.{scss,js}')
        .on('change', gulp.series(buildCustom, revFiles))
}