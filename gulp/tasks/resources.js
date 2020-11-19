import gulp from 'gulp'
import rename from 'gulp-rename'
import { NODE_MODULES_DIR } from '../config'


function moveResources(done) {
  return gulp.parallel(moveImages, moveFonts)(done)
}

function moveImages() {
  return gulp.src('*/static/*/img/**/*')
    .pipe(rename(function (path) {
      path.dirname = path.dirname.split('/static/')[1]
    }))
    .pipe(gulp.dest('static/.tmp'))
}

function moveFonts() {
  return gulp.src(NODE_MODULES_DIR + '/@fortawesome/fontawesome-free/webfonts/**/*')
    .pipe(gulp.dest('static/commons/webfonts'))
}


export {
  moveResources
}
