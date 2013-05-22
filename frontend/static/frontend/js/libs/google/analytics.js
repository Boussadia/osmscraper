define([
],
function(){
	var GooglAnalyticsHelper = {
		ACOUNT_ID : 'UA-33426317-3',
		DOMAIN_NAME: 'mastercourses.com',

		init: function() {
			var _gaq = window._gaq = _gaq || [],
			ga = document.createElement('script'),
			s = document.getElementsByTagName('script')[0];

			_gaq.push(['_setAccount', this.ACOUNT_ID]);
			_gaq.push(['_setDomainName', this.DOMAIN_NAME]);
			_gaq.push(['_setAllowLinker', true]);

			ga.type = 'text/javascript';
			ga.async = true;
			ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';

			s.parentNode.insertBefore(ga, s);
		},
		
		track : function(url){
			_gaq.push(['_trackPageview', "/"+url])
		}
		// _trackEvent pour tracker des events spécifiques
	};
	return GooglAnalyticsHelper;
});