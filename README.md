Paco's Version of BeerSnobSays
============

This is a fork of BeerSnobSays, a Twitter bot written by [@gjreda](https://twitter.com/gjreda). Follow the bot at  [@cigibot](https://twitter.com/cigibot) and follow me at [@pacohope](https://twitter.com/pacohope).

It's using the text of [@cigitalgem](https://twitter.com/cigitalgem)'s book *Software Security* and the text of the [BSIMM 6](https://www.bsimm.com/) report. It has produced a few fun gems.

So far, I've made a few small enhancements:

1. I made it randomly hashtag words. Right now, it looks to see if a word is longer than 6 characters, then it rolls a die. 20% of the time, it will hashtag the word.
2. It capitalises the first letter of the tweet, whether that word was originally capitalised or not. (there's a silly bug: if the first word of the tweet gets hashtagged, then it doesn't get capitalized)
3. It delays a random amount of time (between 0 and 1200 seconds) just so the tweets aren't bang on the minute every single time.

It's built with Python and a bunch of modules. In my case, I had to do the following to get my environment running on [FreeBSD](http://freebsd.org):
* `sudo pkg install git readline python`
* Make a link to `/usr/local/bin/bash` in `/bin` because Python's readline library won't compile correctly unless you do. `sudo ln -s /usr/local/bin/bash /bin`
* `curl -O https://bootstrap.pypa.io/get-pip.py`
* `sudo python get-pip.py`
* `sudo pip install Twython ipython gnureadline`
* create a `config.py` file

You invoke it by calling it with a file name of text that you want it to generate from. E.g.,:
```
/usr/local/bin/python markov.py input.txt
```

I took a bunch of word docs I had for a book and converted them to text files so it could use them. On MacOS that looks like:
```
for i in *.doc
  do
    /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to txt:Text "$i"
done
```

I invoke it from cron like so:
```
6 7,9,11,13,15,17,19,21,23 * * Mon,Tue,Wed,Thu,Fri,Sat /usr/local/bin/python /path/to/markov.py /path/to/cigibot.txt
```

You can follow the original [@beersnobsays](https://twitter.com/beersnobsays) and read [his original blog post](http://www.gregreda.com/2015/03/30/beer-review-markov-chains/).
