/**
 * Build profile for django-require.
 * 
 * This supports all the normal configuration available to a r.js build
 * profile. The only gotchas are:
 *
 *   - 'baseUrl' will be overidden by django-require during the build process.
 *   - 'appDir' will be overidden by django-require during the build process.
 *   - 'dir' will be overidden by django-require during the build process. 
 *
 * r.js documentation:
 * http://requirejs.org/docs/optimization.html
 *
 * Reference of all configuration options:
 * https://github.com/jrburke/r.js/blob/master/build/example.build.js
 */
({
    modules: [
        {
            name: "main"
        }
    ],
    optimizeCss: "none",
    optimize: "uglify2",
    preserveLicenseComments: false,
    skipDirOptimize: true
})
