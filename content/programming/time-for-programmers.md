Title: Time for Programmers
Date: 2011-06-05 21:20
Tags: time, epoch, java, python

[TOC]

Computer (Unix / POSIX) time starts 1970-01-01 00:00:00 UTC <http://en.wikipedia.org/wiki/Unix_time>

An excellent article about time, especially for java programmers, <http://www.odi.ch/prog/design/datetime.php>

Inside the "river of time" measurement is absurd, but Physicists have spacetime, 

> "...cycles of radiation corresponding to the transition between the two electron spin energy levels of the ground state of the 133 Caesium atom".


24 hours, UTC and NTP can synchronize the world (especially servers!), but days, calendars, time zones, weeks, etc. will drive you crazy, so think carefully and use the utility libraries!

### Java datetime timezone example

    :::java
    import java.util.Date;
    import java.util.Calendar;
    import java.util.TimeZone;
    import java.text.DateFormat;
    import java.text.SimpleDateFormat;
    
    // not thread-safe
    public static SimpleDateFormat dfm = new SimpleDateFormat("yyyy-MM-dd");
    
    DateFormat dfm = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    dfm.setTimeZone(TimeZone.getTimeZone("Europe/Zurich"));
    Date a = dfm.parse("2007-02-26 20:15:00");



### Yesterday in python 

    from datetime import date
    yesterday = date.fromordinal(date.today().toordinal()-1).strftime('%Y-%m-%d')

### dateutil and helper functions

    import dateutil.parser		
    # http://labix.org/python-dateutil  (for google app engine put the source directory at the root project level)
	
    myd = 'Thu, 11 Jul 2013 05:01:21 -0700'
    datetime_obj = dateutil.parser.parse( myd )

    def seconds_to_datetime( t ):
	    return datetime.datetime.fromtimestamp( int( t ) )


    def datetime_string_to_seconds( date_str ):
        datetime_obj = dateutil.parser.parse( date_str)  # Thu, 11 Jul 2013 05:01:21 -0700
        return Utility.datetime_to_seconds( datetime_obj )


    def datetime_to_seconds( datetime_obj ):
	    return int( time.mktime( datetime_obj.timetuple() ) )


### pytz for timezones

    import pytz	# sometimes requires complex installation, easy_install --upgrade pytz
    from datetime import datetime
    print datetime.datetime.now()

    utc = pytz.timezone("UTC")
    print utc

    date_utc = datetime.datetime.now( pytz.timezone( "UTC" ) ).strftime( "%Y-%m-%d" )
    print date_utc

### time and datetime tuples

    import time
    mytime = time.strptime("Mon Apr 07 13:05:55 PDT 2014", "%a %b %d %H:%M:%S %Z %Y")
    # time.struct_time(tm_year=2014, tm_mon=4, tm_mday=7, tm_hour=13, tm_min=5, tm_sec=55, tm_wday=0, tm_yday=97, tm_isdst=1)
    time.mktime(mytime)  # 1396901155.0
    print time.strftime("%Y-%m-%d %H:%M:%S", mytime)  # 2014-04-07 13:05:55
    
    time_tuple = (2008, 11, 12, 13, 51, 18, 2, 317, 0)
    print time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)  # 2008-11-10 17:53:59
    
    import datetime
    date_object = datetime.datetime(2008, 11, 10, 17, 53, 59)
    print date_object.strftime("%Y-%m-%d %H:%M:%S")  # 2008-11-10 17:53:59
    
    timestamp = 1226527167.595983
    print repr(  datetime.fromtimestamp( timestamp ) )  # repr prints with limits on sizes of objects
    
    import calendar
    time_tuple_utc = (2008, 11, 12, 13, 59, 27, 2, 317, 0)	# time tuple in utc time to timestamp
    timestamp_utc = calendar.timegm(time_tuple_utc)
    print repr(timestamp_utc)
    

    #-------------------------------------------------
    time_tuple = (2008, 11, 12, 13, 51, 18, 2, 317, 0)
    datetime_object = datetime(*time_tuple[0:6])
    print repr(datetime_object)
    
    date_string = "2008-11-10 17:53:59"
    datetime_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    print repr(datetime_object)
    
    timestamp = 1226527167.595983
    datetime_object = datetime.fromtimestamp(timestamp)  # local time
    print repr(datetime_object)
    
    timestamp = 1226527167.595983
    datetime_object = datetime.utcfromtimestamp(timestamp)
    print repr(datetime_object)
    
    #-------------------------------------------------
    # conversions to time tuples
    
    datetime_object = datetime(2008, 11, 10, 17, 53, 59)
    time_tuple = datetime_object.timetuple()
    print repr(time_tuple)
    
    date_str = "2008-11-10 17:53:59"
    time_tuple = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    print repr(time_tuple)
    
    timestamp = 1226527167.595983
    local_time_tuple = time.localtime(timestamp)  # local time
    print repr(local_time_tuple)
    utc_time_tuple = time.gmtime(timestamp)  # UTC
    print repr(utc_time_tuple)
    
    
    #-------------------------------------------------
    # conversions to timestamps
    
    # time tuple in local time to timestamp
    time_tuple = (2008, 11, 12, 13, 59, 27, 2, 317, 0)
    timestamp = time.mktime(time_tuple)
    print repr(timestamp)
    
    # time tuple in utc time to timestamp
    time_tuple_utc = (2008, 11, 12, 13, 59, 27, 2, 317, 0)
    timestamp_utc = calendar.timegm(time_tuple_utc)
    print repr(timestamp_utc)
    
    #-------------------------------------------------
    # results
    #-------------------------------------------------
    # 2008-11-10 17:53:59
    # 2008-11-12 13:51:18
    # datetime.datetime(2008, 11, 12, 13, 51, 18)
    # datetime.datetime(2008, 11, 10, 17, 53, 59)
    # datetime.datetime(2008, 11, 12, 13, 59, 27, 595983)
    # datetime.datetime(2008, 11, 12, 21, 59, 27, 595983)
    # (2008, 11, 10, 17, 53, 59, 0, 315, -1)
    # (2008, 11, 10, 17, 53, 59, 0, 315, -1)
    # (2008, 11, 12, 21, 59, 27, 2, 317, 0)
    # (2008, 11, 12, 13, 59, 27, 2, 317, 0)
    # 1226527167.0
    # 1226498367
    