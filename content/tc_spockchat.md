Title: ThugCrowd Spock Chat Challenge
Date: 2019-08-10 12:00
Keywords: thugcrowd, ctf, chat challenge, star-trek

## [Thugcrowd Matrix Spock Challenge](https://twitter.com/thugcrowd/status/1158172622577946625), [Mirror](http://archive.is/kldUo):

Yet again, we have another classic ThugCrowd chat challenge, this time, featuring a picture of Spock from Star Trek. This challenge was set to expire in 14 days from the publishing date, but unfortunately the steps to solve it were leaked early which is why I'm publishing this writeup early as well. To begin, the tweet contains the following message: 

```
--- BEGIN ThugCrowd Chat Challenge No. 4 ---

This message will self destruct in 14 days

YmVnaW4gNjY0IHVybApNOicxVDwnLForUl1UPEYlTjxWOUU8QllTOiJdLDFXLFc4Ml1TPSYlUjlGUUU5NzE/PSY1Ujs2RU44NlAqCmAKZW5kCg==
```

This string appears to have a main characteristic of a base64 encoded string (the padding on the end), so we can throw this into a [base64 decode utility](https://cryptii.com/pipes/base64-to-text), or just use bash. Either way, we can decode it into this: 

```
begin 664 url
M:'1T<',Z+R]T<F%N<V9E<BYS:"],1W,W82]S=&%R9FQE971?=&5R;6EN86P*
`
end
```

I was unfamiliar with this syntax, so I searched for `begin 664 url`, which turned out to be a [Uuencoded](https://en.wikipedia.org/wiki/Uuencoding) package. To turn this file into something worthwhile, we can use `uudecode` in Linux to decode and unpack. Decoding provides us with a text file, and getting the contents: 

```
user@box:~/tc_spock_chat$ cat url 
https://transfer.sh/LGs7a/starfleet_terminal
```

Downloading the file and performing some basic identification analysis: 

```
user@box:~/tc_spock_chat$ file starfleet_terminal 
starfleet_terminal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), for GNU/Linux 3.2.0, BuildID[sha1]=17f312b0279669021ac1fd51f1aa39c42a773bad, dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, no section header


user@box:~/tc_spock_chat$ binwalk starfleet_terminal 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
544           0x220           LZMA compressed data, properties: 0x5C, dictionary size: 0 bytes, uncompressed size: 1543503872 bytes
552           0x228           LZMA compressed data, properties: 0x5C, dictionary size: 0 bytes, uncompressed size: 67108864 bytes
13476         0x34A4          LZMA compressed data, properties: 0x5C, dictionary size: -1056964608 bytes, uncompressed size: 436207580 bytes
13568         0x3500          LZMA compressed data, properties: 0xB8, dictionary size: -1023410176 bytes, uncompressed size: 1442840540 bytes
16160         0x3F20          LZMA compressed data, properties: 0xC0, dictionary size: 0 bytes, uncompressed size: 150994944 bytes
```

Based on this initial inspection, it's safe to say that this is an executable file, and since I'm running this challenge in a decently secured sandbox, I don't have any qualms about executing the binary in bash, but you could also run it in `gdb` if you wanted to step through it. I didn't feel like this was necessary, so I `chmod +x starfleet_terminal` and executed it. One of the interesting things about this binary, is that it floods the screen with newlines, and accepts all input, but doesn't respond in any way until you try to kill the program with `CTRL-C`. I ended up with something like this: 

```
user@box:~/tc_spock_chat$ ./starfleet_terminal 
ENTERPRISE TERMINAL:

<snip whitespace>

^C

ESTABLISHING SIGNAL...


ESTABLISHING SIGNAL...


ESTABLISHING SIGNAL...


ESTABLISHING SIGNAL...


ESTABLISHING SIGNAL...
CONNECTION ESTABLISHED
...
 ... INCOMING EMERGENCY BROADCAST
 ...
 ...
 ... ACCEPTING BROADCAST MESSAGE
 ... 
                                                                                 
                                                                                 
                                                                                 
                                                                                 
                                        .                                        
                                       .:.                                       
                                      .:::.                                      
                                     .:::::.                                     
                                 ***.:::::::.***                                 
                            *******.:::::::::.*******                            
                          ********.:::::::::::.********                          
                         ********.:::::::::::::.********                         
                         *******.::::::'***`::::.*******                         
                         ******.::::'*********`::.******                         
                          ****.:::'*************`:.****                          
                            *.::'*****************`.*                            
                            .:'  ***************    .                            
                           .                                                     
 
 
   ##############################################################################
   ##############################################################################
   ##########################        BROADCAST       ############################
   ##############################################################################
   ##############################################################################
   #**********************************ORIGIN************************************#
   #                                                                            #
   #                              STARFLEET SHIP                                #
   #----------------------------------------------------------------------------#
   #                                                                            #
   #                              USS VENGEANCE                                 #
   #                                                                            #
   #****************************************************************************#
   #                                                                            #
   #                               REGISTRY ID                                  #
   #----------------------------------------------------------------------------#
   #                                                                            #
   #                               NCC-177358                                   #
   #                                                                            #
   #*********************************MESSAGE************************************#
   # MAYDAY                                                                     #
   #                                                                            #
   # MAYDAY                                                                     #
   #                                                                            #
   # WE HAVE BEEN BOARDED BY KAHN, HE IS COMMANDEERING THE SHIP.                #
   #                                                                            #
   # HE HAS KILLED ADMIRAL MARCUS                                               #
   #                                                                            #
   # HE IS NOW TRANSPORTING SEVENTY TWO ADVANCED LONG-RANGE TORPEDOES           #
   #                                                                            #
   # WE BELIEVE HE IS AIMING FOR STARFLEET HEADQUATERS                          #
   #                                                                            #
   # THE ENTERPRISE IS HEAVILY DAMAGED                                          #
   #                                                                            #
   #**********************************ERROR*************************************#
 
   SIGNAL LOST ....
   ...
   ATTEMTPING TO REESTABLISH  ...........
   .......
   ............
   .............
   UNABLE TO ESTABLISH CONNECTION ............. 
   ....
   ARCHIVING MESSAGE.. 
   .........
   .............. 
   ARCHIVED MESSAGE : 
 
     /Td6WFoAAATm1rRGAgAhARYAAAB0L+WjAQCeH4sICMA2Rl0AA2N0NjQAHcvRCoIwFADQd79GW0E9 
     NsF5lw1MnfO+6RYzu6tAMvz7qPdz6qAZ5JI6JpPelDPkjgahlqFtvBN7r8WYYIwztjoubrzp24RA 
     UABxCJBfnlhxskzREBRFRcpXNHyxj/Kf3WYkG/TLsh/cTb3IYhDZG1M+dUau14ovzpS+ZvKOBvx5 
     On5UtT1FXxDiLoKWAAAAAABY3YwVRBDWWgABtwGfAQAAZUUbHbHEZ/sCAAAAAARZWg== 
 
ENTERPRISE TERMINAL:
```

In this awesome looking output, we have an archived message near the bottom, which again appears to be base64 encoded, so we can decode it and see what type of file it is:

```
user@box:~/tc_spock_chat$ base64 -d <<< /Td6WFoAAATm1rRGAgAhARYAAAB0L+WjAQCeH4sICMA2Rl0AA2N0NjQAHcvRCoIwFADQd79GW0E9NsF5lw1MnfO+6RYzu6tAMvz7qPdz6qAZ5JI6JpPelDPkjgahlqFtvBN7r8WYYIwztjoubrzp24RAUABxCJBfnlhxskzREBRFRcpXNHyxj/Kf3WYkG/TLsh/cTb3IYhDZG1M+dUau14ovzpS+ZvKOBvx5On5UtT1FXxDiLoKWAAAAAABY3YwVRBDWWgABtwGfAQAAZUUbHbHEZ/sCAAAAAARZWg==>archived_message.file

user@box:~/tc_spock_chat$ file archived_message.file
archived_message: XZ compressed data
```

I wasn't familiar with `.xz` compression beforehand, so I kept going with basic analysis: 

```
user@box:~/tc_spock_chat$ binwalk archived_message.file

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             xz compressed data
27            0x1B            gzip compressed data, has original file name: "ct64", from Unix, last modified: 2019-08-04 01:37:04
```

And the `gzip` really gave it away (I suppose `compressed data` wasn't obvious enough for me). We can use `unxz` to unpack the binary: 

```
user@box:~/tc_spock_chat$ unxz archived_message.file 
unxz: archived_message.file: Filename has an unknown suffix, skipping
```

Rename the file to .xz and try again...

```
user@box:~/tc_spock_chat$ mv archived_message.file archived_message.xz
user@box:~/tc_spock_chat$ unxz archived_message.xz
```

This expands the `gzip` file, which we can extract with gunzip: 

```
user@box:~/tc_spock_chat$ gunzip archived_message 
gzip: archived_message: unknown suffix -- ignored
```

And the filetype again...

```
user@box:~/tc_spock_chat$ mv archived_message  archived_message.gz
user@box:~/tc_spock_chat$ gunzip archived_message.gz 
```

And now we're left with another text file with a string:

```
user@box:~/tc_spock_chat$ cat archived_message 
TmV3IHJlY3J1aXQsIHdlbGNvbWUgdG8gVGh1Z0ZsZWV0LiBUaW1lIGlmIG9mIHRoZSBlc3NlbmNl
LCByZXBvcnQgdG8gd2hlcmVpc3RoZS5jaGF0IGFuZCBjYXJyeSBvdXQgT3JkZXIgMjAwNS4K
```

Again, this looks like base64:
```
user@box:~/tc_spock_chat$ base64 -d archived_message
New recruit, welcome to ThugFleet. Time if of the essence, report to whereisthe.chat and carry out Order 2005.
```

Unfortunately, due to the challenge being leaked, `whereisthe.chat` now redirects to the main ThugCrowd website, so I'll have to omit some graphics regarding the next section. Visiting `whereisthe.chat`, the user is given a QR code which can be decoded with a number of different utilities. I chose `zbarimg`, which can decode an input QR code to the plaintext result:

```
user@box:~/tc_spock_chat$ zbarimg whereisthe.chat.png 
QR-Code:otpauth://totp/StarThug:you@thu.gg?issuer=OperationSelfDestruct&algorithm=SHA1&digits=6&period=30&secret=GE4TELRRGY4C4MJSFY4TSLRT&port=42069
scanned 1 barcode symbols from 1 images in 0.03 seconds
```

This result immediately looks like a time-based one-time password, indicated by `otpauth`, `totp`, `digits`, `period` - you can read more about this on the [Google Authenticator Key URI Format](https://github.com/google/google-authenticator/wiki/Key-Uri-Format) GitHub page. The interesting things about this `otpauth` url are the port on the end, `42069`, and the `secret`, which as seen in the GitHub page, is a base32 encoded key, with no padding required (the padding in this case was an arbitrary number appended to the requester's IP address): 

```
user@box:~/tc_spock_chat$ base32 -d <<< GE4TELRRGY4C4MJSFY4TSLRT
192.168.12.99.3
```

There doesn't seem to be anything fishy with this, so I loaded the QR code into [WinAuth](https://winauth.github.io/winauth/) to generate my OTP. The more pressing matter however is the port at the end of the `otpauth` string, and to which host it's used to connect. We probably don't have that port open on our own machine (unless the archived message opened it, but it didn't), so I tried to connect to the QR code issuing website, since that's the only other server we've been given so far: 

```
user@box:~/tc_spock_chat$ nc whereisthe.chat 42069
DESTRUCT SEQUENCE
    ONE      
  CODE:768290
ABORTING
DESTRUCT SEQUENCE
    ONE      
  CODE:768 290 
ABORTING
DESTRUCT SEQUENCE
    ONE      
  CODE:803 923
ABORTING
DESTRUCT SEQUENCE
    ONE      
  CODE:803923
ABORTING
```

As seen above, I tried entering my OTP code a few different ways, but I couldn't get the destruct sequence to start. A little bit of searching on Memory Alpha turned up [a page about Order 2005](https://memory-alpha.fandom.com/wiki/Auto-destruct). Unfortunately I skipped TOS and went straight into TNG/Voyager... Anyway, let's give this a shot (still keeping our OTP code in mind): 

```
user@box:~/tc_spock_chat$ nc whereisthe.chat 42069


DESTRUCT SEQUENCE
    ONE      
  CODE:11A
DESTRUCT SEQUENCE
    TWO      
  CODE:11A2B
DESTRUCT SEQUENCE
   THREE    
  CODE:1B2B3


DESTRUCT SEQUENCE
 COMPLETED    
   AND ENGAGED   


  AWAITING     
 FINAL CODE    
  FOR 30-SECOND   
    COUNTDOWN    

  CODE:724137
ENCRYPTED MESSAGE FROM THUGFLEET
               .
              .:.
             .:::.
            .:::::.
        ***.:::::::.***
   *******.:::::::::.*******
 ********.:::::::::::.********
********.:::::::::::::.********
*******.::::::'***`::::.*******
******.::::'*********`::.******
 ****.:::'*************`:.****
   *.::'*****************`.*
   .:'  ***************    .
  .
jrKJt72MnauFjJ3uvJydi4bt5u+7l7S3lpmzqbuMnaW97afthYiOuLuYt7OWl53uurGvrIWMmriN7ee4u5jnuLyys6m7nOqvvYyd772mnbW8som3u5iKuIaI67iGiJG1veyJqruc67iJmLezvbadrr3ts6qWnJG2veyVsZCyt6m7mKevvbKKqoayp6+9tuqxhaadt72yjri7l7OohYyet4aHie++nJ2qvO2vsoW0jbCLtKeQke67rJCKlqiJmo6mkIeds5CKjZC7ma+Ou++JkYqO4uI=
```

Now this looks like something we would expect, a Thugcrypted message from ThugFleet. Again, this appears to be a base64 encoded string, so let's do some basic checking: 
```
user@box:~/tc_spock_chat$ base64 -d <<< jrKJt72MnauFjJ3uvJydi4bt5u+7l7S3lpmzqbuMnaW97afthYiOuLuYt7OWl53uurGvrIWMmriN7ee4u5jnuLyys6m7nOqvvYyd772mnbW8som3u5iKuIaI67iGiJG1veyJqruc67iJmLezvbadrr3ts6qWnJG2veyVsZCyt6m7mKevvbKKqoayp6+9tuqxhaadt72yjri7l7OohYyet4aHie++nJ2qvO2vsoW0jbCLtKeQke67rJCKlqiJmo6mkIeds5CKjZC7ma+Ou++JkYqO4uI=
����������������ﻗ�������������텈�����������������縻�縼�����꯽��ｦ������������븆����쉪��븉����������������앱������������������걅������������������ﾜ����������������������������������������

user@box:~/tc_spock_chat$ base64 -d <<< jrKJt72MnauFjJ3uvJydi4bt5u+7l7S3lpmzqbuMnaW97afthYiOuLuYt7OWl53uurGvrIWMmriN7ee4u5jnuLyys6m7nOqvvYyd772mnbW8som3u5iKuIaI67iGiJG1veyJqruc67iJmLezvbadrr3ts6qWnJG2veyVsZCyt6m7mKevvbKKqoayp6+9tuqxhaadt72yjri7l7OohYyet4aHie++nJ2qvO2vsoW0jbCLtKeQke67rJCKlqiJmo6mkIeds5CKjZC7ma+Ou++JkYqO4uI=> encrypted_message

user@box:~/tc_spock_chat$ file encrypted_message 
encrypted_message: Non-ISO extended-ASCII text, with NEL line terminators

user@box:~/tc_spock_chat$ binwalk encrypted_message 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------

```

Now is where the real fun begins. There are a few different methods to solve this, but the most important thing we need to do is to identify what type of file we are actually working with. Unbeknownst to me at the time, there exists a pretty cool tool called [CyberChef](https://gchq.github.io/CyberChef) which trivializes this challenge, with the `magic` operator. If this is the tool you would decide to use, the proper way of going about this would be to use the following recipe: 

```
Input = jrKJt72MnauFjJ3uvJydi4bt5u+7l7S3lpmzqbuMnaW97afthYiOuLuYt7OWl53uurGvrIWMmriN7ee4u5jnuLyys6m7nOqvvYyd772mnbW8som3u5iKuIaI67iGiJG1veyJqruc67iJmLezvbadrr3ts6qWnJG2veyVsZCyt6m7mKevvbKKqoayp6+9tuqxhaadt72yjri7l7OohYyet4aHie++nJ2qvO2vsoW0jbCLtKeQke67rJCKlqiJmo6mkIeds5CKjZC7ma+Ou++JkYqO4uI=

From Base64
"Magic" (scroll through until you find something that looks legitimate, and click on one of the results and finish from there)
```

This will give you an auth code and connection information to join the ThugCrowd Matrix chat. If you're interested in another way to solve this, please continue reading. 

<hr>

Speaking with one of my more savvy friends about this, I originally thought this was some type of private key or other type of secret which contained the answer - however, I wasn't able to get anywhere by formatting it multiple ways and trying to use `openssl` to decode the message. The decoded base64 output didn't really give me any major pointers, but one of the things he pointed out to me was that I should take a look at the bytes in the hex dump: 

```
user@box:~/tc_spock_chat$ base64 -d <<< jrKJt72MnauFjJ3uvJydi4bt5u+7l7S3lpmzqbuMnaW97afthYiOuLuYt7OWl53uurGvrIWMmriN7ee4u5jnuLyys6m7nOqvvYyd772mnbW8som3u5iKuIaI67iGiJG1veyJqruc67iJmLezvbadrr3ts6qWnJG2veyVsZCyt6m7mKevvbKKqoayp6+9tuqxhaadt72yjri7l7OohYyet4aHie++nJ2qvO2vsoW0jbCLtKeQke67rJCKlqiJmo6mkIeds5CKjZC7ma+Ou++JkYqO4uI= | xxd
00000000: 8eb2 89b7 bd8c 9dab 858c 9dee bc9c 9d8b  ................
00000010: 86ed e6ef bb97 b4b7 9699 b3a9 bb8c 9da5  ................
00000020: bded a7ed 8588 8eb8 bb98 b7b3 9697 9dee  ................
00000030: bab1 afac 858c 9ab8 8ded e7b8 bb98 e7b8  ................
00000040: bcb2 b3a9 bb9c eaaf bd8c 9def bda6 9db5  ................
00000050: bcb2 89b7 bb98 8ab8 8688 ebb8 8688 91b5  ................
00000060: bdec 89aa bb9c ebb8 8998 b7b3 bdb6 9dae  ................
00000070: bded b3aa 969c 91b6 bdec 95b1 90b2 b7a9  ................
00000080: bb98 a7af bdb2 8aaa 86b2 a7af bdb6 eab1  ................
00000090: 85a6 9db7 bdb2 8eb8 bb97 b3a8 858c 9eb7  ................
000000a0: 8687 89ef be9c 9daa bced afb2 85b4 8db0  ................
000000b0: 8bb4 a790 91ee bbac 908a 96a8 899a 8ea6  ................
000000c0: 9087 9db3 908a 8d90 bb99 af8e bbef 8991  ................
000000d0: 8a8e e2e2                                ....
```

He made the observation that the bytes were somewhat uniform, and that they were all just right outside of the printable ASCII hexadecimal range (0x20-0x7F): 

```
  2 3 4 5 6 7   
-------------  
0:   0 @ P ` p   
1: ! 1 A Q a q  
2: " 2 B R b r  
3: # 3 C S c s  
4: $ 4 D T d t
5: % 5 E U e u  
6: & 6 F V f v 
7: ' 7 G W g w  
8: ( 8 H X h x 
9: ) 9 I Y i y
A: * : J Z j z
B: + ; K [ k {
C: , < L \ l |
D: - = M ] m }
E: . > N ^ n ~
F: / ? O _ o DEL
```

I didn't notice this at the time, and I probably wouldn't have been able to figure this out without that tip, but I like to believe the ThugCrowd challenges are all about spreading knowledge and helping everyone to improve. I decided this one might be a bit much to finish in Microsoft Excel, so I started looking up some more command-line ways of processing XOR'd strings. I had previously used [xortool](https://github.com/hellman/xortool), but I don't think it's the best method to use if you're looking to understand the solution, so I kept searching, and eventually found a set of crypto challenges on [cryptopals](https://cryptopals.com/sets/1) which helped me write my own tool to decode this message.

I worked through the first few challenges to get an idea as to how I was going to approach [challenge 3](https://cryptopals.com/sets/1/challenges/3), and the code below was what I wrote to decode this message (it expands upon the Cryptopals challenge by adding a base64 decode) - this requires `langdetect` to do some basic result parsing. It's not great, but it ended up getting the job done! 

The methodology behind the development of this was to initially decode the message as a `base64->hex->xor(single byte)`, but I needed to add a `.decode('hex')` while developing to get a readable result. Most of the results were garbled text, but a small amount looked like base64, which is where the second set of `b64decode` comes from. 

```python
import base64, binascii, string
from textwrap import wrap
from langdetect import detect
def try_base64 (input):
    try: 
        result = base64.b64decode(input)
    except:
        result = False
        pass 
    if (result):
        return True

# take our input string and convert it to hexadecimal 
input_string = 'jrKJt72MnauFjJ3uvJydi4bt5u+7l7S3lpmzqbuMnaW97afthYiOuLuYt7OWl53uurGvrIWMmriN7ee4u5jnuLyys6m7nOqvvYyd772mnbW8som3u5iKuIaI67iGiJG1veyJqruc67iJmLezvbadrr3ts6qWnJG2veyVsZCyt6m7mKevvbKKqoayp6+9tuqxhaadt72yjri7l7OohYyet4aHie++nJ2qvO2vsoW0jbCLtKeQke67rJCKlqiJmo6mkIeds5CKjZC7ma+Ou++JkYqO4uI='
string_hex = base64.b64decode(input_string).encode('hex')

hex_range = [hex(x) for x in range(256)]

result_list = []
string_split = wrap(string_hex, 2)
for i in hex_range:
    i = i[2:]
    temp_values = []
    for value in string_split:
        # xor and add to list as hex
        # print('xoring {} and {}'.format(int(i, 16), int(value,16)))
        xor_value = int(i, 16) ^ int(value, 16)
        # print('appending {}'.format(hex(xor_value)))
        temp_values.append(hex(xor_value)[2:].zfill(2))
        
    new_result = (''.join(temp_values[0:len(temp_values)]))
    # print('appending {}'.format(new_result))
    result_list.append(new_result)

valid_results = []
printable = set(string.printable)
for result in result_list:
    # convert to base64 and see if its decodeable
    try: 
        b64string = result.decode('hex').encode('base64')
    except:
        pass
    
    if(try_base64(b64string)): 
        # try to decode the string and check if it's valid 
        test_string = base64.b64decode(b64string)
        if(try_base64(test_string)):
            test_string = base64.b64decode(test_string)
        
        # check language
        try:
            test_lang = detect(test_string)
            # should we assume that the answer has a space as well?
            # using langdetect to check for a string which matches 'en', and has a space
            # we also do a simple comparison to throw out all non-printable characters, and check input->output length
            if ((test_lang == 'en') and (' ' in test_string) ):
                # looks ok, try to remove non printable chars and check if its the same 
                printable_chars = filter(lambda x: x in printable, test_string)
                print('processing: {}'.format(test_string))
                if(len(printable_chars) == len(test_string)):
                    # strings match 
                    valid_results.append(test_string)
        except: 
            pass

valid_results
```

running this file: 

```bash
user@box:~/tc_spock_chat$ python testfile.py 
processing: 7
/            05$<5$W%$2?T_V.
5$TT<17!
/.$<5#4T^!^

%S5$V$

      0!3?1R?1(
               U0%R0!
$T
/%(U)
     !
      3?
        <$
          7.
<5'?>0V%$T
)(W)3/0#7)>$
)34) 7V0(37[[
processing: B~E{q@QgI@Q"pPQGJ!*#w[x{ZUew@Qiq!k!IDBtwT{Z[Q"v}c`I@VtA!+twT+tp~ewP&cq@Q#qjQyp~E{wTFtJD'tJD]yq EfwP'tET{qzQbq!fZP]zq Y}\~{ewTkcq~FfJ~kcqz&}IjQ{q~Btw[dI@R{JKE#rPQfp!c~IxA|Gxk\]"w`\FZdEVBj\KQ\FA\wUcBw#E]FB..
processing: @|GysBSeKBS rRSEH#(!uYzyXW}guBSks#i#KF@vuVy}XYS tabKBTvC#)vuV)vr|}guR$asBS!shS{r|GyuVDvHF%vHF_{s"GduR%vGVy}sxS`s#}dXR_xs"[^|yguVias|DdH|iasx$KhSys|@vuY}fKBPyHIG!pRSdr#a|KzC~Ezi^_ ub^DXfGT@h^IS}^DC^uWa@u!G_D@,,
processing: A}FxrCRdJCR!sSRDI") tX{xYV|ftCRjr"h"JGAwtWx|YXR!u~`cJCUwB"(wtW(ws}|ftS%`rCR riRzs}FxtWEwIG$wIG^zr#FetS$wFWx|ryRar"|eYS^yr#Z~_}xftWh`r}EeI}h`ry%~JiRxr}AwtX|gJCQxIHF qSRes"`}J{BD{h_^!tc_EYgFUAi_HR|_EB_tV`At F^EA--
processing: Beam me up Scotty! You solved the puzzle! Go to riot.im to create an account. Then join #borg:hotline.blin.gg and type !auth nsjffDhNLN7Wl9B0TD29pe9DNtZPwEMQ
```

I had some erroneous results in the output, but I was able to get the correct message in the end. I'm currently working through the Cryptopals challenges, and I would highly recommend them - they build on top of each other and are very good for learning (for me at least!). Thank you for reading, and thanks to the ThugCrowd community for making this awesome challenge! 