import gulp from 'gulp'
import del from 'del'

import { buildVendor } from './gulp/tasks/vendor'
import { buildCustom } from './gulp/tasks/custom'
import { moveResources } from './gulp/tasks/resources'
import { revFiles } from './gulp/tasks/rev'


gulp.task('default', make)

gulp.task('watch', gulp.series(make, watch))


function make(done) {
  return gulp.series(
    clean,
    gulp.parallel(buildVendor, buildCustom, moveResources),
    revFiles
  )(done)
}

function clean() {
  return del(['./static/*'], { dot: true })
}

function watch() {
  return gulp.watch('*/**/static/**/*.{scss,js}')
    .on('all', gulp.series(buildCustom, revFiles))
}
