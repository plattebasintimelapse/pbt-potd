module.exports = function(grunt) {

    var config = {
        assets: 'timelapse/static'
    };

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        config: config,

        watch: {
            options: {
                livereload: true
            },
            sass: {
                files: '<%= config.assets %>/sass/**/*.scss',
                tasks: ['sass']
            },
            js: {
                files: '<%= config.assets %>/js/{,*/}*.js',
                tasks: ['uglify']
            }
        },

        sass: {
            options: {
                sourcemap: 'none',
                style: 'compressed'
            },
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= config.assets %>/sass',
                    src: ['*.scss'],
                    dest: '<%= config.assets %>/',
                    ext: '.min.css'
                }]
            }
        },

        // Any new scripts added with Bower must be put into the files array below to get concat into main.min.js
        uglify: {
            dist: {
                options: {
                    banner: '/*! <%= pkg.name %> - v<%= pkg.version %> - ' +
                        '<%= grunt.template.today("yyyy-mm-dd") %> */'
                },
                files: {
                    '<%= config.assets %>/main.min.js': [
                        'bower_components/jquery/dist/jquery.min.js',
                        'bower_components/fullpage.js/vendors/jquery.easings.min.js',
                        'bower_components/fullpage.js/vendors/jquery.slimscroll.min.js',
                        'bower_components/fullpage.js/jquery.fullPage.min.js',
                        '<%= config.assets %>/js/main.js'
                    ]
                }
            }
        },

        copy: {
            dist: {
                files: [{
                    expand: true,
                    dot: true,
                    flatten: true,
                    cwd: '.',
                    dest: '<%= config.assets %>/fonts',
                    src: [
                        'bower_components/font-awesome/fonts/{,*/}*.*'
                    ]
                }]
            }
        }
    });

    require('load-grunt-tasks')(grunt, {scope: 'devDependencies'});

    grunt.registerTask('default', [
        'watch'
    ]);

    grunt.registerTask('build', [
        'sass',
        'uglify'
    ]);

    grunt.registerTask('ysha', function (target) {
        grunt.log.writeln( '*****************');
        grunt.log.writeln( '*****************');
        grunt.log.writeln( '** Ysha rules! **');
        grunt.log.writeln( '*****************');
        grunt.log.writeln( '*****************');
        grunt.log.writeln(  );
    });

};