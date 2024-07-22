
<div align="center">
  <h1>SoundCld</h1>
  <p>
    Python Api Handler For The Internal V2 SoundCloud API. Does Not Require An API Key.
  </p>

<!-- Badges -->

<a href="https://github.com/faridrasidov/soundcld" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=faridrasidov&message=soundcld&color=purple&logo=github" alt="faridrasidov - soundcld"></a>
<a href="https://github.com/faridrasidov/soundcld"><img src="https://img.shields.io/github/stars/faridrasidov/soundcld?style=social" alt="stars - soundcld"></a>
<a href="https://github.com/faridrasidov/soundcld"><img src="https://img.shields.io/github/forks/faridrasidov/soundcld?style=social" alt="forks - soundcld"></a>

**Written On**

![Python](https://img.shields.io/badge/Python-black?style=for-the-badge&logo=Python&logoColor=000&labelColor=fff)

**Tests**

![Python](https://img.shields.io/badge/tox-black?style=for-the-badge&logo=testcafe&logoColor=000&labelColor=fff)


</div>

****

**Example Of Usage:**
```python
from soundcld import SoundCloud

sc = SoundCloud()
assert sc.is_client_id_valid()
search = sc.get_search_all("GRXGVR")
for item in search:
    print(item.permalink, item.kind)
```

**Specifications:**

- **Last Valid Generated ID's Automatically Added To 'data.json' File To improve Api Speed.**
****
**Notes about `auth_token`:**

**Some methods require authentication in the form of an OAuth2 access token. You can find your token in your browser cookies for SoundCloud under the name "oauth_token". A new token will be generated each time you log out and log back in.**
