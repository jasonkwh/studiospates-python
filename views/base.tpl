<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Studios Pâtes</title>
<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,400italic,700,700italic' rel='stylesheet' type='text/css'>
<link href="/static/style.css" rel="stylesheet">
<script src="http://zeptojs.com/zepto.min.js"></script>
<script src="/static/script.js"></script>
<link rel="stylesheet" href="/static/vegas.min.css">
<script src="/static/vegas.min.js"></script>
</head>
<body>
<script>function submitenter(a,b){var c;if(window.event)c=window.event.keyCode;else{if(!b)return!0;c=b.which}return 13==c?(a.form.submit(),!1):!0}$("#example, body").vegas({timer:!1,preloadImage:!0,transitionDuration:3e3,shuffle:!0,slides:[{src:"https://dl.dropboxusercontent.com/u/4846156/studiospates/bg01.jpg"},{src:"https://dl.dropboxusercontent.com/u/4846156/studiospates/bg02.jpg"},{src:"https://dl.dropboxusercontent.com/u/4846156/studiospates/bg03.jpg"}],overlay:"https://dl.dropboxusercontent.com/u/4846156/studiospates/overlays/01.png"});</script>
<header>
<a href="/"><img src="/static/images/logo.png" /></a>
</header>
<div id='cssmenu'>
<ul>
   <li class='active'><a href='/'><span>Home</span></a></li>
   <li class='has-sub'><a href='#'><span>Projects</span></a>
      <ul>
         <li><a href='game.html'><span>Product 1</span></a></li>
         <li><a href='#'><span>Product 2</span></a></li>
         <li class='last'><a href='#'><span>Product 3</span></a></li>
      </ul>
   </li>
   <li class='last'><a href='/about'><span>About</span></a></li>
</ul>
</div>
<div class="content">
<section>
{{!base}}
</section>
<footer>
<p>©2016 <a href="mailto:jasonkwh@gmail.com?subject=FAQ">Studios Pâtes</a>.</p>
</footer>
</div>
<div class="sidebar">
<section>
<form name="searchForm" method="POST" action ="/search">
<input type="text" name="search" placeholder="search something..." class="focus" onKeyPress="return submitenter(this,event)">
</form>
</section>
</div>
<div class="sidebar2">
<section>
{{!login}}
{{!validate}}
</section>
</div>
</body>
</html>