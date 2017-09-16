var text = function()
{
    var lines = require('fs').readFileSync
		("/home/pi/Desktop/data.txt",
		'utf-8').split('\n')
		.filter(Boolean);
    return lines;
}