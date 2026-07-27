Organize an Ableton Ideas folder for the Buried Landscapes project.

The user will name a folder containing .als files, e.g. "/organize ~/Ableton/Buried_Landscapes/Ideas".

Run:

```
python3 scripts/organize_project.py <folder> [--dry-run]
```

This moves each .als file into its own named subfolder with standard subfolders inside (`Samples/Recorded`, `Samples/Imported`, `Samples/Bounces`, `Versions`).

This reorganizes files on disk. If the user didn't explicitly say to just preview, or if this is the first time organizing this folder, run with `--dry-run` first and show the user what would happen before running for real. Only run without `--dry-run` if the user confirms or has clearly already reviewed the plan.

After running, tell the user what was moved/created (or, for a dry run, what would be).

Arguments: $ARGUMENTS
