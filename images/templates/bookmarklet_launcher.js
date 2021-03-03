(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(document.createElement('script')).src='https://mysite.com:9999/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();
