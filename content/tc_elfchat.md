Title: ThugCrowd ELF Chat Challenge
Date: 2019-07-27 22:00
Keywords: thugcrowd, ctf, code-challenge

## [Thugcrowd Matrix ELF Chat Challenge Link](https://twitter.com/thugcrowd/status/1153811494838030338), [Mirror](http://archive.is/LFPCc):

As with most challenges which appear to be base64 encoded, I think it's always good to try to decode them first to see if there is anything worthwhile (a message which is encoded) or if it has binary characters. This just gives us a direction to head in.

Standard base64 decoders online don't seem to like the format of this challenge, so we head to a decoder that can handle different types of characters more easily.
```bash
user@box:~$ base64 -d <<< f0VMRki7TyxCbTpkfj7rPAIAPgABAAAABAAAAAEAAAAcAAAAAAAAAAAAAAAAAAAAAQAAAEAAOAABAAIABDwPBQAAAAAEPA8FAAAAAFNIuytFKS0/RC4uU0i7L1gyREQjUjdTSLtSQ2hbY3UvblNIuyxdTi8zYldHU0i7ckFCNjgwJkVTSLs4b0pFXSs8dFNIu0RDMERFIDx+U0gx/+ud
ELFH�O,Bm:d~>�<>@8<<SH�+E)-?D..SH�/X2DD#R7SH�RCh[cu/nSH�,]N/3bWGSH�rAB680&ESH�8oJE]+<tSH�DC0DE <~SH1��p
```

This looks like something we would want to make into a binary file, due to the first few characters being `ELFH`.

Another way to do this without utilizing bash would be to convert the base64 directly to hex online, and try to make a binary instead. I'm a fan of [Cryptii](https://cryptii.com) for quick conversions:
<a href="/includes/static/thugcrowd_elf/2-cryptii-1.jpg" data-lightbox="2-cryptii-1" data-title="cryptii pt 1">
    <img src="/includes/thumbs/thugcrowd_elf/2-cryptii-1.jpg" title="" />
</a>
<a href="/includes/static/thugcrowd_elf/3-cryptii-2.jpg" data-lightbox="3-cryptii-2" data-title="cryptii pt 2">
    <img src="/includes/thumbs/thugcrowd_elf/3-cryptii-2.jpg" title="" />
</a>


Pasting this into a hex editor (Bless or HxD are my choices), we see the same thing we saw in bash:
<a href="/includes/static/thugcrowd_elf/4-hxd.jpg" data-lightbox="4-hxd.jpg" data-title="4-hxd.jpg">
    <img src="/includes/thumbs/thugcrowd_elf/4-hxd.jpg" title="message displayed in hex" />
</a>

To make the determination of what type of file it is without having to rely on guesswork as much, we can use a utility called [Binwalk](https://github.com/ReFirmLabs/binwalk) to try to get a better idea of what we're working with. We need to make a binary from this resultant hex code - we can do this by saving the hex in your hex editor of choice, or you can write it to a file using the `base64 -d` command as shown above, with some additions: 

```bash
base64 -d <<< f0VMRki7TyxCbTpkfj7rPAIAPgABAAAABAAAAAEAAAAcAAAAAAAAAAAAAAAAAAAAAQAAAEAAOAABAAIABDwPBQAAAAAEPA8FAAAAAFNIuytFKS0/RC4uU0i7L1gyREQjUjdTSLtSQ2hbY3UvblNIuyxdTi8zYldHU0i7ckFCNjgwJkVTSLs4b0pFXSs8dFNIu0RDMERFIDx+U0gx/+ud > ~/challenge_bin
```
With this file, we can run binwalk with no arguments other than the file:
```bash
user@box:~$ binwalk challenge_bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
```

This it doesn't look like we are going to get anywhere with binwalk here at least. There are a couple of other ways to learn more information about files, the first one is using the aptly named `file` command:
```bash
user@box:~$ file challenge_bin 
challenge_bin: ELF, unknown class 72
```

From this we figure out what we already knew, which is that it's in ELF format, but not much more. We can verify this by using a [common file signature table](https://www.garykessler.net/library/file_sigs.html), to search for the first few bytes, in this case, `7F 45 4C 46`. On Gary's website, we get this result:
<a href="/includes/static/thugcrowd_elf/5-fst.jpg" data-lightbox="5-fst.jpg" data-title="gary kesslers awesome file signature table">
    <img src="/includes/thumbs/thugcrowd_elf/5-fst.jpg" title="" />
</a>

We can pretty much assume this is a binary ELF without a doubt. Another `obvious` clue was in the ThugCrowd follow up tweet, stating: [Yes, it's a binary. No, binary analysis tools will not work here.](https://twitter.com/thugcrowd/status/1153811747045691392), but it's always good to be sure.

We need to modify the binary to be executable, using `chmod +x ~/challenge_bin`, and we can execute it with `~/challenge_bin`. Unfortunately, when we do this we get no result, so from here, I'll usually try to feed the binary some input to see if I can get a different result. Again, unfortunately, passing the file any arguments (`-h, -i, --input, etc`) results in the same outcome, which is that there is no result. 

One of the good things about this file is that it's very small, so it's easy to run and parse the output from the Linux `strings` command on the binary:
```bash
user@box:~$ strings challenge_bin 
ELFH
O,Bm:d~>
+E)-?D..SH
/X2DD#R7SH
RCh[cu/nSH
,]N/3bWGSH
rAB680&ESH
8oJE]+<tSH
DC0DE <~SH1
```
This output is very interesting, and more reminiscent of a code than something we should be executing - the main part that should point us in that direction is the `SH` termination on every line, and the `DC0DE` at the very end. If we look at the string following `DC0De`, `<~SH1`, along with the first non-ELFH line, `O,Bm:d~>`, this is somewhat of a clue, although not quite an obvious one. 

A few weeks prior to this, [ThugCrowd tweeted](https://twitter.com/thugcrowd/status/1149142932487905281)/[mirror](http://archive.is/ZjnCE) an encrypted message forwarded from the DollarVPNClub Tactical Datacenter Ops Commander, directed at the current VPN regime: ```<~6=h9<F`M%9<,WmIEbTE,+B`W*EZe/$@;L%"DIkF~>```. This message format was unfamiliar to me at the time, but a Google search guess gave me a pretty good idea of how to decode it:

<a href="/includes/static/thugcrowd_elf/6-character-search.jpg" data-lightbox="6-character-search.jpg" data-title="character search">
    <img src="/includes/thumbs/thugcrowd_elf/6-character-search.jpg" title="" />
</a>

Being able to identify the ascii85 encoding scheme leads us back to the original problem, since it certainly seems possible that this message could be encoded as such. Doing some trial and error with ordering the output string properly doesn't really give us anything, but there are some assumptions that we can make with this message. 

- We can probably exclude the `ELFH` header, as this was probably added to point the solver in the wrong direction.
- Due to the fact that `SH` appears on every line but the decode fails when including it, we can probably remove the string from each line. 
- `DC0DE` was probably added to point the solver in the right direction, and is not actually part of the message. 

That leaves us with a message like this: 
```bash
O,Bm:d~>
+E)-?D..
/X2DD#R7
RCh[cu/n
,]N/3bWG
rAB680&E
8oJE]+<t
<~1
```

We know from the original tactical-encrypted VPN message that ascii85 encoded strings aren't decoded with the `<~ ~>` characters wrapping the string (at least, not on Cryptii), so we can remove these as well to get something like this: 

```bash
O,Bm:d
+E)-?D..
/X2DD#R7
RCh[cu/n
,]N/3bWG
rAB680&E
8oJE]+<t
1
```

Pasting this into Cryptii gives us an encoding error: `Unexpected continuation byte at 0x0`. Deleting the first character doesn't help, and trying to make the decoder happy by removing more characters doesn't help either. The clue that pointed me in the right direction was the bottom, unstripped section, and the top unstripped sections: 

```bash
O,Bm:d~>
---snip---
DC0DE <~SH1
```

The opening and closing terminations on this message are the key - wrapping the message around bottom to top would leave us with: 
```bash
<~1O,Bm:d~>
```

Which is a very short message, leaving most of the text unused. As you might expect, this gives us nothing, but going from bottom to top through the message, reversing it, gives us this: 
```bash
1
8oJE]+<t
rAB680&E
,]N/3bWG
RCh[cu/n
/X2DD#R7
+E)-?D..
O,Bm:d
```

Pasting this into Cryptii gives us a continuation error, but luckily this time removing the invalid character gives us the answer, which comes from this ascii85 encoded message:
```bash

8oJE]+<t
rAB680&E
,]N/3bWG
RCh[cu/n
/X2DD#R7
+E)-?D..
O,Bm:d
```

<a href="/includes/static/thugcrowd_elf/7-cryptii-error.jpg" data-lightbox="7-cryptii-error.jpg" data-title="cryptii error">
    <img src="/includes/thumbs/thugcrowd_elf/7-cryptii-error.jpg" title="" />
</a>
<a href="/includes/static/thugcrowd_elf/8-answer.jpg" data-lightbox="8-answer.jpg" data-title="challenge result">
    <img src="/includes/thumbs/thugcrowd_elf/8-answer.jpg" title="8-answer.jpg" />
</a>


This writeup is sponsored by and dedicated to DollarVPNClub, without their help and faithful network of cryptographic enhancements I would never have been able to complete this challenge. `#FREEDVC`
<a href="/includes/static/thugcrowd_elf/dvc.jpg" data-lightbox="8-answer.jpg" data-title="FREEDVC">
    <img src="/includes/thumbs/thugcrowd_elf/dvc.jpg" title="dvc.jpg" />
</a>