[![Advent of Code](./advent-of-code.jpg)](https://adventofcode.com)

[![MIT License](https://img.shields.io/github/license/sumnerevans/advent-of-code)](https://github.com/sumnerevans/advent-of-code/blob/master/LICENSE)
[![LiberaPay Donation Status](https://img.shields.io/liberapay/receives/sumner.svg?logo=liberapay)](https://liberapay.com/sumner/donate)

These are my solutions to Advent of Code problems. If you want to join my
leaderboard, the code is `540750-9589f56d`.

When I solve for speed on the night when the problem opens, I solve using
Python. I've gone back and solved a few problems in other languages as well.

**Starting in 2020, I am streaming my solve sessions [on
Twitch](https://www.twitch.tv/sumnerevans).** Go over there and follow to be
notified when I stream!

I then upload the VODs to [my YouTube
channel](https://www.youtube.com/channel/UCyrdRO4oJRpszr0ovN1FwBA).

* [2020 Playlist](https://www.youtube.com/playlist?list=PLpnr_TeIrBtB56VmuG8PIn5TU3wxkDtHE)
* [2021 Playlist](https://www.youtube.com/playlist?list=PLpnr_TeIrBtAXS6uWQijhF-2JjsArzFz7)

## A few random links

**Other solutions that I take a look at:**

* [Adam Sandstedt](https://github.com/AdamSandstedt/AdventOfCode)
* [Colin Siles](https://github.com/sColin16/AoC)
* [Jack Garner](https://gitlab.com/jhgarner/advent2021)
* [Jordan Newport](https://sr.ht/~talos/advent-of-code/)
* [Kelly Dance](https://github.com/mcbobby123/AdventOfCode2020)
* [Sam Sartor](https://gitlab.com/samsartor/aoc-2021/)

**Other streamers I like watching:**

* [Anthony Sottile](https://www.twitch.tv/anthonywritescode)
* [Jonathan Paulson](https://www.youtube.com/channel/UCuWLIm0l4sDpEe28t41WITA/featured)
* [Joshua Wise](https://www.youtube.com/user/joshuawise)
* [lizthegrey](https://www.twitch.tv/lizthegrey)
* [Rhymu](https://www.twitch.tv/rhymu)
* [where_is_x](https://www.twitch.tv/where_is_x)

**Why I'm not good at this:**

* [Why you probably won't get better at pool](https://jenniferbarretta.wordpress.com/2016/02/16/why-you-probably-wont-get-better-at-pool/)

## Workflow

This project uses [direnv](https://direnv.net/) and the Nix package manager to
manage the environment. The `shell.nix` file defines the Nix shell environment
and includes all of the necessary development dependencies. It also adds a bunch
of helper scripts to help with things such as running tests and getting the
input using `curl`.

## Results

### 2021 (44*, 115 points on global leaderboard)

```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
 22   00:09:58    503      0   03:45:25   2276      0
 21   00:07:55    352      0   00:22:56    144      0
 20   00:45:49   1489      0   01:07:34   2108      0
 19       >24h  11368      0       >24h  11815      0
 18   17:42:08  11447      0   17:50:55  11230      0
 17   00:10:48    240      0   00:16:56    271      0
 16   01:40:59   3439      0   01:55:56   3005      0
 15   00:05:10     84     17   01:51:23   3682      0
 14   00:07:33    391      0   01:08:40   3371      0
 13   00:35:07   3962      0   00:36:37   2836      0
 12   00:10:51    422      0   00:43:27   2240      0
 11   00:52:24   4855      0   00:54:24   4535      0
 10   00:11:12   1902      0   00:19:18   1640      0
  9   00:22:40   5314      0   00:39:34   2937      0
  8   00:07:24    890      0   00:44:03   1066      0
  7   00:02:29    252      0   00:10:14   1865      0
  6   00:03:14    122      0   00:06:50    175      0
  5   00:13:24   1238      0   00:36:27   2733      0
  4   00:16:54    845      0   00:37:47   2325      0
  3   00:06:56   1338      0   00:38:16   3718      0
  2   00:03:03   1045      0   00:04:57    856      0
  1   00:00:49     38     63   00:02:22     66     35
```

### 2020 (50*)

```
      -------Part 1--------   -------Part 2--------
Day       Time  Rank  Score       Time  Rank  Score
 25   00:57:18  3173      0   00:57:21  2555      0
 24   00:20:23  1084      0   00:40:55  1049      0
 23   00:22:30   613      0   02:26:58  1792      0
 22   00:06:49   439      0   00:33:54   573      0
 21   00:37:49  1489      0   00:58:18  1837      0
 20   04:32:46  4269      0   06:01:56  1760      0
 19   01:03:50  1931      0   05:58:15  4038      0
 18   00:26:27  1225      0   00:43:41  1219      0
 17   00:53:00  2348      0   00:56:46  2006      0
 16   00:10:02   399      0   00:26:58   254      0
 15   00:13:56  1055      0   00:15:28   464      0
 14   00:23:12  1982      0   00:43:30  1388      0
 13   00:06:21   573      0   03:50:06  5233      0
 12   00:09:49   775      0   00:39:10  2405      0
 11   00:28:55  2173      0   01:05:09  3183      0
 10   00:07:25  1095      0   00:19:54   708      0
  9   00:04:03   227      0   00:07:33   168      0
  8   00:09:07  1923      0   00:12:57   580      0
  7   00:12:51   360      0   00:27:50   830      0
  6   00:03:39   438      0   00:07:41   558      0
  5   00:10:35  1359      0   00:22:43  2656      0
  4   00:15:09  2854      0   00:30:14  1294      0
  3   00:08:47  1930      0   00:18:05  2689      0
  2   00:04:43   609      0   00:07:35   554      0
  1   00:08:00  1134      0   00:09:30   945      0
```

### 2019 (25*)

```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
 22       >24h   6358      0          -      -      -
 13       >24h  11578      0       >24h  10113      0
 12       >24h  13444      0          -      -      -
 11       >24h  12234      0       >24h  12056      0
 10       >24h  15732      0       >24h  13079      0
  9       >24h  16483      0       >24h  16401      0
  8       >24h  22630      0       >24h  21765      0
  7       >24h  22271      0       >24h  17754      0
  6       >24h  27344      0       >24h  25856      0
  5       >24h  29709      0       >24h  28316      0
  4       >24h  44079      0       >24h  40851      0
  3       >24h  44663      0       >24h  39209      0
  2       >24h  66808      0       >24h  60609      0
  1       >24h  90496      0       >24h  80094      0
```

### 2018 (16*)

```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
  8       >24h  18548      0       >24h  17532      0
  7       >24h  21967      0       >24h  17896      0
  6       >24h  22692      0       >24h  21696      0
  5       >24h  25987      0       >24h  25088      0
  4       >24h  25671      0       >24h  24794      0
  3       >24h  35912      0       >24h  34109      0
  2       >24h  49555      0       >24h  44474      0
  1       >24h  70773      0       >24h  56082      0
```

### 2017 (2*)

```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
  3       >24h  33811      0       >24h  25001      0
  2       >24h  48271      0       >24h  41038      0
  1       >24h  58514      0       >24h  48641      0
```
