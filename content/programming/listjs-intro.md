Title: ListJS: Sort, Filters, Search and more for HTML lists and tables in Javascript 
Date: 2014-08-08 21:37

[TOC]

Self contained javascript library to make lists of information awesome!

<http://listjs.com/docs>

### listjs.html

    <!DOCTYPE html>
    <html>
    <head>
    <script src="http://listjs.com/no-cdn/list.js"></script>
    
    <style type="text/css">
    .list {
      font-family:sans-serif;
      margin:0;
      padding:20px 0 0;
    }
    .list > li {
      display:block;
      background-color: #eee;
      padding:10px;
      box-shadow: inset 0 1px 0 #fff;
    }
    .avatar {
      max-width: 150px;
    }
    img {
      max-width: 100%;
    }
    h3 {
      font-size: 16px;
      margin:0 0 0.3rem;
      font-weight: normal;
      font-weight:bold;
    }
    p {
      margin:0;
    }
    
    input {
      border:solid 1px #ccc;
      border-radius: 5px;
      padding:7px 14px;
      margin-bottom:10px
    }
    input:focus {
      outline:none;
      border-color:#aaa;
    }
    .sort {
      padding:8px 30px;
      border-radius: 6px;
      border:none;
      display:inline-block;
      color:#fff;
      text-decoration: none;
      background-color: #28a8e0;
      height:30px;
    }
    .sort:hover {
      text-decoration: none;
      background-color:#1b8aba;
    }
    .sort:focus {
      outline:none;
    }
    .sort:after {
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-bottom: 5px solid transparent;
      content:"";
      position: relative;
      top:-10px;
      right:-5px;
    }
    .sort.asc:after {
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 5px solid #fff;
      content:"";
      position: relative;
      top:13px;
      right:-5px;
    }
    .sort.desc:after {
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-bottom: 5px solid #fff;
    </style>
    
    
    
    <meta charset=utf-8 />
    <title>Existing list</title>
    </head>
    <body>
    
    <div id="users">
      <input class="search" placeholder="Search" />
      <button class="sort" data-sort="name">
        Sort by name
      </button>
    
      <ul class="list">
        <li>
          <h3 class="name">Jonny Stromberg</h3>
          <p class="born">1986</p>
        </li>
        <li>
          <h3 class="name">Jonas Arnklint</h3>
          <p class="born">1985</p>
        </li>
        <li>
          <h3 class="name">Martina Elm</h3>
          <p class="born">1986</p>
        </li>
        <li>
          <h3 class="name">Gustaf Lindqvist</h3>
          <p class="born">1983</p>
        </li>
      </ul>
    
    </div>
    
    <script type="text/javascript">
        var options = {
            valueNames: [ 'name', 'born' ]
        };
    
        var userList = new List('users', options);
    </script>
    
    </body>
    </html>

### ListJS with Pelican and Jinja2

ListJS with the Pelican elegant theme to list all the articles sortable/searchable, default pagination for ListJS set to 1000 items

    :::html
	{% extends "base.html" %}
	
	{% block title %}
	All Categories · {{ super() }}
	{% endblock title %}
	
	{% block head_description %}
	All categories of the {{ SITENAME|striptags }} blog. 
	{% endblock head_description %}
	{% block content %}
	
	
	<head>
	    <script src="http://listjs.com/no-cdn/list.js"></script>
	
	    <style type="text/css">
	        h3 {
	            font-size: 16px;
	            margin:0 0 0.3rem;
	            font-weight: normal;
	            font-weight:bold;
	        }
	        p {
	            margin:0;
	        }
	
	        input {
	            border:solid 1px #ccc;
	            border-radius: 5px;
	            padding:7px 14px;
	            margin-bottom:10px
	        }
	        input:focus {
	            outline:none;
	            border-color:#aaa;
	        }
	        .sort {
	            padding:8px 30px;
	            border-radius: 6px;
	            border:none;
	            display:inline-block;
	            color:#fff;
	            text-decoration: none;
	            background-color: #28a8e0;
	            height:30px;
	        }
	        .sort:hover {
	            text-decoration: none;
	            background-color:#1b8aba;
	        }
	        .sort:focus {
	            outline:none;
	        }
	        .sort:after {
	            width: 0;
	            height: 0;
	            border-left: 5px solid transparent;
	            border-right: 5px solid transparent;
	            border-bottom: 5px solid transparent;
	            content:"";
	            position: relative;
	            top:-10px;
	            right:-5px;
	        }
	        .sort.asc:after {
	            width: 0;
	            height: 0;
	            border-left: 5px solid transparent;
	            border-right: 5px solid transparent;
	            border-top: 5px solid #fff;
	            content:"";
	            position: relative;
	            top:13px;
	            right:-5px;
	        }
	        .sort.desc:after {
	            width: 0;
	            height: 0;
	            border-left: 5px solid transparent;
	            border-right: 5px solid transparent;
	            border-bottom: 5px solid #fff;
	        }
	    </style>
	
	</head>
	<body>
	
	
	<div id="article-list">
	    <button class="sort" data-sort="date">Sort by date</button>
	    <button class="sort" data-sort="title">Sort by title</button>
	    <input class="search" placeholder="Search" style="margin-top: 10px; height: 16px;"/>
	
	    <ul class="list">
	    {% for category, articles in categories %}
	        {% for article in articles %}
	        <li>
	            <span class="date" style="padding-right: 10px;">
	                <time pubdate="pubdate" datetime="{{ article.date.isoformat() }}">{{ article.locale_date }}</time>
	            </span>
	            <a href="{{ SITEURL }}/{{ article.url }}"><span class="title">{{ article.title }} {%if article.subtitle %}
	                <small> {{ article.subtitle }} </small> {% endif %}</span> </a>
	        </li>
	        {% endfor %}
	    {% endfor %}
	    </ul>
	</div>
	
	
	{% endblock content %}
	{% block script %}
	{{ super() }}
	<script  language="javascript" type="text/javascript">
	    function uncollapse() {
	            $(window.location.hash).collapse({
	                toggle: true
	            })
	    }
	</script>
	
	<script type="text/javascript" language="JavaScript">
	    uncollapse(); 
	</script>
	
	<script type="text/javascript">
	    var options = {
	        valueNames: [ 'date', 'title' ],
	        page: 1000
	    };
	    var hackerList = new List('article-list', options);
	    hackerList.sort('date')
	
	</script>
	
	{% endblock script %}


