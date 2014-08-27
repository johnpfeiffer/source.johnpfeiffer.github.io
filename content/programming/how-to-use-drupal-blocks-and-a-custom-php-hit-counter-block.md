Title: How-to-use-Drupal-Blocks-and-a-custom-php-hit-counter-block
Date: 2010-01-06 14:15
Tags: drupal

Blocks control the layout of the pages, i.e. a "footer" block appears at the bottom of each page.

Each theme might have a different layout (and blocks available), and of course you can add your own custom blocks.

Using the WebUI you can modify the look of the site's layout pretty quickly:

`Administer -> Blocks`

Drag and drop the "Powered by Drupal" option from **FOOTER** into **DISABLED**.


ADVANCED: a custom php blog (maybe dangerous)

drupal-6-custom-php-block

admin/build/block

create a new block

in the body (plain text!) insert (copy paste?) your code

Input Format = PHP code 
 (Core Module -> Optional -> PHP Filter must be enabled)
 

`Home -> Administer -> Site Configuration -> Input Format`
admin/settings/filters

`PHP code -> configure `
(the super user System Administrator ALREADY has this filter,
the above only allows you to add other users which is dangerous!)


IF HITFILE EXISTS:     read current count
IF NOT, return error

    <?php
    $filename = "hit-counter.txt" ;
    $file_pointer = fopen( $filename , 'a+' );    //r+ = read + write, start at beginning  
    
    if ( is_writable( $filename )) 
        { 
            $buffer = "test123\ntest456\ntest789";
            fwrite( $file_pointer , $buffer ); 
        } 
    fclose( $file_pointer  );
    


    <?php
    $filename = "hit-counter.txt" ;
    $file_pointer = fopen( $filename , 'r' );    //r = read, starts at beginning  
    if( $file_pointer == NULL ) {    die( "error accessing file" );    }
    
    fseek( $file_pointer , 0 );
    $filecontents = file_get_contents( $filename );
    $filecontents++;   //the file only contains an integer
    print $filecontents;
    fclose( $file_pointer  );
    
    $file_pointer = fopen( $filename , 'w' );    //r = read, starts at beginning  
    if( $file_pointer == NULL ) {    die( "error accessing file" );    }
    
    if ( is_writable( $filename ) ) 
    {    fseek( $file_pointer , 0 );    
          fwrite( $file_pointer , $filecontents ); 
    } 
    
    fclose( $file_pointer  );
    
    
    ?>
    