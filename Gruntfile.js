module.exports = function(grunt) {
    grunt.initConfig({
        copy: {
            main: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        cwd: "bower_components/",
                        src: ["angular/angular.min.js", 
                              "angular-bootstrap/ui-bootstrap-tpls.js",
                              "angular-sanitize/angular-sanitize.min.js",
                              "angular-sanitize/angular-sanitize.min.js.map",
                              "angular-ui-router/release/angular-ui-router.min.js",
                              "bootstrap/dist/js/bootstrap.min.js",
                              "lodash/dist/lodash.underscore.min.js",
                              "jquery/dist/jquery.min.js",
                              "jquery/dist/jquery.min.map"],
                        dest: "tos/static/js/lib/",
                        filter: "isFile"
                    },
                    {
                        expand: true,
                        flatten: true,
                        cwd: "bower_components/",
                        src: ["bootstrap/dist/css/bootstrap.min.css",
                              "font-awesome/css/font-awesome.min.css"],
                        dest: "tos/static/css/lib/"
                    },
                    {
                        expand: true,
                        flatten: true,
                        cwd: "bower_components/",
                        src: ["font-awesome/fonts/*"],
                        dest: "tos/static/css/fonts/"
                    },
                ]
            }
        }
    });
    
    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.registerTask("default", ["copy"]);
};