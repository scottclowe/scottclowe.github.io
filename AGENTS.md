# AGENTS.md

## Build & Serve

```bash
bundle install                    # install dependencies
bundle exec jekyll serve          # local dev server at http://localhost:4000
bundle exec jekyll serve --future # include posts with future dates
```

Requires Ruby and Bundler. The gemspec (`beautiful-jekyll-theme.gemspec`) pins Beautiful Jekyll v6.0.1.

CI runs `bundle exec appraisal jekyll build` to test against both Jekyll 3.9.4 and 4.3.3 (see `Appraisals`).

## Architecture

Jekyll site using the **Beautiful Jekyll** theme (v6.0.1). Layout chain: `base.html` -> `default.html` -> `page.html` / `post.html` / `home.html`.

Key paths:
- `_config.yml` - site config (navbar, social links, colors, plugins)
- `_data/publications.yml` - **primary data file** for the publications page
- `publications.md` - publications page (Liquid static fallback + JS client-side rendering)
- `_layouts/` - layout templates
- `_includes/` - partials
- `_posts/` - blog posts
- `.github/workflows/ci.yml` - GitHub Actions CI

## Publications (`_data/publications.yml`)

Most common edit. Each entry follows this schema:

```yaml
- date: '2025'           # Year string (quoted), used for display and sorting
  title: 'Paper Title'
  venue: 'Conference or Journal Name'
  authors: First Last, Second Author, Third Author  # plain text, commas between
  topics:                # list of lowercase topic tags for filtering
  - optimization
  - vision
  main_link: https://...          # primary URL (title links here)
  links:                          # named links shown as buttons
    arXiv: https://arxiv.org/abs/...
    openreview: https://...
    code: https://github.com/...
    poster: https://...
  thumbnail: ''                   # optional image path
  summary: ''                     # optional short description
  highlighted: 6                  # optional integer; lower = higher priority in highlighted section
  bibtex: |                       # literal block scalar
    @inproceedings{Key2025_ShortName,
        title = {Title with {P}roper {N}ouns in braces},
        author = {First Last and Second Author},
        year = {2025},
        booktitle = {Conference Name},
        url = {https://...},
    }
```

Thumbnails: generate with `python make_thumbnail.py <source-figure> <CitationKey>` (add `--jpeg` for photos). It crops to content, downscales to <=240px (the thumbnail slot size, so it displays 1:1), and compresses into `img/publications/`; it also writes a <=1200px copy to `img/publications/hires/` (same filename), which `publications.md` serves to high-density screens via `srcset` (matched by filename stem, so a missing hi-res copy just falls back to the 240px one). Use `--hires-only` to add a hi-res copy for an existing thumbnail. Source figures live in `_thumbnail_candidates/<CitationKey>/` (gitignored). Needs `pip install pyoxipng` for full compression.

Entries are ordered newest-first in the YAML file. The JS on `publications.md` provides topic filtering, highlight grouping, BibTeX copy/download. The Liquid template renders a static fallback for non-JS browsers.

### Author notation

- `*` suffix = equal contribution (e.g., `Author A*, Author B*`)
- `†` suffix = equal senior/advising (e.g., `Author X†, Author Y†`)

### BibTeX conventions

- Protect capitalization with braces: `{SOAP}`, `{K}ullback`
- Use `month = sep` style (three-letter lowercase, no braces), with spaces around `=`
- Trailing comma after last field
- 4-space indentation for fields
- Citation key format: `AuthorYEAR_ShortName` (e.g., `Lin2026_KLShampoo`)

### Topic tags

Reuse existing tags where possible. Current tags include: `optimization`, `vision`, `biodiversity`, `insect`, `DNA`, `language`, `self-supervised learning`, `dataset`, `music`, `image segmentation`, `hierarchical`, `multimodal`.
