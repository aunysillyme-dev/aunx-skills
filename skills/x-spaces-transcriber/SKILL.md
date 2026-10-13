---
name: x-spaces-transcriber
description: Transcribe a recorded X Space or Twitter Space with timestamps and speaker labels using the open-source space-tape CLI. Use for requests to turn an X Spaces replay or its announcement tweet into a transcript, or to install and check space-tape.
---

# X Spaces Transcriber

## When to use

Use when the user supplies a public recorded X Space, a tweet linking its replay, or asks to set up space-tape. Work within the user's approved download and output locations.

## Steps

1. If setup is needed, check Python 3.10 or later and `ffmpeg`. Install space-tape in the user's chosen Python environment with the upstream command:

   ```sh
   pip install git+https://github.com/hovtgc/x-spaces-transcription.git
   ```

   If network access is unavailable, use an authorized local checkout for an offline setup check. Report dependency or build-tool gaps rather than claiming installation succeeded.

2. Run `space-tape --help` to confirm that the entry point starts. If setup alone was requested, report that result and stop.
3. If transcription was requested, accept `x.com/i/spaces/<id>`, `x.com/<user>/status/<id>`, and corresponding `twitter.com` links. Run the upstream command with the supplied URL:

   ```sh
   space-tape transcribe "$URL" -o ./out
   ```

   For an English replay when the user chooses a smaller model, use the documented form:

   ```sh
   space-tape transcribe "https://x.com/user/status/123" --model openai/whisper-small.en
   ```

   The example URL is a placeholder; replace it with the user's link. Downloading the replay and uncached model weights requires network access.

4. Keep the original downloaded `.m4a` or `.ts` until Hydra speaker metadata has been parsed. If handling audio manually, parse the raw replay before converting a copy: remuxing or transcoding can remove its speaker tags. The CLI performs this sequence for transcription.
5. Wait for command completion, retain its exit code, and inspect the output directory. Report which of `cues.json`, `transcript.md`, `audio.mp3`, and `highlights.json` actually exist. Preserve the original X URL in the transcript.
6. If speaker tags are absent or speakers are reported as `unknown`, state that limitation. If the replay is unavailable, stop and report the download result. A help check does not prove replay download or transcription works.

## Output shape

Return the command outcome, source URL when provided, output paths, and any speaker or replay limitations. For setup, return the installation result and help result separately. For transcription, include a short excerpt from the actual transcript only after reading it.

## Conditions and actions

- If the Space is live or private, request a public recorded replay before using this workflow.
- If a command fails, report its error and the stage reached. Do not fabricate transcript text or labels.
- If Hydra metadata is missing, report unknown speakers; do not infer identities from a voice.
- If the user requests setup only, stop after the install/help check.
- If output files exist, keep the source link with them and attribute the Space to its source.

## Examples

Request: "Install space-tape and check that the command opens."
Action: install in the chosen environment, run `space-tape --help`, and report both exit codes. State that no transcription was tested.

Request: "Transcribe this recorded X Space with speaker labels."
Action: run `space-tape transcribe "$URL" -o ./out`, read the completed outputs, and report timestamps, observed labels, paths, and the original link.

## Credits

This skill teaches commands and replay-handling techniques from **space-tape**, created by **hovtgc** and contributors: [hovtgc/x-spaces-transcription](https://github.com/hovtgc/x-spaces-transcription), MIT License. It also references [Auny's public fork](https://github.com/aunysillyme/x-spaces-transcription), MIT License. No upstream implementation code is bundled in this pack.

space-tape uses [Whisper by OpenAI](https://github.com/openai/whisper), including [Whisper large-v3 weights](https://huggingface.co/openai/whisper-large-v3). Its documentation identifies those weights as Apache-2.0. Model downloads are separate from this pack and were not exercised by the setup demo.
