Here are the instructions:

-----

**Task**

Add rejection list filtering to the normalization pipeline, create the stewardship folder structure, and create an archive utility for processed queues.

**Part 1: Create stewardship folder structure**

**Step 1: Create folder structure**

Create the following folders under data/stewardship/:

data/stewardship/archive/

data/stewardship/rejection_lists/

data/stewardship/provisional/

**Step 2: Create initial rejection list file**

Create an empty os_rejection_list.csv in data/stewardship/rejection_lists/.

Columns: raw_os_string, rejection_reason, rejected_date

Leave it empty for now. It will be populated during stewardship review.

**Step 3: Add paths to settings.yaml**

Add stewardship paths to settings.yaml under a stewardship key:

stewardship_queue_path: path to stewardship_queue.json

archive_path: path to archive folder

rejection_list_path: path to os_rejection_list.csv

provisional_path: path to provisional folder

Use relative paths consistent with existing path conventions.

**Part 2: Add rejection list filtering**

**Step 4: Create rejection list loader**

Create a utility function or class to load the rejection list.

Location: Could be in stewardship folder or a utils module.

Function: load_rejection_list(path) returns a set of raw_os_strings that are rejected.

Load the CSV file. Extract raw_os_string column. Return as a set for fast lookup.

If file is empty or does not exist, return empty set.

**Step 5: Update normalization pipeline to filter rejections**

In the normalization pipeline, after matching is complete and before writing to stewardship queue:

Load the rejection list using the loader.

Filter the incomplete matches dataframe.

Remove any rows where raw_os_string is in the rejection list.

Only write non-rejected incomplete matches to stewardship_queue.json.

**Step 6: Log rejection filtering**

Log how many items were filtered out due to rejection list.

Example: “Filtered 15 rejected OS strings from stewardship queue”

**Part 3: Create archive utility**

**Step 7: Create archive function**

Create a utility function to archive the processed stewardship queue.

Location: Could be in stewardship folder or a utils module.

Function: archive_stewardship_queue(queue_path, archive_path)

**Step 8: Implement archive logic**

Check if stewardship_queue.json exists. If not, log and return.

Generate a timestamp string. Format: YYYYMMDD_HHMMSS

Create archive filename: stewardship_queue_YYYYMMDD_HHMMSS.json

Copy the queue file to archive folder with timestamped name.

Delete or clear the original queue file.

Log the archive action: “Archived stewardship queue to stewardship_queue_20241215_143022.json”

**Step 9: Create archive script or CLI command**

Create a simple script that can be run manually to archive the queue.

Takes no arguments. Uses paths from settings.yaml.

User runs it after completing stewardship review.

Example: python -m canonix.stewardship.archive_queue

Or a simple script: scripts/archive_stewardship_queue.py

**Part 4: Testing**

**Step 10: Test rejection list filtering**

Create a test rejection list with a few raw_os_strings.

Run normalization pipeline with data that includes rejected strings.

Verify rejected strings do not appear in stewardship_queue.json.

Verify non-rejected incomplete matches do appear.

**Step 11: Test archive utility**

Create a test stewardship_queue.json with sample data.

Run the archive function.

Verify file is moved to archive folder with timestamp.

Verify original queue is cleared or deleted.

**Step 12: Test empty rejection list**

Run with empty rejection_list.csv.

Verify pipeline still works.

Verify all incomplete matches go to stewardship queue.

**Step 13: Test missing rejection list**

Delete or rename the rejection list file.

Run pipeline.

Verify pipeline handles gracefully (empty set, no filtering).

Log warning that rejection list not found.

**Rules**

Work one step at a time. Show me after each step. Keep utilities simple and focused. Use existing path conventions from settings.yaml.

**Do not**

Do not automate the full stewardship workflow yet. Only add rejection filtering and archive utility. Do not create frontend or review UI. That is a future phase.

-----

Does that cover it?​​​​​​​​​​​​​​​​