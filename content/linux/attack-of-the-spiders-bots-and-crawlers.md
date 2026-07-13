Title: Attack of the Spiders, Bots, and Crawlers
Date: 2013-07-20 23:00

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
> 96 hits from <https://en.wikipedia.org/wiki/Bingbot>

`cat john-pfeiffer.access | grep "Baiduspider" | wc -l`
> 93 hits from <https://www.baidu.com/search/robots_english.html>

`cat john-pfeiffer.access | grep "SISTRIX Crawler" | wc -l`
> 76 hits from <https://www.sistrix.com/support/handbook/optimizer/crawling-log/>

`cat john-pfeiffer.access | grep "YandexBot" | wc -l`
> 64 hits from <https://web.archive.org/web/20141006192654/www.botopedia.org/user-agent-list/search-bots/yandex-bot>

`cat john-pfeiffer.access | grep "Mail.RU\_Bot" | wc -l`
> 23 hits from <https://www.webmasterworld.com/search_engine_spiders/4520951.htm> , <http://www.botopedia.org/user-agent-list/search-bots/mailru-bot>

`cat john-pfeiffer.access | grep "MJ12bot" | wc -l`
> 12 hits from <https://www.majestic12.co.uk/projects/dsearch/>

`cat john-pfeiffer.access | grep "Sogou" | wc -l`
> 7 hits from <https://web.archive.org/web/20141010233507/http://www.botopedia.org/user-agent-list/search-bots/sogou-spider>


### More Info on Bots and Crawlers    

<https://web.archive.org/web/20131028113445/http://www.incapsula.com/the-incapsula-blog/item/393-know-your-top-10-bots>

<https://searchenginewatch.com/article/2067357/Bye-bye-Crawler-Blocking-the-Parasites>

(Besides robots.txt you are pretty much left with ban by User-Agent or IP Address Range.)

