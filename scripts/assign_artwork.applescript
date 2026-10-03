-- Assign artwork to Buried Landscapes tracks in Music
-- Images loaded from /Users/rhysgravell/Ableton/Artwork in alphabetical order

set artworkFolderPath to "/Users/rhysgravell/Ableton/Artwork"

-- Get sorted list of image files
try
	set imageFilesRaw to do shell script "ls -1 " & quoted form of artworkFolderPath & " | grep -iE '\\.(jpg|jpeg|png)$'"
on error
	display dialog "Could not read artwork folder. Check it exists at:" & return & artworkFolderPath buttons {"OK"} default button "OK"
	return
end try

if imageFilesRaw is "" then
	display dialog "No JPG or PNG images found in:" & return & artworkFolderPath buttons {"OK"} default button "OK"
	return
end if

set imageFileNames to paragraphs of imageFilesRaw
set imageCount to count of imageFileNames

tell application "Music"
	-- Get all Buried Landscapes tracks from the library
	set buriedTracks to {}
	try
		tell source 1
			tell library playlist 1
				set buriedTracks to every track whose artist is "Buried Landscapes"
			end tell
		end tell
	on error errMsg
		display dialog "Could not access Music library: " & errMsg buttons {"OK"} default button "OK"
		return
	end try

	set trackCount to count of buriedTracks

	if trackCount is 0 then
		display dialog "No tracks found for artist 'Buried Landscapes'. Check the artist name matches exactly in Music." buttons {"OK"} default button "OK"
		return
	end if

	set imageIndex to 1
	set successCount to 0
	set errorLog to ""

	repeat with i from 1 to trackCount
		set thisTrack to item i of buriedTracks
		set trackName to name of thisTrack
		set imageFileName to item imageIndex of imageFileNames
		set imagePath to artworkFolderPath & "/" & imageFileName

		set fileExt to do shell script "echo " & quoted form of imageFileName & " | sed 's/.*\\.//' | tr '[:upper:]' '[:lower:]'"

		try
			-- Clear existing artwork
			delete every artwork of thisTrack

			-- Read image data
			if fileExt is in {"jpg", "jpeg"} then
				set artData to read POSIX file imagePath as «class JPEG»
			else
				set artData to read POSIX file imagePath as «class PNGf»
			end if

			-- Create artwork entry and set data
			set newArt to make new artwork at end of artworks of thisTrack
			set raw data of newArt to artData

			set successCount to successCount + 1

		on error errMsg
			set errorLog to errorLog & "• " & trackName & ": " & errMsg & return
		end try

		-- Advance image index, cycling back if needed
		set imageIndex to (imageIndex mod imageCount) + 1
	end repeat

	if errorLog is not "" then
		display dialog "Finished with errors (" & successCount & "/" & trackCount & " succeeded):" & return & return & errorLog buttons {"OK"} default button "OK"
	else
		display dialog "Done! Artwork assigned to " & successCount & " of " & trackCount & " tracks." buttons {"OK"} default button "OK"
	end if
end tell
