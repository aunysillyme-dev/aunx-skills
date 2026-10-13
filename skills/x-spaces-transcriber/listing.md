## Name

X Spaces Transcriber: Twitter Spaces to Text

## Summary

Teach your agent to turn a recorded X Space into a timed transcript with observed speaker labels using space-tape.

## Price

Free ($0). Not part of the bundle.

## Full description

A Spaces replay is easier to search, quote, and review when you have its words in a file. X Spaces Transcriber guides your agent through installing the open-source space-tape CLI and using it on a public recorded X Space or the tweet that links the replay.

The skill explains the detail that matters for speaker labels: preserve the original replay until its Hydra metadata has been parsed. It also tells your agent to keep the original X link, inspect the files actually written, and report unknown speakers or an unavailable replay clearly.

It is for researchers, writers, community hosts, and anyone collecting notes from recorded Spaces. You get instructions for your agent, not a hosted transcription service. Python, ffmpeg, space-tape, and its dependencies are separate installations. Transcription may need a replay download and a first-time model download.

## Use cases

- Turn a public recorded Twitter Space into searchable notes.
- Collect timestamped quotes while keeping the original source link.
- Review speaker labels supplied by the replay's metadata.
- Install space-tape and check its command-line help.
- Prepare transcript files for your own follow-up writing or research.

## Demo request

"Install space-tape from an available local source checkout without network access. Run its help command and report installation and help outcomes. This is a setup demonstration only; do not download or transcribe a replay."

Request saved in `demos/x-spaces-transcriber/request.md`.

## Demo result

Real offline setup run: Python 3.11 virtual-environment creation exited 0. Installing the local package with `pip install --no-index --no-cache-dir --no-deps --no-build-isolation ./local-source` exited 0 and reported `Successfully installed space-tape-0.1.0`. Running `space-tape --help` exited 0 and listed `transcribe`, `hydra`, `clip`, and `highlights`.

The first attempt used Python 3.14 and failed with `Cannot import 'setuptools.build_meta'`; the help entry point was consequently absent. The Python 3.11 retry succeeded. Both attempts' complete logs are retained with local paths sanitized. Dependencies were not installed by this demo. The copied source and virtual environment were removed afterward.

This demo shows setup and help only. Replay downloads, model downloads, transcript accuracy, and speaker-label accuracy were not tested. Evidence: `demos/x-spaces-transcriber/result.json`, `install-retry.txt`, and `help-retry.txt`.

## FAQ

### How do I transcribe an X Space with an AI agent?

Give your agent this skill and a public recorded Space URL. It uses space-tape to download the replay and produce transcript files, subject to available dependencies and network access.

### Does this work with Twitter Spaces links?

The documented CLI accepts X Spaces URLs and corresponding twitter.com links, including announcement tweets with a replay.

### Can I get speaker names in a Twitter Spaces transcript?

space-tape reads speaker metadata from the raw replay. If those tags are absent, the skill tells the agent to report unknown speakers rather than invent names.

### What do I need to install for space-tape?

Python 3.10 or later, ffmpeg, and the space-tape Python package with its declared dependencies. The upstream repository has the installation command.

### Do I need an X API key to transcribe a recorded Space?

The upstream workflow does not require an X API key. Replay availability and changes to download behavior can still affect a run.

### Does the free skill include a transcription service?

It includes agent instructions. Your environment runs the separately installed open-source CLI, downloads any needed models, and stores outputs locally.

### Was the demo a real transcription?

The demo was a real offline install-and-help check. It did not download or transcribe a replay.

## Keywords

X Spaces transcription, Twitter Spaces transcript, transcribe X Space, space-tape, speaker labels, timestamped transcript, recorded Spaces, Whisper transcription, AI agent skill, Spaces replay, transcript CLI, Python transcription

## Tags

ai-agents, research, writing, documentation, developer-tools, python

## Compatibility

Claude Code, Codex CLI, Cursor, Gemini CLI, and any agent that reads SKILL.md and can run shell commands. Transcription requires Python 3.10 or later, ffmpeg, installed space-tape dependencies, and access to the replay and required model files. A text-only agent can explain the steps but cannot execute the CLI.

## Permissions notes

The skill itself makes no network calls. When asked to install or transcribe, the agent runs external commands: pip may fetch code and dependencies, and space-tape may download a public X replay and uncached model weights. It reads the supplied link and downloaded audio, writes transcript and audio files to the chosen output directory, and may populate package and model caches. Installation writes to the selected Python environment. The offline demo made no network calls and retained only sanitized logs after cleanup.

## Credits

**hovtgc and contributors** created [space-tape / x-spaces-transcription](https://github.com/hovtgc/x-spaces-transcription), MIT License. This skill uses the documented CLI commands and technique for preserving Hydra metadata. [Auny's public fork](https://github.com/aunysillyme/x-spaces-transcription) is also MIT-licensed. No upstream implementation code is shipped inside this skill pack.

space-tape uses [Whisper by OpenAI](https://github.com/openai/whisper) and [Whisper large-v3 model weights](https://huggingface.co/openai/whisper-large-v3). space-tape's documentation identifies the weights as Apache-2.0. The setup demo did not download or run the model.

## Repo link

https://github.com/aunysillyme-dev/aunx-skills/tree/main/skills/x-spaces-transcriber
