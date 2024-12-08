# anki-liberator

## What

`anki-liberator` is an add-on for Anki Desktop to avoid pattern-matching your way through review. It takes the prompt & answer of a flashcard and feeds them to an LLM to get a variation on the prompt.

For example:

**Original prompt**: `🇩🇪lediglich`

**Original answer**: `🇩🇪merely, only, simply`

**Generated variation**: `What does _lediglich_ mean in the following sentence? _Er wollte lediglich helfen, aber niemand hat auf ihn gehört`

## Why

A common issue with flashcards is that the brain starts answering based on the pattern of the question, as opposed to truly understanding or remembering the contents of the answer. This is particularly common with repetitive cards like language-based ones. `anki-liberator` is used to break those patterns.

## Usage

You will need to add your own Claude API key to the add-on's [settings](https://docs.ankiweb.net/addons.html).

The add-on exposes a few different settings (e.g. temperature, model used, base prompt). In order for it to work you will need to provide your own API key for Claude.

## Development

The add-on allows you to alter the base prompt, so it should be flexible enough to support a wide variety of decks. Still, it's something I created for my own benefit and share on the off-chance somebody else might find it useful.

