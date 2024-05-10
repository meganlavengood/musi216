$(function () {
	// create an object with the date of one week ago
	var yesterday = new Date();
	yesterday.setDate(yesterday.getDate() - 1);
	// fudging dates for testing
	// var yesterday = new Date('September 25, 2024 00:00:00 GMT-5:00');
	let yesterdayEpoch = Date.parse(yesterday);
	console.log(yesterday);
	console.log(yesterdayEpoch);

	// loop through all list items with a date
	$("div[date]").each(function () {
		// create a postDate in a date object
		var postDate = Date.parse($(this).attr("date"));
		console.log($(this).attr("date"));
		console.log(postDate);

		// compare dates and hide old posts
		if (postDate < yesterdayEpoch) $(this).hide();
	});

	// open links to outside sites in new tab
	$(document.links)
		.filter(function () {
			return this.hostname != window.location.hostname;
		})
		.attr("target", "_blank");

});

// hide things in iframe view 
if (window.location.href.indexOf("iframe=true") > -1) {
	let els = document.getElementsByClassName("hide-on-embed");
	for (let el of els) el.style.display = "none";
}