# KhorosJX Python Library
The  **khorosjx**  library acts as a Python software development kit (SDK) to administer and manage  [Khoros JX](https://community.khoros.com/t5/Atlas-Insights-Blog/Lithium-and-Jive-x-It-s-Official/ba-p/325465)  (formerly  [Jive-x](https://www.prnewswire.com/news-releases/lithium-technologies-completes-acquisition-of-external-online-community-business-from-jive-300531058.html)) and  [Jive-n](https://www.jivesoftware.com/)  online community platforms.

## Installation
The package can be installed via pip using the syntax below.

``` sh
pip install khorosjx
```

You may also clone the repository and install from source using the syntax below.

```sh
git clone git://github.com/jeffshurtliff/khorosjx.git
cd khorosjx/
python setup.py install
```

## Change Log
The change log is located in the documentation here: [https://khorosjx.readthedocs.io/en/latest/changelog.html](https://khorosjx.readthedocs.io/en/latest/changelog.html)

## Usage
This section provides basic usage instructions for the package.


### Importing the package
The package can be imported into a Python script using the syntax below.

``` python
import khorosjx
```

### Initializing the modules
While it is certainly possible to import modules directly (e.g. ``from khorosjx import users``), it is recommended that you instead leverage the ``init_module()`` function as shown below.

``` python
khorosjx.init_module('content', 'users')
```

In the example above, both the ``khorosjx.content`` and the ``khoros.users`` modules have been initiated.

>**Note:** It is not necessary to import the ``khorosjx.core`` module as it is imported by default.

### Establishing the API connection
Before leveraging the API in function calls, you must first establish your connection by providing the base URL for the environment (e.g. ``https://community.example.com``) and the username and password for the unfederated service account through which the API calls will be made. This is demonstrated below.

``` python
base_url = 'https://community.example.com'
credentials = ('adminuser', 'password123!')
khorosjx.core.connect(base_url, credentials)
```

>**Note:** At this time the library only allow connections using [basic authentication](https://developers.jivesoftware.com/api/v3/cloud/rest/index.html#authentication), but there are plans to include the ability to leverage  [OAuth 2.0](https://developers.jivesoftware.com/api/v3/cloud/rest/AuthorizationEntity.html)  in a future release.

Once the connection has been established, you can proceed to leverage the library of functions in the various modules as needed.

## Requirements
The following packages are leveraged within the khorosjx package:
* numpy 1.17.4
* pandas-0.25.3
* python-dateutil 2.8.1
* pytz 2019.3
* requests 2.22.0
* urllib3 1.25.7

The full requirements list can be foune in the [requirements.txt](https://github.com/jeffshurtliff/khorosjx/blob/master/requirements.txt) file.

## Documentation
The documentation is located here: [https://khorosjx.readthedocs.io/en/latest/](https://khorosjx.readthedocs.io/en/latest/)

## License
[MIT License](https://github.com/jeffshurtliff/khorosjx/blob/master/LICENSE)

# Reporting Issues
Issues can be reported within the [GitHub repository](https://github.com/jeffshurtliff/khorosjx/issues).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by the [Khoros](https://www.builtinaustin.com/company/khoros) or [Aurea Software, Inc.](https://www.jivesoftware.com/) companies.