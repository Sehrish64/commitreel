# 🎬 commitreel

**Turn your Git commit history into a video, in one command.**

```bash
commitreel https://github.com/you/your-repo
```

> 📽️ Add your demo GIF here: `![demo](demo.gif)`

Your commits are a story: the first "initial commit", the late-night "fix", the legendary "final final FINAL fix". commitreel types them out one by one in a vertical video made for YouTube Shorts, Reels and TikTok.

## Quick start

You need **Python 3.9+**, **git**, and **[ffmpeg](https://ffmpeg.org/download.html)**.

```bash
git clone https://github.com/Sehrish64/commitreel
cd commitreel
pip install -e .
commitreel https://github.com/you/your-repo -n 20 -o my-video.mp4
```

Works with a local folder too:

```bash
commitreel . -n 15
```

## Options

| Option | What it does | Default |
|---|---|---|
| `-n, --limit` | How many commits to show | 20 |
| `--first` | Use the *first* n commits instead of the latest | off |
| `-o, --output` | Output video file | `commitreel.mp4` |
| `--size` | Video size (`WIDTHxHEIGHT`) | `720x1280` |
| `--fps` | Frames per second | 12 |
| `--keep-frames` | Keep the PNG frames | off |

## Roadmap

- [ ] 🎵 Turn commit messages into a song (lyrics + music)
- [ ] 🔊 Text-to-speech voiceover
- [ ] 🎨 Themes (retro terminal, neon, light)
- [ ] 🌍 Multi-language captions (Roman Urdu, Hinglish...)
- [ ] 📈 Show files changed and lines added per commit

Ideas and pull requests are welcome!

## License

MIT
