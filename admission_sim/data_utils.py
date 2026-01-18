"""
Data utilities removed.

The helper functions for loading/saving admissions data were removed from the
package to keep the core library focused on modeling and simulation. If you
need to load or save CSV data, use `pandas.read_csv` / `DataFrame.to_csv` or
implement project-specific utilities in your own scripts.

Example:

```python
import pandas as pd

df = pd.read_csv('admissions.csv')
```

"""
