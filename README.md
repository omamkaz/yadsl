
# Yemen Net ADSL Internet Info

yadsl is a simple Python module to easily fetch data from [YemenNet ADSL](https://adsl.yemen.net.ye) official website.

## Features

- **easy to use** fetch data easily with Python.
- **cookies** import & export cookies, for long refresh time without captcha verify

## Installation

You can install **yadsl** via pip:

```bash
pip install yadsl
```

## Usage

```python
from yadsl import YADSL

yadsl = YADSL(
    user: str = "xxxxxx",
    password: str = "..."
)

yadsl.login()
yadsl.fetch_captcha()
yadsl.verify(captcha: str = "xxxx")
yadsl.fetch_data(cookies: dict = None)
```

## License

This project is licensed under the [GPL3 License](https://github.com/omamkaz/yadsl/blob/main/LICENSE).
