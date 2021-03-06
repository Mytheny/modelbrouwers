<?php
    // common variables to be included in templates
    // symlink the templates and this file so it can be included
    // in the templates
    $settings = array(
        'MEDIA_URL'         => '/media/',
        'STATIC_URL'        => '/static/',
        'HONEYPOT_URL'      => '/scratchy.php',
    );
    
    // options: 'achter' or 'voor' in the filename. voor <==> highlighted image
    // use this for the active page
    // CAUTION: due to the preg_match searching, place the most specific urls LAST
    $nav = array(
        'home'          => array(
                            'alt' => 'Ga naar de startpagina!',
                            'url' => '/',
                            ),
        'forum'         => array(
                            'alt' => 'Ga naar het forum!',
                            'url' => '/phpBB3/',
                            ),
        'shop'          => array(
                            'alt' => 'Ga naar de shop!',
                            'url' => '/winkel/',
                            ),
        'albums'        => array(
                            'alt' => 'Ga naar de albums!',
                            'url' => '/albums/',
                            ),
        'kitreviews'    => array(
                            'alt' => 'Ga naar de kitreviews!',
                            'url' => '/kitreviews/',
                            ),
    );
    
    $best_match = '';
    foreach($nav as $k => $tab)
    {
        $uri = $tab['url'];
        $request_uri = $_SERVER['REQUEST_URI'];
        
        $pattern = "%^".$uri.'%';
        preg_match($pattern, $request_uri, $m);
        if (count($m) > 0){
            if ($uri != '/' || ($request_uri == '/index.php')){
                $best_match = $k;
            }
        }
    }
    
    // hightlightsettings doen
    if ($best_match){
        $nav[$best_match]['classes'] = 'nav active';
        $nav[$best_match]['title'] = 'Je bent hier!';
    }
?>
