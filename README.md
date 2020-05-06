
<p align="center">
    <img src="https://raw.finnwea.com/vector-shields-v2/?firstText=Wiki&secondText=Raider&scale=true" width="475" />
</p>
<p align="center">
    <a href="https://github.com/NorthwaveNL/wikiraider/blob/master/LICENSE.md"><img src="https://raw.finnwea.com/vector-shields-v2/?firstText=License&secondText=MIT" /></a>
    <a href="https://github.com/NorthwaveNL/wikiraider/releases"><img src="https://raw.finnwea.com/vector-shields-v1/?typeKey=SemverVersion&typeValue1=northwavenl&typeValue2=wikiraider&typeValue4=Release&cache=1"></a>
    <a href="https://travis-ci.org/github/NorthwaveNL/wikiraider"><img src="https://raw.finnwea.com/vector-shields-v1/?typeKey=TravisBuildStatus&typeValue1=northwavenl/wikiraider&typeValue2=master&cache=1"></a>
</p>
<p align="center">
    <b>Want to crack passwords faster by using a wordlist that fits your 'target audience'? Use WikiRaider.</b>
    <br/>
    <a href="#goal">Goal</a>
    •
    <a href="#wordlists">Wordlists</a>
    •
    <a href="#parsing">Parsing</a>
    •
    <a href="#cracking">Cracking</a>
    •
    <a href="#limitations">Limitations</a>
    •
    <a href="#issues">Issues</a>
    •
    <a href="#license">License</a>
    <br/>
    <sub>Built with ❤ by the <a href="https://twitter.com/NorthwaveLabs">Northwave</a> Red Team</sub>
    <br/>
</p>
<hr>

## Goal

In the Northwave Red Team we crack password hashes during penetration tests and red team engagements, mostly using [hashcat](https://tools.kali.org/password-attacks/hashcat) and [john-the-ripper](https://tools.kali.org/password-attacks/john). Cracking these hashes based on certain wordlists is generally faster than brute-forcing the entire alphabet of possibilities. As long as the wordlist in use is related to the hashes you are cracking of course. But how do you find wordlists that are related to the passwords hashes you are trying to crack?

**WikiRaider to the rescue!** WikiRaider enables you to generate wordlists based on country specific databases of Wikipedia. This will provide you with not only a list of words in a specific language, it will also provide you with e.g. country specific artists, TV shows, places, etc.

## Wordlists

*Parsing a Wikipedia database takes a while. If you've parsed a database, feel free to contribute by adding it to this list.*

* NL (Dutch) - [download](https://github.com/NorthwaveNL/wikiraider/blob/master/wordlists/nlwiki/nlwiki-2020-05-05.txt)
* ES (Spanish) - [download](https://github.com/NorthwaveNL/wikiraider/blob/master/wordlists/eswiki/eswiki-2020-05-05.txt)

## Parsing

**Listing Wikipedia databases**

Find all databases:

    ./wikiraider.py list

Search (based on language code):

    ./wikiraider.py list -s EN

*If your preferred database is not listed, Wikipedia might be exporting backups. Check the [backup index](https://dumps.wikimedia.org/backup-index.html) to see if any backup exports are running.*

**Parsing a Wikipedia database**

Parse the Dutch Wikipedia database

    ./wikiraider.py parse -u https://dumps.wikimedia.org/nlwiki/20200401

*Parsing a database will take a while and requires quite some processing power and memory. WikiRaider is multi-threaded and for performance it loads all words (as a hashset) into memory.*

## Cracking

**NTLM**

Lets say you want to crack NTLM hashes from a NTDS file. Using your WikiRaider wordlist, you can run the following command on `dump.ntds`. A rule (`OneRuleToRuleThemAll`) is used to forge the words to passwords.

hashcat -m [HASH_MODE](https://hashcat.net/wiki/doku.php?id=hashcat#options) [NTDS_DUMP](https://medium.com/@bondo.mike/extracting-and-cracking-ntds-dit-2b266214f277) [WORDLIST](https://github.com/NorthwaveNL/wikiraider/blob/master/wordlists/nlwiki/nlwiki-2020-05-05.txt) -r [RULESET](https://raw.githubusercontent.com/NotSoSecure/password_cracking_rules/master/OneRuleToRuleThemAll.rule) -vvv

````hashcat -m 1000 dump.ntds -vvv nlwiki-2020-05-05.txt -r OneRuleToRuleThemAll.rule````

## Limitations

Currently only words that comply with the regex `[A-zÀ-ú]+` are gathered. This is due to the fact that I'm not familiar with languages outside of this alphabet space. In a future release of WikiRaider I will try to provide you with options to parse words outside of this alphabet space. If you have a proper solution, feel free to contribute.

## Issues

Issues or new features can be reported via the [GitHub issue tracker](https://github.com/NorthwaveNL/wikiraider/issues). Please make sure your issue or feature has not yet been reported by anyone else before submitting a new one.

## License

Wikiraider is open-sourced software licensed under the [MIT license](https://github.com/NorthwaveNL/wikiraider/blob/develop/LICENSE.md).