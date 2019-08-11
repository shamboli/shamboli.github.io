Title: ThugCrowd DEFCON Badge Challenge
Date: 2018-08-10 18:00
Keywords: thugcrowd, ctf, badge-challenge

## [Thugcrowd DEFCON Badge Challenge Link](https://thugcrowd.com/badge.html), [Mirror](http://archive.is/xrfD6):

This was one of my first introductions to non-standard CTF-y solvable challenges. At first glance, challenge has a few things which seem to be noteworthy: 
- `BEGIN PRIVATE KEY` seems indicative of a cryptographic key. `BEGIN PRIVATE KEY` is indicative of the PKCS#8 format, which, in this format appears to be unencrypted (since it lacks the `ENCRYPTED` phrase in the header). 
- The body of the key is not base64 encoded as we would expect, instead, it appears to be in hexadecimal. 
- The skull resembles the Punisher logo, this might be important.
- There are two MD5 sums near the bottom, and a binary. 

My first step was to download the binary, `skull`, and run md5sum on it to see if the value matched:
```bash
user@box:/mnt/a/thugcrowd_skull_challenge$ 
md5sum skull
7ffb9fbb97af9533f0ed771b3856d7a8  skull
```

This file matches the checksum on the website, which is a good start. I tried doing the same with the "key", and ended up spending way too much time trying to format the file to get a match on the checksum listed on the page. What I ended up doing was copying the contents of the "key" into HxD, and saving that as a binary:
<a href="/includes/static/thugcrowd_badge/1-hxd-1.jpg" data-lightbox="1-hxd-1" data-title="1-hxd.jpg">
    <img src="/includes/thumbs/thugcrowd_badge/1-hxd-1.jpg" title="hxd skull key" />
</a>
```
user@box:/mnt/a/thugcrowd_skull_challenge$ md5sum key 
34d00b96da65131a759ebe54d42d3136  key
```

I ran `binwalk` on both binaries, which resulted in the following: 
```
user@box:/mnt/a/thugcrowd_skull_challenge$ binwalk key                                                            

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------

user@box:/mnt/a/thugcrowd_skull_challenge$ binwalk skull

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ELF, 64-bit LSB executable, AMD x86-64, version 1 (GNU/Linux)
216           0xD8            ELF, 64-bit LSB processor-specific, (GNU/Linux)
325235        0x4F673         Copyright string: "Copyright (C) 1996-2013 the UPX Team. All Rights Reserved. $"
```

Running the `skull` binary shows us: 
```bash
ptl@kali:~/tc_badge$ ./skull 
This message requires that you supply a key to decrypt
```

At the time, I wasn't really sure what to do (I forgot about the `key`), so I decided to try my hand at a little debugging to see if I could get anywhere. I used `gdb`, the GNU Debugger. 
```bash
ptl@kali:~/tc_badge$ gdb -f ./skull 
GNU gdb (Debian 8.2.1-2) 8.2.1
Reading symbols from ./skull...(no debugging symbols found)...done.
(gdb) r
Starting program: /home/ptl/tc_badge/skull 
The gates of heaven remain closed

Program terminated with signal SIGKILL, Killed.
The program no longer exists.
```

This didn't prove to be much help, but the message `The gates of heaven remain closed` seemed like something that wasn't part of gdb. Searching for this string online:

- [SherLocked](https://github.com/elfmaster/sherlocked/blob/master/stub.c)
- [PoC || GTFO 0x06 - Davinci Seal by Ryan O’Neill](https://nostarch.com/gtfo) 

Without going too deep down the path, at this point I decided that it was probably better to try to not find a way around the way the challenge was meant to be solved, so back to the skull key. I ran the `strings` command on the binary I created from the hex dump on the website - the binary was expectedly very small, so it seemed like a decent option:
```bash
ptl@kali:~/tc_badge$ strings key 
   B8012 4CD15 B8030 0CD10 FA0F0 1 163      7 7C0             F20 C0668 3C801   0 F  2  2 C       6     6 8 3 C 8      0 1 0 F22C0     EA3D  7 C 0   8     00000 0 000 00000 00 00 FFFF0 000 0      09A C             F00 F   F FF 00   
```

Running file gives us:
```bash
ptl@kali:~/tc_badge$ file key
key: COM executable for DOS
```

Having some experience with Windows, I knew that .COM files are part of the DOS boot process, one specific example being the command line interpreter, `COMMAND.COM`. 
<a href="/includes/static/thugcrowd_badge/2-hxd-2.jpg" data-lightbox="2-hxd-2" data-title="2-hxd-2.jpg">
    <img src="/includes/thumbs/thugcrowd_badge/2-hxd-2.jpg" title="hxd header" />
</a>
I went back to the file in HxD, and I looked up the first few bytes in [Gary Kessler's file signature table](https://www.garykessler.net/library/file_sigs.html) to see if I could verify this, but I wasn't able to find it in the table. Searching for them instead led me to a better result: 

- [Alex Parker's Writing a Bootloader Part 1](http://3zanders.co.uk/2017/10/13/writing-a-bootloader/)
- [Alex Parker's Writing a Bootloader Part 2](http://3zanders.co.uk/2017/10/16/writing-a-bootloader2/) 
- [Alex Parker's Writing a Bootloader Part 3](http://3zanders.co.uk/2017/10/18/writing-a-bootloader3/)
- [Alex PArker's Writing a Bootloader Presentation](http://3zanders.co.uk/2017/10/13/writing-a-bootloader/writingabootloader.pdf)

[Wikibooks](https://en.wikibooks.org/wiki/X86_Assembly/Bootloaders) has a great writeup about the makeup and technical details behind bootloaders - this article helped me understand more about what I was possibly dealing with, but I was a bit unsure as to if this was actually a bootloader, since it was missing the very clearly required/documented `0xAA55` signature designating a valid boot sector. I tried executing this file in multiple Windows OS (7, DOSBOX, FreeDOS), but I was unable to get it to run in any capacity. My next step was to attempt to boot it inside of VirtualBox as a floppy disk image.
<a href="/includes/static/thugcrowd_badge/3-virtualbox-1.jpg" data-lightbox="3-virtualbox-1.jpg" data-title="3-virtualbox-1.jpg">
    <img src="/includes/thumbs/thugcrowd_badge/3-virtualbox-1.jpg" title="virtualbox floppy" />
</a>

<a href="/includes/static/thugcrowd_badge/4-virtualbox-2.jpg" data-lightbox="4-virtualbox-2.jpg" data-title="4-virtualbox-2.jpg">
    <img src="/includes/thumbs/thugcrowd_badge/4-virtualbox-2.jpg" title="virtualbox boot" />
</a>

Once booting, we see something reminiscent of the result of the `strings` command we ran above. ThugCrowd has a thing for making awesome ASCII art, so looking at with a less technical interpretation might be a good idea (it does appear to be somewhat abstract): 

<a href="/includes/static/thugcrowd_badge/5-key-1.jpg" data-lightbox="5-key-1.jpg" data-title="5-key-1.jpg">
    <img src="/includes/thumbs/thugcrowd_badge/5-key-1.jpg" title="the key?" />
</a>

<a href="/includes/static/thugcrowd_badge/6-key-2.jpg" data-lightbox="6-key-2.jpg" data-title="6-key-2.jpg">
    <img src="/includes/thumbs/thugcrowd_badge/6-key-2.jpg" title="the key..." />
</a>

`KEY IS SAKURA` is clearly the message. Maybe this is the key to decrypt the binary? 
```
ptl@kali:~/tc_badge$ ./skull SAKURA
                                                                  ██           
    ──────────────────────────────────────────────────────────── ▒██ ──────    
   ████████ ███  ██ ███  ██  ██████  ██████ ███████ ███████  ██  ▒██ ███████   
  ▒▒▒▒███  ▒███ ▒██▒███ ▒██ ███     ███▒▒▒ ▒▒▒▒▒▒▒██▒▒▒▒▒▒██▒██ █▒██▒▒▒▒▒▒▒██  
     ▒███  ▒███████▒███ ▒██▒███  ██▒███      ██████  ██  ▒██▒███████  ███ ▒██  
     ▒███  ▒███▒▒██▒███ ▒██▒███ ▒██▒███     ▒██▒▒██ ▒██  ▒██▒███▒███ ▒███ ▒██  
     ▒███  ▒███ ▒██▒▒█████ ▒▒██████▒▒██████ ▒██ ▒▒██▒▒█████ ▒██ ▒▒██ ▒██████   
     ▒▒▒   ▒███ ▒▒  ▒▒▒▒▒   ▒▒▒▒▒▒  ▒▒▒▒▒▒  ▒▒   ▒▒  ▒▒▒▒▒  ▒▒   ▒▒  ▒▒▒▒▒▒    
    ┌───── ▒▒▒  ───────────────────────────────────────────────────────────┐   
    │                                                                      │   
    │             Congrats! You just figured out the puzzle!               │   
    │  If you were the first to solve it and alert us, you have just won   │   
    │  a really beautiful custom Defcon Badge / Embedded lab! Lucky you!   │   
    │                                                                      │   
    │        Tweet a screenshot of this to @thugcrowd or email to          │   
    │                         info@thugcrowd.com                           │   
    │                                                                      │   
    │    Badges will be available for pick up at Defcon. If you aren't     │   
    │  attending Defcon, we can give the badge through alternative means!  │   
    │                                                                      │   
    │                       Thanks for playing!                            │   
    │                                                                      │   
    └──────────────────────────────────────────────────────────────────────┘   
          Verification Hash: aHR0cHM6Ly90d2l0dGVyLmNvbS90aHVnY3Jvd2Q=
```