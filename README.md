# YouTubeLinkGrabber
This repo automatically converts YouTube live streams into a single .m3u8 playlist. The stream URLs are stored in a text file, which a Python script parses and builds the .m3u8 file from when a GitHub action is triggered (triggered by a cron job). A direct link can then be used to get the playlist, which automatically updates.

## Usage
1. Open the `youtubeLink.txt` file.
2. Add to the file with the following information for each stream:
```
Channel Name - M3U Grouping
URL
``` 
The dash seperator on the first line is important, and the URL must come on the next line.

3. After saving changes, either wait for the cron job to run (this repo's job runs at 00:00, 03:00, 06:00, 09:00, 12:00, 15:00 and 18:00), or start the `LinkGrabber` workflow manually (repo > Actions tab > LinkGrabber > Run workflow).

You can also run the program locally by `python YouTubeLinkGrabber.py > YouTubeLive.m3u` or by `chmod +x exec_grabber.sh && ./exec_grabber.sh`.

4. The .m3u8 file will be generated again. You can use the following direct path to the .m3u8 file in your IPTV app:
`https://raw.githubusercontent.com/<your-username-here>/YouTubeLinkGrabber/main/youtube.m3u8`
