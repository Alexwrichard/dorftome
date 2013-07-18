df-legends-reader
=================

Hopefully, this will eventually be a GTK browser-thing that allows you to view Dwarf Fortress legends exports in an efficient and fluid manner. I'm trying to write non-OO code, just to see what it's like. So this is a little experiment in that respect, too. 

I'm using lxml to parse the XML, because it's HELLA fast. I can get it to parse a 12MB file in under a second, and that includes the time it takes to convert those tags to a gigantic Python dictionary. We'll see how it performs for larger worlds...

##Goals
I'd like to do things that other DF legends browsers don't do well. 

* Keyboard-only navigation
* Fast search. This is going to be hard. But I want it to be *at least* as responsive as the search in DF legends mode.
* Giving the user a good idea of the *relationships* between historical figures.
    + Eventually, maybe a graph (vertices+edges) that shows this visually? That would be awesome.
* Visually appealing - I will use clean, elegant light fonts against a dark background, but allow users to change this.
* Easy reading. Actually, this is the most important. I want to build a way for a reader to get immersed in the history of the world. I haven't been able to experience this in DF Legends mode.
