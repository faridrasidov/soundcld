<div align="center">
  <h1>SoundCld</h1>
  <p>
      Python API handler for the SoundCloud Internal V2 API,
      allowing interaction without an API key.
  </p>

<!-- Badges -->

<a href="https://github.com/faridrasidov/soundcld" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=faridrasidov&message=soundcld&color=white&logo=github" alt="faridrasidov - soundcld"></a>
<a href="https://github.com/faridrasidov/soundcld/actions/workflows/ci.yml"><img src="https://github.com/faridrasidov/soundcld/actions/workflows/ci.yml/badge.svg" alt="soundcld - CI Tests"></a>

<a href="https://github.com/faridrasidov/soundcld"><img src="https://img.shields.io/github/stars/faridrasidov/soundcld?style=social" alt="stars - soundcld"></a>
<a href="https://github.com/faridrasidov/soundcld"><img src="https://img.shields.io/github/forks/faridrasidov/soundcld?style=social" alt="forks - soundcld"></a>
</div>

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Specifications](#specifications)
- [Authentication](#authentication)
- [License](#license)


<a name="installation"></a>
## Installation:
**Global Installation**
```shell
$ git clone https://github.com/faridrasidov/soundcld
$ cd soundcld
$ pip install .
```
**Virtual Environment**
```shell
$ git clone https://github.com/faridrasidov/soundcld
$ cd soundcld
$ path/to/your/venv/pip install .
```

<a name="usage"></a>
## Usage
```python
from soundcld import SoundCloud

sc = SoundCloud(auth=False, auto_id_gen=False)
assert sc.is_client_id_valid()
search = sc.get_search_all("GRXGVR")
for item in search:
    print(item.permalink, item.kind)
```

<a name="specifications"></a>
## Specifications

- **You Can Change Your Profile Info**
- **45 Get Api Requests Has Been Handled.(Some Of Them Require Auth)**
- **7 Put Api Requests Has Been Handled. (All Of Them Require Auth)**
- **1 Post Api Requests Has Been Handled. (All Of Them Require Auth)**
- **2 Delete Api Requests Has Been Handled. (All Of Them Require Auth)**
- **Last Valid Generated ID's Automatically Added To 'data.json' File To improve Api Speed.**


<a name="authentication"></a>
## Authentication
**Notes about `auth`:**

**Some methods require authentication. If you want to use them, you should get the values 
written at the bottom from your cookies and put them in file which is in package folder ("soundcloud") 
named cookies.json. You will also need to change your "client_id" in data.json file in that folder.**

**Save Them Into:**

**`package_root/soundcld/`**

**cookies.json:**
```json
{
  "moe_uuid": "<moe_uuid>",
  "oauth_token": "<oauth_token>",
  "sc_anonymous_id": "<sc_anonymous_id>",
  "datadome": "<datadome>"
}
```

**data.json (this file automatically generates when you get instance):**
```json
{
  "user_id": "<user_id>",
  "client_id": "<client_id>",
  "app_version": "<app_version>"
}
```

<a name="license"></a>
## License
`Soundcld` source code is licensed under the terms of the Boost Software License. See [LICENSE](https://github.com/faridrasidov/soundcld/blob/master/LICENCE.txt) for more information.