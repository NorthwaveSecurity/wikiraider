# Wikipedia Wordlists

Wordlists based on the Wikipedia databases of certain countries. These wordlists can be used for cracking password hashes using tools such as [hashcat](https://tools.kali.org/password-attacks/hashcat), [john-the-ripper](https://tools.kali.org/password-attacks/john) or any other tool you wish to use.

### Parsed databases

* NL (dutch) - [download](https://github.com/tijme/wordlists/raw/master/nlwiki-2019-03-25.txt)

### Example usage

**NTLM**

hashcat -m [HASH_MODE](https://hashcat.net/wiki/doku.php?id=hashcat) [NTDS_DUMP](https://medium.com/@bondo.mike/extracting-and-cracking-ntds-dit-2b266214f277) [WORDLIST](https://raw.githubusercontent.com/tijme/wordlists/master/nlwiki-2019-03-25.txt) -r [RULESET](https://raw.githubusercontent.com/NotSoSecure/password_cracking_rules/master/OneRuleToRuleThemAll.rule) -vvv

````hashcat -m 1000 dump.ntds -vvv ./nlwiki-2019-03-25.txt -r OneRuleToRuleThemAll.rule````

### Parsing databases

I will upload a Python script that is able to convert Wikipedia databases to wordlists soon.
