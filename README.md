# scottclowe.github.io

This is the source for my [personal website and blog](https://scottclowe.com).

It is served by [GitHub Pages](https://pages.github.com/) using [Jekyll](https://jekyllrb.com), the combination of which is detailed [here by Jekyll](https://jekyllrb.com/docs/github-pages/) and [here by GitHub](https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/).
There is also a guide on making a blog with GitHub Pages and Jekyll [here](http://jmcglone.com/guides/github-pages/), amongst others.

To render the site at the domain [scottclowe.com](https://scottclowe.com), I used an Apex Domain (`A`) DNS with the registrar to point the URL to the GitHub pages page corresponding to this repository (ordinarily at <http://scottclowe.github.io>).
Details on rendering the site at a custom domain name can be found on [GitHub's help pages](https://help.github.com/articles/using-a-custom-domain-with-github-pages/).

Incidentally, if you were to clone the source for this website, you could compile and browse the site locally using the command
```
bundle exec jekyll serve
```
(Although you may want to disable Disqus and Google Analytics beforehand, by commenting out their lines in `_config.yml`.)
Jekyll will tell you the local port at which you're serving the site, which should be something like http://127.0.0.1:4000/.
This all assumes you've [installed Jekyll using RubyGems](https://jekyllrb.com/docs/installation/).

The theme is a modified version of [*Beautiful Jekyll*](https://github.com/daattali/beautiful-jekyll) (see [demo](http://deanattali.com/beautiful-jekyll)) by [@daattali](https://github.com/daattali).

