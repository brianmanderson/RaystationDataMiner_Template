# RaystationDataMiner_Template

A template for evaluating patient data exported from RayStation. It shows how to load
previously exported RayStation patient databases (via the
[AbstractInfoStructure](https://github.com/brianmanderson/AbstractInfoStructure)
submodule), filter patients of interest, and iterate their plans and ROIs — without
touching RayStation itself. Copy this repo and adapt `Main.py` to your own question.

## How it works

`Main.py` walks through the typical mining workflow:

1. Sync exported database files from a network share to a local folder
   (`update_database`) — edit `network_path` and `local_db_path` for your environment.
2. Load lightweight patient headers from all databases
   (`PatientHeaderDatabases.build_from_folder`), optionally restricted to a list of MRNs.
3. Drop unapproved patients and pre-filter by ROI name/type
   (`identify_wanted_headers`, e.g. organ `parotid_r`); a helper also lists unique
   ROI names across databases with optimization/PTV-style structures screened out.
4. Load the full patient data only for the filtered headers
   (`return_patient_databases`), deduplicate patients that appear in multiple yearly
   databases (keeping the most recent), then iterate approved treatment plans and the
   ROIs on their referenced examinations.

## Requirements

- Python with `tqdm`
- The `AbstractInfoStructure` git submodule (clone with
  `git clone --recurse-submodules`), which provides `EvaluationTools`,
  `PatientHeaderDatabases`, and the related data classes
- Access to a folder of databases exported by the companion RayStation data
  structure/export tooling

## Usage

```bash
git clone --recurse-submodules https://github.com/brianmanderson/RaystationDataMiner_Template
# edit the paths and filter criteria in Main.py, then
python Main.py
```

Template/example code with site-specific paths; adapt before use.
