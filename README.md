# :tv: kisskh-dl

<div align="center">
   <br>
   <strong><i>Fork of kisskh-dl - Simple downloader for kisskh.co using KissKH Api</i></strong>
   <br>
</div>

---

## Credits

This project is a fork of [kisskh-dl](https://github.com/debakarr/kisskh-dl) by [Debakar Roy](https://github.com/debakarr).

It uses the [KissKH Api](https://github.com/beorgsh/KissKH-Api) by [beorgsh](https://github.com/beorgsh) (forked by [cjayacopra](https://github.com/cjayacopra/KissKH-Api)) to fetch drama information and stream URLs.

---

## 💻 Installation

### Prerequisites

- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

### Install uv

```bash
# On macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

For more installation options, visit the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/kisskh-dl.git
cd kisskh-dl

# Install dependencies
uv sync
```

---

## 📚 Usage

After setting up, use the `kisskh dl` command to download shows from the command line.

> **Note**: Always use `uv run kisskh dl ...` from the project directory. This ensures the correct environment is used.

```console
uv run kisskh dl --help
Usage: kisskh dl [OPTIONS] DRAMA_URL_OR_NAME

Options:
  -f, --first INTEGER             Starting episode number.
  -l, --last INTEGER              Ending episode number.
  -q, --quality [360p|480p|540p|720p|1080p]
                                  Quality of the video to be downloaded.
  -s, --sub-langs TEXT            Languages of the subtitles to download.
  -o, --output-dir TEXT           Output directory where downloaded files will
                                  be store.
  --help                          Show this message in exit.
```

Here are some examples:

### 🔗 Direct download entire series in highest quality available in current folder

```bash
uv run kisskh dl "https://kisskh.co/Drama/Island-Season-2?id=7000" -o .
```

### 🔍 Search and download entire series in highest quality available in current folder

```bash
uv run kisskh dl "Stranger Things" -o .
1. Stranger Things - Season 4
2. Stranger Things - Season 1
3. Stranger Things - Season 2
4. Stranger Things - Season 3
Please select one from above: 1
```

### ⬇️ Download specific episodes with specific quality

> :exclamation: Note that if the selected quality is not available, it will try to get something lower than that quality. If that also is not available, it will try to get the best quality available.

Downloads episode 4 to 8 of `Alchemy of Souls` in 720p:
```bash
uv run kisskh dl "https://kisskh.co/Drama/Alchemy-of-Souls?id=5043" -f 4 -l 8 -q 720p -o .
```

Downloads episode 3 of `A Business Proposal` in 720p:
```bash
uv run kisskh dl "https://kisskh.co/Drama/A-Business-Proposal?id=4608" -f 3 -l 3 -q 720p -o .
```

You can also download single episode by providing the episode URL

```bash
uv run kisskh dl "https://kisskh.co/Drama/A-Business-Proposal/Episode-3?id=4608&ep=86439&page=0&pageSize=100" -o .
```

For more options, use the `--help` flag.

### 📖 Decrypting Subtitles

If you want to decrypt the downloaded subtitles, you need to pass the `--decrypt-subtitle` or `-ds` flag along with a decryption key and initialization vector. Check [#14](https://github.com/debakarr/kisskh-dl/issues/14).

Here is an example of how to pass these parameters from the command line:

```bash
uv run kisskh dl "<drama_url>" --decrypt-subtitle --key "your_key_here" --initialization-vector "your_iv_here"
```

You can also set these parameters as environment variables. If you set the `KISSKH_KEY` and `KISSKH_INITIALIZATION_VECTOR` environment variables, they will be used by default.

Here is an example of how to set these environment variables:

- On Linux/Mac:

```bash
export KISSKH_KEY="your_key_here"
export KISSKH_INITIALIZATION_VECTOR="your_iv_here"
```

- On Windows:

```cmd
set KISSKH_KEY="your_key_here"
set KISSKH_INITIALIZATION_VECTOR="your_iv_here"
```

After setting these environment variables, you can use the `--decrypt-subtitle` flag without passing the key and initialization vector explicitly:

```bash
uv run kisskh dl "Drama Name" --decrypt-subtitle
```

Please make sure to replace `"your_key_here"` and `"your_iv_here"` with your actual decryption key and initialization vector.

---

## 🐞 DEBUG

To enable debugging, use the `-vv` flag while running `kisskh dl`.

```bash
uv run kisskh -vv dl "https://kisskh.co/Drama/A-Business-Proposal?id=4608" -f 3 -l 3 -q 720p
```

---

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -v

# Update dependencies
uv sync --upgrade
```
