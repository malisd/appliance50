<?

    /**
     * quote3.php
     *
     * Outputs price, low, and high of given symbol as JSON.
     *
     * Computer Science 50
     * David J. Malan
     */

    // try to get quote
    $quote = array();
    $handle = @fopen("http://download.finance.yahoo.com/d/quotes.csv?s={$_GET["symbol"]}&f=e1l1hg", "r");
    if ($handle !== FALSE)
    {
        $data = fgetcsv($handle);
        if ($data !== FALSE && $data[0] == "N/A")
        {
            $quote["price"] = $data[1];
            $quote["high"] = $data[2];
            $quote["low"] = $data[3];
        }
        fclose($handle);
    }
    header("Content-type: application/json");
    print(json_encode($quote));
?>
