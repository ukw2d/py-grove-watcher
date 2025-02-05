<div align="center">

  <img src="assets/logo.png" alt="logo" width="200" height="auto" />
  <h1>GroveWatcher</h1>
  
  <p>
    Tree-Sitter grammar fetcher for Python.
  </p>

  
<!-- Badges -->
<p>
  <a href="https://pypi.python.org/pypi/grove-watcher">
      <img src="https://img.shields.io/pypi/v/py-grove-watcher.svg" 
      alt="forks" />
    </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/ukw2d/py-grove-watcher" 
    alt="last update" />
  </a>
  <a href="https://github.com/ukw2d/py-grove-watcher/network/members">
    <img src="https://img.shields.io/github/forks/ukw2d/py-grove-watcher" 
    alt="forks" />
  </a>
  </a>
  <a href="https://github.com/ukw2d/py-grove-watcher/issues/">
    <img src="https://img.shields.io/github/issues/ukw2d/py-grove-watcher" alt="open issues" />
  </a>
  <a href="https://github.com/ukw2d/py-grove-watcher/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/ukw2d/py-grove-watcher.svg" 
    alt="license" />
  </a>
</p>
   
<h4>
    <a href="https://github.com/ukw2d/py-grove-watcher">Documentation</a>
  <span> · </span>
    <a href="https://github.com/ukw2d/py-grove-watcher/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/ukw2d/py-grove-watcher/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# Table of Contents

- [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
    - [Tech Stack](#tech-stack)
    - [Features](#features)
    - [Configuration](#configuration)
      - [Environment Variables](#environment-variables)
      - [Config files](#config-files)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgements](#acknowledgements)
  

<!-- About the Project -->
## About the Project
<!-- TechStack -->
### Tech Stack

<ul>
    <li><a href="https://www.python.org">Python</a></li>
    <li><a href="https://github.com/tree-sitter/py-tree-sitter">Py-Tree-Sitter</a></li>
    <li><a href="https://pydantic.dev">Pydantic</a></li>
  </ul>

<!-- Features -->
### Features

- **Automated Grammar Installation**: Easily install Tree-Sitter language grammars via `pip` by simply specifying the language name.
- **Virtual Environment Support**: Optionally use a dedicated virtual environment to cache grammar installations, ensuring isolation and reproducibility.
- **Pydantic Validation**: Ensure that only valid Tree-Sitter `Language` and `Parser` objects are returned from installed grammar modules.

<!-- Env Variables -->
### Configuration

#### Environment Variables

`.env` is used to store default path values required for the optional dedicated venv that is used for grammar (pip packages) caching.

- `CACHE_DIR_WIN32` - Path to the optional dedicated venv directory for Windows platform

- `CACHE_DIR_UNIX` - Path to the optional dedicated venv directory for Unix platforms

- `VENV_EXECUTABLE_WIN32` - Path to the optional dedicated venv Python executable for Windows platform

- `VENV_EXECUTABLE_UNIX`  - Path to the optional dedicated venv Python executable for Unix platforms

- `VENV_EXECUTABLE_DEFAULT_EXECUTABLE` - Python executable name used for the optional dedicated venv


#### Config files
`src/grove_watcher/config/config.json` - json used for pip packages prefixes. As per naming convention of the tree_sitter grammar pip packages. There is only 1 value there for now which should be enough.

`src/grove_watcher/config/logging.json` - json used for logging configuration. You can change the values as per your requirements.


<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites

- **Python** : Ensure you have Python 3.6 or higher installed.

- **Python venv** - Optional, but highly recommended.

<!-- Installation -->
### Installation

Package has been published to PyPI, so you can install it using pip:

```bash
  pip install grove-watcher
```
This package will install 3 dependencies:
- `tree-sitter` - for creating grammar objects based on imported grammar modules
- `pydantic` - for grammar objects validation
- `pydantic-settings` - for config validation and dynamic path fetching

<!-- Usage -->
## Usage

After installation, you can use it simply like this:

```python
import grove_watcher

parser = grove_watcher.find("python")
```
If you prefer not to install grammar packages in your current environment, pass the `use_venv` parameter as `True`:

```python
import grove_watcher

parser = grove_watcher.find("python", True)
```
This will create a dedicated virtual environment in the cache directory (the path can be configured in the `.env` file). This virtual environment is used for installing grammar modules from `pip` and retrieving the Tree-Sitter grammar object for your current environment. Subsequent calls with `use_venv=True` will reuse the existing virtual environment if it's available.

That's it! Hope this module saves you time and reduces your code complexity. 😊

<!-- Contributing -->
## Contributing
Contributions are always welcome!

See `contributing.md` for ways to get started.

<!-- License -->
## License

Distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for more information.

<!-- Contact -->
## Contact

Vlad Andreev - ukw2d@outlook.com


<!-- Acknowledgments -->
## Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

 - [Tree-Sitter](https://tree-sitter.github.io/tree-sitter/)
 - [Tree-Sitter Python Bindings](https://github.com/tree-sitter/py-tree-sitter)
 - [Pydantic](https://github.com/pydantic/pydantic)
 - [Shields.io](https://shields.io/)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
