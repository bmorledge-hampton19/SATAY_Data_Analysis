# This script takes the aligned reads (in bed format) from the SATAY sequencing data 
# and calls the insertion site as being just beyond the 5' end of the read.
from mutperiodpy.Tkinter_scripts.TkinterDialog import TkinterDialog
from mutperiodpy.helper_scripts.UsefulFileSystemFunctions import getDataDirectory
from typing import List

def isolateInsertionSites(alignedReadsFilePaths: List[str]):

    for alignedReadsFilePath in alignedReadsFilePaths:

        # Generate a path to the output file.
        insertionSitesFilePath = alignedReadsFilePath.rsplit('.',1)[0] + "_insertion_sites.bed"

        with open(alignedReadsFilePath, 'r') as alignedReadsFile:
            with open(insertionSitesFilePath, 'w') as insertionSitesFile:

                for line in alignedReadsFile:
                    choppedUpLine = line.split()

                    # Based on which strand the read is on, alter the position to highlight the 5' insertion site.
                    if choppedUpLine[5] == '+':
                        choppedUpLine[2] = str(int(choppedUpLine[1]) + 1)
                        choppedUpLine[1] = str(int(choppedUpLine[1]) - 1)
                    elif choppedUpLine[5] == '-':
                        choppedUpLine[1] = str(int(choppedUpLine[2]) - 1)
                        choppedUpLine[2] = str(int(choppedUpLine[2]) + 1)
                    else:
                        raise ValueError("Line does not have expected strand designation:\n" + line)
                    
                    insertionSitesFile.write('\t'.join(choppedUpLine) + '\n')


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