$(':radio').change(function() {
	$('#myTabs a[href="#pet-review"]').click(function (e) {
		e.preventDefault()
		$(this).tab('show')
	})
	$('#myTabs a[href="#owner-review"]').click(function (e) {
		e.preventDefault()
		$(this).tab('show')
	})
})