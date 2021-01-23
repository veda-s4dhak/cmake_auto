<h2> Summary: </h2>

Automatic CMake Generation Tools<br>

<h2> Sample: CMake Executable: </h2>

```
import os

from cmake_auto.CMakeAutoEXE import CMakeAutoEXE

# Configuration
cmake_config = dict()
cmake_config['proj_name'] = 'okane_crypt'
cmake_config['proj_dir'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
cmake_config['version'] = '0.01'
cmake_config['cmake_version'] = '3.15'
cmake_config['exclude_folders'] = ['tfm', 'port']

# Generate CMake
cme = CMakeAutoEXE(**cmake_config)
cme.run()
```

<h2> Contacts: </h2>

- a22agarw@outlook.com
