Title: Self configuration tests for scalability
Date: 2012-03-12 02:42
Tags: java, perl, TDD

[TOC]

Goal: Customers (Users = system admins) able to self verify configuration.

The more a user can self verify with software, the less support required per customer deployment.

I used the Java API to quickly prototype a solution and exported a runnable .jar file...

<https://code.google.com/p/atmos-java/>

### Java source code for a configuration validation

    :::java
    import com.emc.esu.api.EsuApi;
    import com.emc.esu.api.rest.EsuRestApi;
    import com.emc.esu.api.EsuException;
    import com.emc.esu.api.ObjectId;
    import com.emc.esu.api.ObjectInfo;
    import org.apache.log4j.Level;
    import org.apache.log4j.Logger;
    import org.apache.log4j.ConsoleAppender;
    import org.apache.log4j.PatternLayout;
    
    public class AtmosConnect
    {
        static Logger rootLogger = Logger.getRootLogger();
        public static void main( String[] args )
        {
            if( !rootLogger.getAllAppenders().hasMoreElements() )
            {	rootLogger.setLevel( Level.INFO );
                rootLogger.addAppender( new ConsoleAppender( new PatternLayout(PatternLayout.TTCC_CONVERSION_PATTERN ) ) );
                rootLogger.info("Entering application");
            }
    
            if( args.length != 4 )
            {	System.out.println( args.length + " does not equal the 4 required arguments.");
                System.out.println( "version 0.1: java -jar AtmosConnect.jar HOST PORT SUBTENANTID/UID SECRETKEY" );
                System.exit( 1 );
            }
    
            String HOST = args[0];
            int PORT = Integer.parseInt( args[1] );
            String FULLTOKENID = args[2];
            String SECRETKEY = args[3];
            
            displayConnectionCredentials( HOST , PORT , FULLTOKENID , SECRETKEY );
            EsuApi myEsuAPI = null;
            try{    	myEsuAPI = new EsuRestApi( HOST, PORT, FULLTOKENID, SECRETKEY );
            }catch( EsuException e )
            {	System.out.println( "EsuRestApi Constructor failed.");
                System.out.println( e.getMessage() );
                e.printStackTrace();
            }
            
            ObjectId myObjectId = null;
            myObjectId = createAtmosObject( myObjectId , myEsuAPI );
            displayAtmosObject( myObjectId , myEsuAPI );
            deleteAtmosObject( myObjectId , myEsuAPI );
            
            rootLogger.info("Application Successful");
        } // end main()
            
        private static void displayConnectionCredentials( String HOST , int PORT , String FULLTOKENID , String SECRETKEY )
        {
            System.out.println( "Connecting to Host: " + HOST );
            System.out.println( "Connecting on Port: " + PORT );
            System.out.println( "Full Token ID: " + FULLTOKENID );
            System.out.println( "Secret Key: **************" );
            //System.out.println( "Secret Key: " + SECRETKEY );
        }
            
        private static ObjectId createAtmosObject( ObjectId myObjectId , EsuApi myEsuAPI )
        {
            try
            {   myObjectId = myEsuAPI.createObject( null, null,	null,"application/octet-stream");
                System.out.println( "Created object: " + myObjectId.toString() );
            } catch( Exception e )
            {
                System.out.println("Create Object failed.");
                System.out.println( e );
                //e.printStackTrace();
                // JUnit Tests: Invalid Host, Port, SubtenantID, UID, Shared Secret, etc.
            }
            return myObjectId;
        }
            
        private static void displayAtmosObject( ObjectId myObjectId , EsuApi myEsuAPI )
        {   ObjectInfo myObjectInfo = null;
            myObjectInfo = myEsuAPI.getObjectInfo( myObjectId );
            //System.out.println( "ObjectInfo: " + myObjectInfo.toString() );
            //System.out.println( "ObjectInfo as XML: " + myObjectInfo.getRawXml() );
        }
            
        private static void deleteAtmosObject( ObjectId myObjectId , EsuApi myEsuAPI )
        {
            try
            {   
                System.out.println( "Trying to delete Server Object: " + myObjectId.toString() );
                myEsuAPI.deleteObject( myObjectId );
                System.out.println("Test Object deleted on Server: " + myObjectId.toString() );
            } catch(Exception e)
            {	System.out.println("Delete Object " + myObjectId.toString() + " failed " + e);
                //e.printStackTrace();
            }
        }
    } // end class
    
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

### Verify the bash commands

Verify bash commands that will help extract the configuration:  

    /bin/grep -i 'emcIpAddress=' /var/lib/tomcat6/webapps/storagegateway/WEB-INF/app.properties | cut -f 2 -d '='


### Modify the perl console menu script

    start on stopped rc RUNLEVEL=[2345]  
    stop on runlevel [!2345]

    respawn  

    exec /sbin/getty -n -l /etc/init.d/CONSOLEMENU.pl 38400 tty1



`sudo vi /etc/init.d/CONSOLEMENU.pl`

    :::perl
    sub testatmosconnect()
    {
        system("clear");
        my $sourcefilename = "/var/lib/tomcat6/webapps/storagegateway/WEB-INF/app.properties";
        my $applicationfilename = "/var/lib/tomcat6/oxygen-storagegateway/atmosconnect.jar";
        
        if( (-e $sourcefilename) and (-e $applicationfilename) )
        {
            my $emcipaddress = qx( /bin/grep -i 'emcIpAddress=' $sourcefilename | cut -f 2 -d '=' );
            chomp( $emcipaddress );
            my $emcportnumber = qx( /bin/grep -i 'emcPortNumber=' $sourcefilename | cut -f 2 -d '=' );
            chomp( $emcportnumber );
            my $emcuid = qx( /bin/grep -i 'emcUid=' $sourcefilename | cut -f 2 -d '=' );
            chomp( $emcuid );
            my $emcsharedsecret = qx( /bin/grep -i 'emcSharedSecret=' $sourcefilename | cut -f 2 -d '=' );
            chomp( $emcsharedsecret );
        
            my @status = qx( /usr/bin/java -jar $applicationfilename $emcipaddress $emcportnumber $emcuid $emcsharedsecret );
        
            print "@status\n";
        }else
        {	print "$sourcefilename or $applicationfilename does not exist.\n";
        }
    } # end atmosconnect()
    

### Goal Achieved

A user can self test if they've misconfigured the VM or there's  missing conf files/app, etc. SUCCESS!

Next steps: further unit and system tests, debug, refactor

