var browserify = require('browserify'),
    
    uglifyify = require('uglifyify'),
    reactify = require('reactify'),
    fs = require('fs');

try {
    var coffeeify  = require('coffeeify'),
        creactify = require('coffee-reactify');
} catch(e) {}

function make_bundle(bundle_file, requires, files, debug)
{
	var b = browserify({debug: debug, global: true})
    b.transform({global: true}, coffeeify);
	b.transform({global: true}, reactify);
    b.transform({global: true}, creactify);
    if (!debug)
        b.transform({global: true}, uglifyify);
	requires.forEach(function(element, index, array) {
        b.require(element);
    });
    files.forEach(function(element, index, array) {
        b.require(element[1], {expose: element[0]});
    });
    b.bundle().pipe(fs.createWriteStream(bundle_file));
}