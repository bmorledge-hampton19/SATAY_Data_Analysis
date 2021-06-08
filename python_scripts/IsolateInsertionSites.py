# This script takes the aligned reads (in bed format) from the SATAY sequencing data 
# and calls the insertion site as being just beyond the 5' end of the read.
from mutperiodpy.Tkinter_scripts.TkinterDialog import TkinterDialog
from mutperiodpy.helper_scripts.UsefulFileSystemFunctions import getDataDirectory
from typing import List
import subprocess

def isolateInsertionSites(alignedReadsFilePaths: List[str]):

    for alignedReadsFilePath in alignedReadsFilePaths:

        print("Working with", alignedReadsFilePath)

        # Generate a path to the output file.
        insertionSitesFilePath = alignedReadsFilePath.rsplit('.',1)[0] + "_insertion_sites.bed"

        filteredReads = 0
        remainingReads = 0

        with open(alignedReadsFilePath, 'r') as alignedReadsFile:
            with open(insertionSitesFilePath, 'w') as insertionSitesFile:

                for line in alignedReadsFile:
                    choppedUpLine = line.split()

                    # Check for the expected ADE2 read to filter out.
                    if choppedUpLine[0] == "chrXV" and choppedUpLine[1] == "565445" and choppedUpLine[2] == "565595" and choppedUpLine[5] == '-':
                        filteredReads += 1
                        continue
                    else: remainingReads += 1

                    # Based on which strand the read is on, alter the position to highlight the 5' insertion site.
                    if choppedUpLine[5] == '+':
                        choppedUpLine[2] = str(int(choppedUpLine[1]) + 1)
                        choppedUpLine[1] = str(int(choppedUpLine[1]) - 1)
                    elif choppedUpLine[5] == '-':
                        choppedUpLine[1] = str(int(choppedUpLine[2]) - 1)
                        choppedUpLine[2] = str(int(choppedUpLine[2]) + 1)
                    else:
                        raise ValueError("Line does not have expected strand designation:\n" + line)
                    
                    # Replace the 4th column (sequencing ID?) to conserve space.
                    choppedUpLine[3] = '.'

                    insertionSitesFile.write('\t'.join(choppedUpLine) + '\n')

        print("Filtered out", filteredReads, "reads at expected ADE2 Location. ", remainingReads, " reads remaining.")
        print("Sorting...")
        subprocess.run(("sort", insertionSitesFilePath, "-k1,1", "-k2,2n", "-k3,3n", "-o", insertionSitesFilePath), check = True)


def main():

    # Create the Tkinter UI
    dialog = TkinterDialog(workingDirectory=getDataDirectory())
    dialog.createMultipleFileSelector("Aligned SATAY Reads:",0,"aligned_SATAY_reads.bed",("Bed Files",".bed"))

    # Run the UI
    dialog.mainloop()

    # If no input was received (i.e. the UI was terminated prematurely), then quit!
    if dialog.selections is None: quit()

    isolateInsertionSites(dialog.selections.getFilePathGroups()[0])


if __name__ == "__main__": main()