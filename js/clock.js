function update24hrClock ( )
{
	var currentTime = new Date ( );

	var currentHours = currentTime.getHours ( );
	var currentMinutes = currentTime.getMinutes ( );
	var currentSeconds = currentTime.getSeconds ( );

	// Pad the minutes and seconds with leading zeros, if required
	currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;
	currentSeconds = ( currentSeconds < 10 ? "0" : "" ) + currentSeconds;
	currentHours = ( currentHours < 10 ? "0" : "" ) + currentHours;-

	// Compose the string for display
	var current24hrTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds;

	// Update the time display
	document.getElementById("24hrclock").firstChild.nodeValue = current24hrTimeString;
}
setInterval('update24hrClock()', 1000 );

