<?

    /***********************************************************************
     * dictionary.php
     *
     * Computer Science 50
     * David J. Malan
     *
     * Implements a dictionary.
     **********************************************************************/


    // size of dictionary
    $size = 0;

    // dictionary
    $dictionary = array();


    /*
     * bool
     * check($word)
     *
     * Returns TRUE if word is in dictionary else FALSE.
     */

    function check($word)
    {
        global $dictionary;
        if ($dictionary[strtolower($word)])
            return TRUE;
        else
            return FALSE;
    }


    /*
     * bool
     * load($dict)
     *
     * Loads dict into memory.  Returns TRUE if successful else FALSE.
     */

    function load($dict)
    {
        global $dictionary, $size;
        if (!file_exists($dict) && is_readable($dict))
            return FALSE;
        foreach (file($dict) as $word)
        {
            $dictionary[chop($word)] = TRUE;
            $size++;
        }
        return TRUE;
    }


    /*
     * int
     * size()
     *
     * Returns number of words in dictionary if loaded else 0 if not yet loaded.
     */

    function size()
    {
        global $size;
        return $size;
    }


    /*
     * int
     * unload()
     *
     * Unloads dictionary from memory.  Returns TRUE if successful else FALSE.
     */

    function unload()
    {
        return TRUE;
    }

?>
