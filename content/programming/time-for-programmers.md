Title: Time for Programmers
Date: 2011-06-05 21:20
Author: John Pfeiffer
Slug: time-for-programmers

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Computer (Unix / POSIX) time starts 1970-01-01 00:00:00 UTC

</p>

An excellent article about time, especially for java programmers,
[http://www.odi.ch/prog/design/datetime.php][]

</p>

Inside the "river of time" measurement is absurd, but Physicists have
spacetime, "...cycles of radiation corresponding to the transition
between the two electron spin energy levels of the ground state of the
133 Caesium atom".

</p>

24 hours, UTC and NTP can synchronize the world (especially servers!),
but days, calendars, time zones, weeks, etc. will drive you crazy, so
think carefully and use the utility libraries!

</p>

import java.util.Date;  

import java.util.Calendar;  

import java.util.TimeZone;  

import java.text.DateFormat;  

import java.text.SimpleDateFormat;

</p>

public static SimpleDateFormat dfm = new SimpleDateFormat("yyyy-MM-dd");
// not thread-safe

</p>

DateFormat dfm = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");  

dfm.setTimeZone(TimeZone.getTimeZone("Europe/Zurich"));  

Date a = dfm.parse("2007-02-26 20:15:00");  

...

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Programming][]

</div>
</p>

  [http://www.odi.ch/prog/design/datetime.php]: http://www.odi.ch/prog/design/datetime.php
  [Programming]: http://john-pfeiffer.com/category/tags/programming
