jQuery(function($) {
    //speak("Yo dawg, I heard you like text-to-speech, so I'm working on this site that will read other sites for you.");

    function got_lines(lines) {
	function read_next_line() {
	    if (lines.length) {
		var line = lines.shift();
		speak(line, {callback: read_next_line});
	    }
	}
	read_next_line();
    }

    function read_error(xhr, status, http_error) {
        speak('Sorry, there was an error requesting the specified URL.');
        speak(status);
        speak(http_error);
    }

    function get_lines(url) {
        $.ajax('/read', {
            type: 'GET',
            data: {'url': url},
            dataType: 'json',
            success: got_lines,
            error: read_error
        });
    }

    var url = new String(window.location);
    if (url.search('\\?') != -1) {
        $('body').append(url.split('?')[1]);
        get_lines(url.split('?')[1])
    }
});