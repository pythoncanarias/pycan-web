import gulp from 'gulp'

import { buildVendor } from './gulp/tasks/vendor'
import { buildCustom } from './gulp/tasks/custom'
import { moveResources } from './gulp/tasks/resources'
import { revFiles } from './gulp/tasks/rev'


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
        .on('all', gulp.series(buildCustom, revFiles))
}