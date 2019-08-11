Title: ThugCrowd XOR Chat Challenge
Date: 2018 04 04 18:00
Keywords: thugcrowd, ctf, chat challenge, xor

## [ThugCrowd XOR Chat Challenge](https://twitter.com/thugcrowd/status/1113138128754225158), [Mirror](http://archive.fo/6GUyS):

```
seven days until discord xors itself \x1b\x11\x02\x15\x1d\x1aKN\r\x1bU\x12\r\x06\x06\x1bDJ\n\x1c\x0e@\x11\x0cA\x14@\x11\x1bA\x1dZ\x1b\x11\x01\n 
```

This chat challenge was interesting for me, as it was my first attempt XOR cipher CTF. As per [Wikipedia](https://en.wikipedia.org/wiki/XOR_cipher), `the simple XOR cipher is a type of additive cipher`. Using a message and a key, you can generate an message by XORing the two, or one with a repeating key. 

Initially when learning about XOR ciphers, the main information I found was regarding repeating keys (the contents of which are truncated at the end of the input message), such as this: 
```
Message: MESSAGE TO ENCRYPT
Key: ENCRYPTIONKEY

Since len(Message) > len(Key), the key is repeated (pipe| denotes the start of the repeat):
M  E  S  S  A  G  E     T  O     E  N  C  R  Y  P  T
4d 45 53 53 41 47 45 20 54 4f 20 45 4e 43 52 59 50 54
45 4e 43 52 59 50 54 49 4f 4e 4b 45 59|45 4e 43 52 59
E  N  C  R  Y  P  T  I  O  N  K  E  Y |E  N  C  R  Y 

To XOR the two strings in Python, we can use: hex(int(message, 16) ^ int(key, 16))
Message: 4d 45 53 53 41 47 45 20 54 4f 20 45 4e 43 52 59 50 54
Key:     45 4e 43 52 59 50 54 49 4f 4e 4b 45 59|45 4e 43 52 59
XOR'd:   08 0b 10 01 18 17 11 69 1b 01 6b 00 17 06 1c 1a 02 0d
```

In order to solve this challenge, I wanted a way to parse and interpret a lot of data at once, since the key wasn't immediately clear to me, so I decided to use Microsoft Excel to allow me to get a better overview and to be able to quickly play with keys. I ran through a few iterations of formats (all pretty close to the end result), but the final sheet was formatted as follows: 

``` 
Secret: row contains a repeating secret which I manually entered to try to intelligently bruteforce the result

String: each individual value in the tweet went here, \x1b, \x11, \x02, etc. manually entered 

Hex: the hex representation of the "String" row, =REPLACE(LEFT(CELL,4), 1, 1, "0"), this converts \x1b->0x1b

Hex stripped: stripped 0x from string, to get the plain hex value, this could have been done in one formula but I decided to do it in two, =RIGHT(CELL, 2) converts 0x1b->1b

HexToDec: self explanatory, converts hexadecimal to decimal, =HEX2DEC() 0x1b->27

SecretToDec: converts the current secret character to decimal format, using =CODE() converts "s"->115

XORtoDec: performs a bitwise XOR of two numbers, =BITXOR(CELL1,CELL2) turns 27 XOR 115 -> 104

Result: uses the excel =CHAR() to turn a decimal value into a character, 104->"h"
```

Using this as my code breaking tool, I was easily able to test keys repeatedly, filling across the columns and seeing the result instantly. The problem I was left with was "what is the key?". Attached to the tweet is a picture of the well scene from the Ring, so I started off with a few repeating keys, `WELL`, `RING`, and `SEVEN DAYS`. `Well` being from the picture, `Ring` being the name of the movie, and `seven` being a large part of the plot (seven days to die).

<a href="/includes/static/thugcrowd_xor/1-excel-1.jpg" data-lightbox="1-excel-1" data-title="excel layout for initial testing">
    <img src="/includes/thumbs/thugcrowd_xor/1-excel-1.jpg" title="excel layout for initial testing" />
</a>

`Ring` and `well` didn't turn up anything worthwhile, but `seven` gave me something interesting, which was `https:`. This seemed to indicate that the message was actually a URL, so I tried seven as a repeating secret, but that was a dead end as well. My next try was `seven days`, which again gave me another hint `https://thu` (thugcrowd.com?), and coincidentally, this is also the start of the tweet: `seven days until discord xors itself`. I still had some formatting issues and wrong ideas about the layout of the hex message, which you can see below:

<a href="/includes/static/thugcrowd_xor/2-excel-1.jpg" data-lightbox="2-excel-1" data-title="seven days">
    <img src="/includes/thumbs/thugcrowd_xor/2-excel-1.jpg" title="seven days " />
</a>

Our message seemed to line up well also:

``` 
Message: 1b 11 02 15 1d 1a K N \r 1b U 12 \r 06 06 1b D J \n 1c 0e @ 11 0c A 14 @ 11 1b A 1d Z 1b 11 01 \n 
Key:     s  e  v  e  n     d a y  s    u  n  t  i  l    d i  s  c  o r  d    x  o r  s    i  t s  e  l  f  
```

<a href="/includes/static/thugcrowd_xor/3-excel-final.jpg" data-lightbox="3-excel-final.jpg" data-title="excel final message with url">
    <img src="/includes/thumbs/thugcrowd_xor/3-excel-final.jpg" title="excel final message with url" />
</a>

Okay, so now we have what is probably the key, so going to the website, `https://thugcrowd.com/chal/chat.html`, gives us a picture of Haunter, and a good remix of Hotline Bling playing in the background, but this doesn't seem like the answer. Inspecting the source gives us something else to work with, and selecting all shows it is actually a haunted string. 

<a href="/includes/static/thugcrowd_xor/4-haunter-1.jpg" data-lightbox="4-haunter-1.jpg" data-title="haunter ascii art">
    <img src="/includes/thumbs/thugcrowd_xor/4-haunter-1.jpg" title="4-haunter-1.jpg" />
</a>

<a href="/includes/static/thugcrowd_xor/5-source-1.jpg" data-lightbox="5-source-1.jpg" data-title="spooky hidden text">
    <img src="/includes/thumbs/thugcrowd_xor/5-source-1.jpg" title="5-source-1.jpg" />
</a>

<a href="/includes/static/thugcrowd_xor/6-haunted-1.jpg" data-lightbox="6-haunted-1.jpg" data-title="very spooky haunted text ">
    <img src="/includes/thumbs/thugcrowd_xor/6-haunted-1.jpg" title="6-haunted-1.jpg" />
</a>

This looks like more hex, so let's try to make a binary with Bless or HxD and run `file` to see what we're working with:
```
user@box:~/tc_xor$ file haunter 
haunter: Zip archive data, at least v?[0x314] to extract
```

And binwalk: 
```
user@box:~/tc_xor$ binwalk haunter 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, at least v2.0 to extract, compressed size: 532, uncompressed size: 3108, name: haunt.txt
662           0x296           End of Zip archive, footer length: 22
```

It's safe to assume we're dealing with a zip, so using the standard Linux archive manager, we see there's one file: 
<a href="/includes/static/thugcrowd_xor/7-onefile-1.jpg" data-lightbox="7-onefile-1.jpg" data-title="only one file">
    <img src="/includes/thumbs/thugcrowd_xor/7-onefile-1.jpg" title="7-onefile-1.jpg" />
</a>

With the contents of: 
```
4pSM4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA
4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSQ
CuKUguKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgICAgIOKW
iOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKUggrilILilojiloji
lojilojilojilojilojilojilojilojilojiloggICDilojilojilojilojilojilogg4paI4paI
4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4pSCCuKUguKWiOKWiOKWiOKWiOKW
iOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCDiloggIOKWiCAgIOKWiCDilojilojilojilojiloji
lojilojilojilojilojilojilojilojilIIK4pSC4paI4paI4paI4paI4paI4paI4paI4paI4paI
4paI4paI4paI4paIICDilojilogg4paI4paI4paIICDilojilojilojilojilojilojilojiloji
lojilojilojilojilojilIIK4pSC4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI
ICDilojilojilojilojilojilojilojiloggIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKW
iOKWiOKWiOKUggrilILilojilojilojilojilojilojilojilojilojilojilogg4paIIOKWiOKW
kuKWiOKWiOKWiOKWiOKWkuKWiCDilogg4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI
4pSCCuKUguKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCDilojilojilojilogg4paS
4paSIOKWiOKWiOKWiOKWiCDilojilojilojilojilojilojilojilojilojilojilojilIIK4pSC
4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paIIOKWiOKWkuKWiOKWiCDilojilogg4paI
4paI4paS4paIIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKUggrilILilojiloji
lojilojilojilojilojilojilojilojilojiloggIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAg
4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4pSCCuKUguKWiOKWiOKWiOKWiOKW
iOKWiOKWiOKWiOKWiOKWiOKWiCAg4paIIOKWiOKWiOKWkuKWkuKWiOKWiCDiloggIOKWiOKWiOKW
iOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKUggrilILilojilojilojilojilojilojilojiloji
lojilogg4paI4paIIOKWiCAgICAgIOKWiCDilojilogg4paI4paI4paI4paI4paI4paI4paI4paI
4paI4paI4pSCCuKUguKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCDilojilogg4paI4paI
ICAgIOKWiOKWiCDilojilogg4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4pSCCuKUguKW
iOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgIOKWiOKWiCDilpLilpIg4paI4paIICAg
4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4pSCCuKUguKWiOKWiOKWiOKWiOKWiOKW
iOKWiOKWiOKWiOKWiOKWiOKWiCDilojilojiloggICAg4paI4paI4paIIOKWiOKWiOKWiOKWiOKW
iOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKUggrilILilojilojilojilojilojilojilojilojiloji
lojilojilojiloggICAgICAgICAg4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI4paI
4paI4pSCCuKUguKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKWiCAgICAg4paI4paI
ICAgICDilojilojilojilojilojilojilojilojilojilojilojilojilIIK4pSCICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAg4pSCCuKUgllvdSBjYW4gY2hvb3NlIHdoZXJlIHlv
dSB3YW50IHRvIGdvIeKUggrilIIgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICDi
lIIK4pSCICAgICBXaWxsIHlvdSBlbnRlciB0aGUgTWF0cml4PyAgICAg4pSCCuKUgiAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKUggrilIIgIEkzZGxiR052YldVNmFHOTBiR2x1
WlM1aWJHbHVMbWRuICDilIIK4pSCICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
4pSCCuKUgiAgICAgT3IgY29udGludWUgd2l0aCBEaXNjb3JkPyAgICAgIOKUggrilIIgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICDilIIK4pSCYUhSMGNITTZMeTlrYVhOamIzSmtM
bWRuTHpWU1JGTkVWbUU94pSCCuKUlOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKU
gOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKU
gOKUgOKUgOKUgOKUgOKUgOKUmAo=
```

Which to me seems like a `base64` encoded string. A couple indicators are the repeated `CAgI`, and the terminating `=`. Let's see what it says: 

```
user@box:~/tc_xor$ base64 -d haunt.txt 
┌────────────────────────────────────┐
│███████████████      ███████████████│
│████████████   ██████ ██████████████│
│█████████████ █  █   █ █████████████│
│█████████████  ██ ███  █████████████│
│████████████  ████████  ████████████│
│███████████ █ █▒████▒█ █ ███████████│
│███████████ ████ ▒▒ ████ ███████████│
│███████████ █▒██ ██ ██▒█ ███████████│
│████████████  ████████  ████████████│
│███████████  █ ██▒▒██ █  ███████████│
│██████████ ██ █      █ ██ ██████████│
│██████████ ██ ██    ██ ██ ██████████│
│███████████   ██ ▒▒ ██   ███████████│
│████████████ ███    ███ ████████████│
│█████████████          █████████████│
│████████████     ██     ████████████│
│                                    │
│You can choose where you want to go!│
│                                    │
│     Will you enter the Matrix?     │
│                                    │
│  I3dlbGNvbWU6aG90bGluZS5ibGluLmdn  │
│                                    │
│     Or continue with Discord?      │
│                                    │
│aHR0cHM6Ly9kaXNjb3JkLmdnLzVSRFNEVmE=│
└────────────────────────────────────┘
```

More `base64`: 

```
user@box:~/tc_xor$ base64 -d <<< I3dlbGNvbWU6aG90bGluZS5ibGluLmdn
#welcome:hotline.blin.gg
```


```
user@box:~/tc_xor$ base64 -d <<< aHR0cHM6Ly9kaXNjb3JkLmdnLzVSRFNEVmE=
https://discord.gg/5RDSDVa
```