# Fanvue content-calendar job — resume handoff

## GOAL
Schedule ~100 media from a Google Drive folder as Fanvue posts, 1/day minimum, cute
engagement captions. Images = FREE posts; videos = pay-to-view $9.99.

## ACCOUNTS / IDS
- Fanvue: single creator @alexisluxxx3, official hosted MCP (mcp.fanvue.com/mcp), tools mcp__Fanvue__*
- Google Drive source folder ID: 1Ybi2lCmI9kHRxqoLy7wIkWX5cNH-S3Pr (82 images + 18 videos = 100)
- Publish time convention: 22:00:00Z daily.

## ENVIRONMENT (critical)
Needs a shell (Bash + curl + jq + base64) AND Fanvue + Google Drive both enabled IN THE CHAT
(check ListConnectors -> enabledInChat:true). A plain claude.ai chat without code execution CANNOT
do the upload (it's a manual curl PUT to a presigned S3 URL).

## REAL STATE (only 9 posts truly created; earlier "32" was a miscount)
FIRST verify live with mcp__Fanvue__get-posts before adding anything. Already scheduled (22:00Z) with
the Drive image file IDs used:
- Jul 27  1myfb5-IP2bOi50UisR5SzO9Ddj2jQ_AD
- Jul 28  1-jgif-SIC86EnlOiYW0MFug3LfdyQiKL
- Aug 6   1521sAUirqA-SxdkXwP_lm5Z-SfE8e8iI
- Aug 7   16zQ-070JhVDqHzTPxRScwkehE_hk3VPa
- Aug 14  1BB1qG2Z5EhDvekBxK07b8TYHpE_ujw7q
- Aug 17  1CljMGyNftR0diy2ZOQcpoB22fOCI_2K4
- Aug 24  1GwSzQmfNwgftoulpEMvq5XK4iJiVFLyf
- Aug 27  1HHBItrYGGi1k-s-RFZc5J4dXfQZJL3rp
- Sep 3   1JrIYX813V7XhmTOVbGhxhqQrRzkxMJ4C
Remaining: 73 images + 18 videos. Fill EVERY open daily slot from Jul 29 on (no gaps).

## BUG TO AVOID
Previous run uploaded bytes but only issued create-image-post for 2 of every 8, then marked all 8
"done" -> 23 orphaned uploads, wrong count. RULE: create-image-post for EVERY file; confirm each
returns a `uuid`; count posts by create responses, never by uploads.

## PROVEN PIPELINE — IMAGES
1. List folder: mcp__Google_Drive__search_files, query:
   parentId = '1Ybi2lCmI9kHRxqoLy7wIkWX5cNH-S3Pr' and (mimeType contains 'image/' or mimeType contains 'video/')
   (large result spills to a tool-results .txt; parse with jq)
2. Per image id: mcp__Google_Drive__download_file_content(fileId). Base64 spills to a file; decode
   off-context:  jq -r '.content' <spillfile> | base64 -d > img.jpg
3. mcp__Fanvue__custom__start-image-upload -> {mediaUuid, uploadId, uploadUrl}
   (uploadUrl host fanvue-raw-media-prod.s3-accelerate.amazonaws.com is reachable via curl)
4. curl -sS -X PUT --data-binary @img.jpg "<uploadUrl>" -D - -o /dev/null \
     | awk 'tolower($1)=="etag:"{gsub(/[\r"]/,"");print $2}'
   (extract muuid = path UUID before '?'; uploadId = value between 'uploadId=' and '&x-amz-checksum'
    from the uploadUrl to avoid transcription errors)
5. mcp__Fanvue__custom__create-image-post:
     image={mediaUuid, uploadId, etag}, audience="followers-and-subscribers",
     text=<caption>, publishAt="<YYYY-MM-DD>T22:00:00Z"
   Confirm response has `uuid` before marking done. Presigned URLs expire in 1h; upload promptly.
Batch ~8 at a time.

## VIDEOS (not yet done; validate on the first)
custom__create-image-post is images only. For mp4s: create-upload-session -> get-upload-part-url
(multipart) -> PUT parts -> complete-upload-session -> create-post with the video media,
price=999 (cents=$9.99, pay-to-view), a teaser + caption. Decode mp4 bytes same as images.

## CAPTION STYLE
Cute, flirty-but-tasteful, always an engagement hook (question/vote/CTA); vary them. Paid videos tease
the unlock ("unlock this one… 🙈🔓").

## WORKING STYLE
Report progress by ACTUAL create responses (uuid). Keep a done-list of Drive file IDs to avoid
double-posting. Fanvue connection flaps — pause/resume, re-check get-posts on resume.
