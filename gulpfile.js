require("es6-promise").polyfill();

const gulp = require("gulp");
const browserify = require("browserify");
const concatCss = require("gulp-concat-css");
const cleanCSS = require("gulp-clean-css");
const sass = require("gulp-sass")(require("sass")); // Switch to Dart Sass
const uglify = require("gulp-uglify");
const buffer = require("vinyl-buffer");
const source = require("vinyl-source-stream");
const sourcemaps = require("gulp-sourcemaps");
const merge = require("merge-stream");
const postcss = require("gulp-postcss");
const pxtorem = require("postcss-pxtorem");
const autoprefixer = require("autoprefixer");
const replace = require("gulp-replace");
const { exec } = require("child_process");
const util = require("util");
const execPromise = util.promisify(exec);

const cssProcessors = [
  autoprefixer(),
  pxtorem({
    rootValue: 14,
    replace: false,
    propWhiteList: [],
  }),
];

gulp.task("scripts", function () {
  return browserify("./jet/static/jet/js/src/main.js")
    .bundle()
    .on("error", function (error) {
      console.error("browserify error:", error);
      this.emit("end");
    })
    .pipe(source("bundle.min.js"))
    .pipe(buffer())
    .pipe(uglify())
    .on("error", function (error) {
      console.error("uglify error:", error);
      this.emit("end");
    })
    .pipe(gulp.dest("./jet/static/jet/js/build/"));
});

gulp.task("styles", function () {
  return gulp
    .src("./jet/static/jet/css/**/*.scss", { allowEmpty: true })
    .pipe(sourcemaps.init())
    .pipe(sass({ outputStyle: "compressed" }))
    .on("error", function (error) {
      console.error("sass error:", error);
      this.emit("end");
    })
    .pipe(postcss(cssProcessors))
    .on("error", function (error) {
      console.error("postcss error:", error);
      this.emit("end");
    })
    .pipe(sourcemaps.write("./"))
    .pipe(gulp.dest("./jet/static/jet/css"));
});

// Split vendor-styles into separate subtasks
gulp.task("vendor-styles-images", function () {
  return gulp
    .src("./node_modules/jquery-ui/themes/base/images/*", { allowEmpty: true })
    .pipe(gulp.dest("./jet/static/jet/css/jquery-ui/images/"))
    .on("error", function (error) {
      console.error("vendor-styles-images error:", error);
      this.emit("end");
    });
});

gulp.task("vendor-styles-jquery-ui", function () {
  return gulp
    .src(["./node_modules/jquery-ui/themes/base/all.css"], { allowEmpty: true })
    .pipe(cleanCSS())
    .on("error", function (error) {
      console.error("cleanCSS error:", error);
      this.emit("end");
    })
    .pipe(concatCss("jquery-ui.css", { rebaseUrls: false }))
    .on("error", function (error) {
      console.error("concatCss error:", error);
      this.emit("end");
    })
    .pipe(replace("images/", "jquery-ui/images/"))
    .on("error", function (error) {
      console.error("replace error:", error);
      this.emit("end");
    })
    .pipe(gulp.dest("./jet/static/jet/css/temp/"));
});

gulp.task("vendor-styles-other", function () {
  return gulp
    .src(
      [
        "./node_modules/select2/dist/css/select2.css",
        "./jet/static/jet/css/jquery.ui.timepicker.css",
        "./jet/static/jet/css/temp/jquery-ui.css",
      ],
      { allowEmpty: true },
    )
    .pipe(postcss(cssProcessors))
    .on("error", function (error) {
      console.error("postcss error:", error);
      this.emit("end");
    })
    .pipe(concatCss("vendor.css", { rebaseUrls: false }))
    .on("error", function (error) {
      console.error("concatCss vendor error:", error);
      this.emit("end");
    })
    .pipe(cleanCSS())
    .on("error", function (error) {
      console.error("cleanCSS vendor error:", error);
      this.emit("end");
    })
    .pipe(gulp.dest("./jet/static/jet/css"));
});

// Combine vendor-styles subtasks into a series
gulp.task(
  "vendor-styles",
  gulp.series(
    "vendor-styles-images",
    "vendor-styles-jquery-ui",
    "vendor-styles-other",
  ),
);

// Split vendor-translations into separate subtasks
gulp.task("vendor-translations-jquery-ui", function () {
  return gulp
    .src(["./node_modules/jquery-ui/ui/i18n/*.js"], { allowEmpty: true })
    .pipe(gulp.dest("./jet/static/jet/js/i18n/jquery-ui/"))
    .on("error", function (error) {
      console.error("jquery-ui translation error:", error);
      this.emit("end");
    });
});

gulp.task("vendor-translations-timepicker", function () {
  return gulp
    .src(["./node_modules/jquery-ui-timepicker-addon/dist/i18n/*.js"], {
      allowEmpty: true,
    })
    .pipe(gulp.dest("./jet/static/jet/js/i18n/jquery-ui-timepicker/"))
    .on("error", function (error) {
      console.error("timepicker translation error:", error);
      this.emit("end");
    });
});

gulp.task("vendor-translations-select2", function () {
  return gulp
    .src(["./node_modules/select2/dist/js/i18n/*.js"], { allowEmpty: true })
    .pipe(gulp.dest("./jet/static/jet/js/i18n/select2/"))
    .on("error", function (error) {
      console.error("select2 translation error:", error);
      this.emit("end");
    });
});

// Combine subtasks into a series
gulp.task(
  "vendor-translations",
  gulp.series(
    "vendor-translations-jquery-ui",
    "vendor-translations-timepicker",
    "vendor-translations-select2",
  ),
);

gulp.task("locales", async function () {
  try {
    await execPromise("python manage.py compilemessages", { stdio: "inherit" });
  } catch (error) {
    console.error("locales error:", error);
  }
});

// Use series instead of parallel to avoid stream conflicts
gulp.task(
  "build",
  gulp.series(
    "scripts",
    "styles",
    "vendor-styles",
    "vendor-translations",
    "locales",
  ),
);

gulp.task("watch", function () {
  gulp.watch("./jet/static/jet/js/src/**/*.js", gulp.series("scripts"));
  gulp.watch("./jet/static/jet/css/**/*.scss", gulp.series("styles"));
  gulp.watch(
    ["./jet/locale/**/*.po", "./jet/dashboard/locale/**/*.po"],
    gulp.series("locales"),
  );
});

gulp.task("default", gulp.series("build", "watch"));
