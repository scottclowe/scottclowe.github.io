---
layout: post
title: Setting Colour Schemes in Matlab
categories: matlab project colours
---

## Background

Quite a while ago now, I was in the situation where I was moving from one MATLAB installation to another, and I wanted to transfer my custom-made GUI colour scheme settings from the old installation to the new one. Since I wanted a dark-background theme, I had long-ago customised the GUI away from the defaults, and I was happy with the settings I had.

The problem was, there is no colour scheme manager option built into MATLAB - no option to export, nor import, a colour scheme.

I ended up manually setting up all the colours again on the new installation, but they didn't quite match and that really was rather annoying. I could have set *all* the RGB values to match -- but what then if I made an improvement to one of the copies? Then I'd have to remember to update the other too.

What's more, not only was I running MATLAB on two machines, but with dual-boot of Windows and Linux too, so there were three copies of the settings which I would have to keep manually synchronised!

This was clearly not going to work as a solution.

I could have copied the MATLAB preferences file, located at
{% highlight matlab %}
fullfile(prefdir, 'matlab.prf')
{% endhighlight %}
between the installations. But this file has a *lot* of content; the vast majority of which isn't to do with colour preferences. Furthermore, some of it is locale-specific, so it's not a great idea to keep copying the whole thing between installations.

Then I read this [Undocumented Matlab article], which described how system preferences could be accessed and changed programatically. This was clearly the best long-term solution.

I searched through `'matlab.prf'` and found the handles for all the Color Preferences settings. With that and the [Undocumented Matlab article] content, I rigged up a script which export the color preferences to the same format as used in `'matlab.prf'`, and another which would set the prefences to match the values in the settings file.

Fast forward around a year and a half, and I finally got around to finishing off this pair of functions, which now constitute the package [*MATLAB Schemer*][fex]. And with that, there is now a fully-fledged colour scheme manager for MATLAB.


## Quick-start

You can download *MATLAB Schemer* from [MATLAB FileExchange][fex] or from [GitHub][matlab-schemer].

You can import a new theme with the simple command
{% highlight matlab %}
schemer_import()
{% endhighlight %}
which will then let you pick the colour scheme to import. A selection of schemes are available in the `schemes` folder.

A new colour scheme can be easily created by exporting your current MATLAB colour preferences with the command:
{% highlight matlab %}
schemer_export()
{% endhighlight %}
New users should note that this won't work if you've left all the GUI colour preferences as they were when you installed MATLAB! The preferences have to have been set to be exportable; but don't worry because you can always restore the default MATLAB colour scheme again with `schemer_import('schemes/default.prf')`.

If you are transferring your settings from one MATLAB installlation to another, you can turn all the optional syntax highlighting on/off as you like it by importing with the `INCLUDEBOOLS` flag enabled, like so.
{% highlight matlab %}
schemer_import(true)
{% endhighlight %}

For more details, view the documentation.
{% highlight matlab %}
help schemer_import
help schemer_export
{% endhighlight %}

A general description of common usage is also available [here][README].

### Enabling/Disabling optional highlighting

If you're not seeing all the colours shown in the sample screenshots below enabled on your own system -- such as the global variable colour, cell-block background colour, current line background, or right-hand side character count line -- these are from colour preferences which are disabled by default on MATAB. You can enable them manually in the Preferences panel, or you can overwrite your current settings with the ones set up for the colour scheme in question with
{% highlight matlab %}
schemer_import(true)
{% endhighlight %}


## Colour schemes

I have implemented 9 themes (some light and some dark) to give users a few options to choose from.

I'd love to see others sharing their own themes and colour schemes, and welcome any such contributions to [matlab-schemes].

### MATLAB Schemes based on Gedit Themes

Since I also use the light-weight GNU editor, [Gedit], I transferred some of their themes over to MATLAB. These aren't a perfect match, since not all the same syntax options are available.

When I was trying to find the XML files defining the Gedit themes, I (unsurprisingly) found they were often based on themes for other editors. Here, I have attributed the author of the version I based my own on.

#### Oblivion
Based on the [Gedit theme, "Oblivion"](https://github.com/mig/gedit-themes/blob/master/oblivion.xml), by Paolo Borelli for GtkSourceView.

![Oblivion]({{ site.url }}/resources/matlab-scheme-screenshots/oblivion.png)

#### Cobalt
Based on the [GTK stylesheet], "Cobalt", by Will Farrington, which is also implmented as a Gedit theme.

![Cobalt]({{ site.url }}/resources/matlab-scheme-screenshots/cobalt.png)

#### Darkmate
Based on the [GTK stylesheet], "Darkmate", by [Luigi Maselli](https://grigio.org/), which is also implmented as a Gedit theme.

![Darkmate]({{ site.url }}/resources/matlab-scheme-screenshots/darkmate.png)

#### Tango
Based on the Gedit theme, "Tango". I found a copy of the Tango XML file for GMate, but curiously it didn't match the version I had in front of me on the screen. So I actually selected these out these settings using an on-screen colour-picker tool on the rendering of a `.m` file in Gedit.

![Tango]({{ site.url }}/resources/matlab-scheme-screenshots/tango.png)

#### Vibrant
Based on the [GTK stylesheet], "Vibrant", by Lateef Alabi-Oki, which is also implmented as a Gedit theme.

![Vibrant]({{ site.url }}/resources/matlab-scheme-screenshots/vibrant.png)


### Solarized themes

[Solarized] is a popular colour scheme created by [Ethan Schoonover] which has been adapted for many editors and environments. Because it is so possible, there are some other implementations available [(1)], [(2)], [(3)] -- most of which have arisen while this project was shelved -- but I believe mine follows the structure most faithfully.

Certainly it is the only one which defines all the colour preference options, including non-MATLAB syntax definitions.

#### Solarised Dark

![Solarized Dark]({{ site.url }}/resources/matlab-scheme-screenshots/solarized-dark.png)

#### Solarised Light

![Solarized Light]({{ site.url }}/resources/matlab-scheme-screenshots/solarized-light.png)


### Home-made MATLAB themes

#### Dark Steel

This is my own theme, a mash-up of Cobalt and Darkmate, and was the colour scheme I was originally trying to transfer between my MATLAB installations and motiviated the creation of *MATLAB Schemer*.

![Dark Steel]({{ site.url }}/resources/matlab-scheme-screenshots/darksteel.png)

#### Matrix

Colour schemes designed to mimic the very-green terminals from the universe of [*The Matrix*](http://www.imdb.com/title/tt0133093/) can be found for many editors. Often, these themes use only shades of pure green (`#000000` to `#00FF00`).

But rather than copy a pre-existing theme, what I decided to do was design my own, and restrict myself to only using colours which appear on the monitors within the movie (picked out with Gpick).

Consequently, you can be sure this theme is realistic, but these restrictions mean it may not be the most user-friendly option!

![Matrix]({{ site.url }}/resources/matlab-scheme-screenshots/matrix.png)


## Additional Features

There are a few clever tricks being used behind the scenes which most users won't notice if they are working correctly.

### Non-MATLAB Language Syntax Highlighting

Many users don't notice this since they only ever edit `.m` files, but MATLAB actually supports the highlighting of syntax in a selection of other languages.
- MuPAD (`.mu`), the symbolic mathematics product acquired by MathWorks
- TLC (`.tlc`), for working with Arduinos
- VRML (`.wrl`), for virtual reality modelling
- C/C++ (`.c`, `.cpp`, `.h`, `.hpp`), the long-standing, popular and efficient programming language(s) which you may be using to make `.mex` files for MATLAB
- Java (`.java`), the language in which MATLAB is written
- VHDL (`.vhd`, `.vhdl`), for hardware programming with parallel processing
- Verilog (`.v`), a hardware description language
- XML/HTML (many extensions), the mark-up languages used for some metadata and almost all webpages

I have noticed this myself when looking at the `.c` source of a MEX-file... MATLAB offers syntax highlighting for these languages but the colours used are partially coupled to general colour settings (background and text colour) and partially set specific for the language in question.

Consequently, if you've made your own theme and only set the colours for `.m` syntax highlighting, you'll find that the syntax for other languanges such as `.c` is broken.

Since we don't want to be imported broken themes in this way, *MATLAB Schemer* gets around this problem by having the syntax highlighting colours in these other languages inherit their values from the colours for related `.m` syntax highlighting. The result is that you can set-up a scheme using just `.m` highlighting and it will give a consistent experience in all the languages currently supported by MATLAB.

If you wish, you can still overwrite the inherited settings for the other languages by going to `Preferences > Editor/Debugger > Language`. This is also where you can enable more extensions to be recognised as a particular language.

### Preferences with limited availability

Over the years, MathWorks has added expanded the syntax highlighting options which are available.

If you're using an older version of MATLAB than the most up-to-date, *MATLAB Schemer* won't export the settings which don't exist in your version of MATLAB. Other users who import the theme you have designed will have the missing value filled-in with an inherited value in the same way as for the additional languages.


## Conclusion

Hopefully you find this utility for managing colour schemes for MATLAB useful and comprehensive.

If this tool improves your MATLAB experience and you're interested in donating to the project, you can [send a small weekly donation with Gratipay][gratipay] or [put a bounty on an issue][bountysource] to encourage further development.

If you find any problems with it, please open an issue on the [GitHub repository][matlab-schemer].


  [matlab-schemer]:     https://github.com/scottclowe/matlab-schemer
  [README]:             https://github.com/scottclowe/matlab-schemer#readme
  [matlab-schemes]:     https://github.com/scottclowe/matlab-schemes
  [fex]:                http://mathworks.com/matlabcentral/fileexchange/53862-matlab-schemer
  [flattr]:             https://flattr.com/submit/auto?user_id=scottclowe&url=https://github.com/scottclowe/matlab-schemer&title=MATLAB-schemer&tags=github&category=software
  [gratipay]:           https://gratipay.com/matlab-schemer/
  [bountysource]:       https://www.bountysource.com/teams/matlab-schemer
  [Undocumented Matlab article]: http://undocumentedmatlab.com/blog/changing-system-preferences-programmatically
  [GTK stylesheet]:     https://wiki.gnome.org/Projects/GtkSourceView/StyleSchemes
  [Solarized]:          http://ethanschoonover.com/solarized
  [Ethan Schoonover]:   http://ethanschoonover.com/
  [Gedit]:              https://wiki.gnome.org/Apps/Gedit
  [(1)]: https://github.com/Chrismarsh/matlab-solarized
  [(2)]: http://www.mikesoltys.com/2013/02/08/matlab-tip-change-the-color-scheme-to-be-easier-on-your-eyes/
  [(3)]: https://www.mathworks.com/matlabcentral/fileexchange/50446-benhager-solarized-matlab
