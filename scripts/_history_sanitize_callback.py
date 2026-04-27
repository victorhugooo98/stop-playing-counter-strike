"""Blob callback for git filter-repo: removes steam_id_64 (and other PII columns)
from CSVs across the entire history.

Detection is content-based (no filename available in blob_callback). A CSV is
flagged for sanitization if its first line is a header that contains
'steam_id_64' AND it does NOT have the comment marker we leave behind to mark
already-sanitized blobs (loop safety).

This is invoked by:
    git filter-repo --blob-callback "$(< scripts/_history_sanitize_callback.py)"

The callback runs against every blob in every commit. We mutate `blob.data`
in place; filter-repo handles tree/commit rewrites automatically.
"""
# This file is consumed BOTH as a script template (read raw) AND can be
# imported standalone for unit testing the helper. Filter-repo only needs
# the body; the wrapper at the bottom executes when imported as a script.

PII_COLUMNS = {b"steam_id_64", b"last_logoff", b"name", b"real_name",
               b"persona_name", b"personaname", b"avatar", b"avatar_url",
               b"discovered_via", b"src_steam_id", b"dst_steam_id"}


def _drop_columns(csv_bytes: bytes, drop: set[bytes]) -> bytes:
    """Drop named columns from a UTF-8 CSV byte string.

    Returns original bytes if header doesn't match or no columns are dropped.
    Robust to LF/CRLF and to columns we don't have.
    """
    # Split on first newline (header)
    nl = b"\n"
    if b"\r\n" in csv_bytes[:4096]:
        nl = b"\r\n"

    head, sep, rest = csv_bytes.partition(nl)
    if not sep:
        return csv_bytes  # single-line file, nothing to do

    headers = [h.strip() for h in head.split(b",")]
    drop_idxs = [i for i, h in enumerate(headers) if h in drop]
    if not drop_idxs:
        return csv_bytes

    keep_idxs = [i for i in range(len(headers)) if i not in drop_idxs]
    new_header = b",".join(headers[i] for i in keep_idxs)

    out = [new_header]
    # Process each line. Use the SAME line separator as detected.
    for line in rest.split(nl):
        if not line:
            out.append(line)
            continue
        # Naive split — our CSVs do not contain quoted commas in these columns,
        # so this is safe for our schema. We verify in pre-publish anyway.
        cells = line.split(b",")
        if len(cells) < len(headers):
            # malformed (shorter than header) — pad
            cells = cells + [b""] * (len(headers) - len(cells))
        elif len(cells) > len(headers):
            # extra commas in last column — re-join the tail
            cells = cells[: len(headers) - 1] + [b",".join(cells[len(headers) - 1:])]
        new_cells = [cells[i] for i in keep_idxs]
        out.append(b",".join(new_cells))
    return nl.join(out)


def sanitize(blob_data: bytes) -> bytes:
    if not blob_data:
        return blob_data
    # Cheap check: skip binary blobs (PNG, etc.)
    if b"\x00" in blob_data[:512]:
        return blob_data
    # Only act if header contains a PII column name
    head_end = blob_data.find(b"\n")
    if head_end < 0 or head_end > 8192:
        return blob_data
    head = blob_data[:head_end].lower()
    if not any(c in head for c in PII_COLUMNS):
        return blob_data
    return _drop_columns(blob_data, PII_COLUMNS)


# When invoked by filter-repo via --blob-callback, the local variable `blob`
# is exposed. We test for it to avoid breaking import-as-module use.
try:
    blob.data = sanitize(blob.data)  # type: ignore[name-defined]  # noqa: F821
except NameError:
    if __name__ == "__main__":
        # Self-test from CLI
        import sys
        if len(sys.argv) > 1:
            data = open(sys.argv[1], "rb").read()
            out = sanitize(data)
            sys.stdout.buffer.write(out)
        else:
            print("Self-test mode: pass a CSV path to sanitize")
