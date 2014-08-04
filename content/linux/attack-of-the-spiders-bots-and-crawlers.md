Title: Attack of the Spiders, Bots, and Crawlers
Date: 2013-07-20 23:00
Author: John Pfeiffer
Slug: content/attack-of-the-spiders-bots-and-crawlers

It is well known that search engines need to index what the contents of webpages are in order to return accurate results to Users. It may not be well known how much traffic that generates.

In this sampling from my logs (not representative of anything), 57% of the traffic in the log is from bots (I'm not turning them away, skip to the end on how to do that).

Drupal (CMS) is remarkably good at making content for bots to read so it's not surprising they're all slurping, and of course if you want to be popular you need all of those indexes to know about you...

### How many hits from each kind of bot

`cat john-pfeiffer.access | wc -l` 
> 1108 hits

    cat john-pfeiffer.access | grep -v "Baiduspider" | grep -v "bingbot" | grep -v "YandexBot" | grep -v "Sogou" | grep -v "Mail.RU\_Bot" | grep -v "Googlebot" | grep -v "SISTRIX Crawler" | grep -v "MJ12bot" | wc -l  
    637

`cat john-pfeiffer.access | grep "Googlebot" | wc -l` 
> 105 hits from <https://en.wikipedia.org/wiki/Googlebot>
    
`cat john-pfeiffer.access | grep "bingbot" | wc -l` 
> 96 hits from <http://en.wikipedia.org/wiki/Bingbot>

`cat john-pfeiffer.access | grep "Baiduspider" | wc -l`
> 93 hits from <http://baidu.com/search/spider_english.html>

`cat john-pfeiffer.access | grep "SISTRIX Crawler" | wc -l`
> 76 hits from <http://crawler.sistrix.net>

`cat john-pfeiffer.access | grep "YandexBot" | wc -l`
> 64 hits from <http://www.botopedia.org/user-agent-list/search-bots/yandex-bot>

`cat john-pfeiffer.access | grep "Mail.RU\_Bot" | wc -l`
> 23 hits from <http://www.webmasterworld.com/search_engine_spiders/4520951.htm> , <http://www.botopedia.org/user-agent-list/search-bots/mailru-bot>

`cat john-pfeiffer.access | grep "MJ12bot" | wc -l`
> 12 hits from <http://www.majestic12.co.uk/projects/dsearch/mj12bot.php>

`cat john-pfeiffer.access | grep "Sogou" | wc -l`
> 7 hits from <http://www.botopedia.org/user-agent-list/search-bots/sogou-spider>


### More Info on Bots and Crawlers    
<http://www.incapsula.com/the-incapsula-blog/item/393-know-your-top-10-bots>

<http://searchenginewatch.com/article/2067357/Bye-bye-Crawler-Blocking-the-Parasites>

(Besides robots.txt you are pretty much left with ban by User-Agent or IP Address Range.)
