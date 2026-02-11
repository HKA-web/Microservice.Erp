module.exports = function (grunt) {
    const sass = require('node-sass');
    require('load-grunt-tasks')(grunt);
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        clean: {
            assets: ['assets/*'],
            data: ['data/*'],
        },
        sass: {
            options: {
                implementation: sass,
                sourceMap: true,
            },
            dist: {
                files: [
                    {'static/application/css/theme.css': ['static/application/scss/theme.scss']},
                    {'static/application/css/rtl.css': ['static/application/scss/rtl.scss']},
                    {'static/application/css/icon.css': ['static/application/scss/icon.scss']},
                    {'static/application/css/bootstrap.css': ['static/application/scss/bootstrap.scss']},
                ]
            }
        },
        shell: {
            runserver: {
                command: 'python manage.py runserver',
            },
        },
    });
    grunt.registerTask('run:server', [
        'shell:runserver',
    ]);
    grunt.registerTask('build:sass', [
        'sass',
    ]);
    grunt.registerTask('build:dist', [
        'clean:assets',
        'clean:data',
        'sass',
    ]);
    grunt.registerTask('default', [
        'sass',
    ]);
};
