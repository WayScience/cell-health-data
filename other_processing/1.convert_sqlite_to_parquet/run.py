import pathlib
import sqlalchemy
import sqlite_clean as sc
import cytotable

sqlite_files = list(pathlib.Path("../0.download-profiles-from-figshare/data/").glob("*.sqlite"))
data = sqlite_files[-1]

# trying on a single file (10GB)
cytotable.convert(source_path=str(sqlite_files[-1]),
                    dest_path="cell_health_parquet/test.parquet",
                    dest_datatype="parquet",
                    source_datatype="sqlite",
                    preset="cellprofiler_legacy")