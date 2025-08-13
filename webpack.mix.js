let mix = require('laravel-mix');

mix.js('mooc/static/assets/set_form.js', 'dist').setPublicPath('mooc/static/dist');
mix.css('mooc/static/assets/drag.css', 'dist').setPublicPath('mooc/static/dist');