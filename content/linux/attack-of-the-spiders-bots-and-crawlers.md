Title: Attack of the Spiders, Bots, and Crawlers
Date: 2013-07-20 23:00
Author: John Pfeiffer
Slug: content/attack-of-the-spiders-bots-and-crawlers

It is well known that search engines need to index what the contents of webpages are in order to return accurate results to Users.

It may not be well known how much traffic that generates!
In this sampling from my logs (not representative of anything), 57% of the traffic in the log is from bots (I'm not turning them away, skip to the end on how to do that).

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">

</p>

</p>

Drupal (CMS) is remarkably good at making content for bots to read so
it's not surprising they're all slurping, and of course if you want to
be popular you need all of those indexes to know about you...

</p>

cat john-pfeiffer.access | wc -l \# 1108

</p>

cat john-pfeiffer.access | grep -v "Baiduspider" | grep -v "bingbot" |
grep -v "YandexBot" | grep -v "Sogou" | grep -v "Mail.RU\_Bot" | grep -v
"Googlebot" | grep -v "SISTRIX Crawler" | grep -v "MJ12bot" | wc -l  

\# 637

</p>

cat john-pfeiffer.access | grep "Googlebot" | wc -l \# 105 ,
[https://en.wikipedia.org/wiki/Googlebot][]  

cat john-pfeiffer.access | grep "bingbot" | wc -l \# 96 ,
[http://en.wikipedia.org/wiki/Bingbot][]  

cat john-pfeiffer.access | grep "Baiduspider" | wc -l \# 93  

cat john-pfeiffer.access | grep "SISTRIX Crawler" | wc -l \# 76 ,
[http://crawler.sistrix.net/][]  

cat john-pfeiffer.access | grep "YandexBot" | wc -l \# 64 ,
[http://www.botopedia.org/user-agent-list/search-bots/yandex-bot.html][]  

cat john-pfeiffer.access | grep "Mail.RU\_Bot" | wc -l \# 23 ,
[http://www.webmasterworld.com/search\_engine\_spiders/4520951.htm][],
[http://www.botopedia.org/user-agent-list/search-bots/mailru-bot.html][]  

cat john-pfeiffer.access | grep "MJ12bot" | wc -l \# 12 ,
[http://www.majestic12.co.uk/projects/dsearch/mj12bot.php][]  

cat john-pfeiffer.access | grep "Sogou" | wc -l \# 7 ,
[http://www.botopedia.org/user-agent-list/search-bots/sogou-spider.html][]

</p>

[http://www.incapsula.com/the-incapsula-blog/item/393-know-your-top-10-bots][]

</p>

[http://searchenginewatch.com/article/2067357/Bye-bye-Crawler-Blocking-th...][]  

(Besides the robots.txt you are pretty much left with ban by User-Agent
or IP Address Range.)

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [IT][]
-   [Linux][]

</div>
</p>

  [https://en.wikipedia.org/wiki/Googlebot]: https://en.wikipedia.org/wiki/Googlebot
  [http://en.wikipedia.org/wiki/Bingbot]: http://en.wikipedia.org/wiki/Bingbot
  [http://crawler.sistrix.net/]: http://crawler.sistrix.net/
  [http://www.botopedia.org/user-agent-list/search-bots/yandex-bot.html]:
    http://www.botopedia.org/user-agent-list/search-bots/yandex-bot.html
  [http://www.webmasterworld.com/search\_engine\_spiders/4520951.htm]: http://www.webmasterworld.com/search_engine_spiders/4520951.htm
  [http://www.botopedia.org/user-agent-list/search-bots/mailru-bot.html]:
    http://www.botopedia.org/user-agent-list/search-bots/mailru-bot.html
  [http://www.majestic12.co.uk/projects/dsearch/mj12bot.php]: http://www.majestic12.co.uk/projects/dsearch/mj12bot.php
  [http://www.botopedia.org/user-agent-list/search-bots/sogou-spider.html]:
    http://www.botopedia.org/user-agent-list/search-bots/sogou-spider.html
  [http://www.incapsula.com/the-incapsula-blog/item/393-know-your-top-10-bots]:
    http://www.incapsula.com/the-incapsula-blog/item/393-know-your-top-10-bots
  [http://searchenginewatch.com/article/2067357/Bye-bye-Crawler-Blocking-th...]:
    http://searchenginewatch.com/article/2067357/Bye-bye-Crawler-Blocking-the-Parasites
  [IT]: http://john-pfeiffer.com/category/it
  [Linux]: http://john-pfeiffer.com/category/tags/linux
