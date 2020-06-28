# Brother QL Labdoo Tags Printer

When preparing a project with several dootronics labels are always some work.
Labdoo.org offers the possibility to print several labels in a sheet, but still have to be printed and cut.
The idea of this script is automatize this process with a QL Brother label printer.

The idea is simple:

1. Read configurations parameters of a file (printer and model) - config.json
2. Read the dootronics ids to be printed from a file - tags.txt
3. Iterate through the ids and print the device label, the power adapter label and battery label

Between every label a user iteraction will be waited to give the user time to cut the label.

It is still a mock-up and the script is not very programmable... i.e. 50 mm label I am using is hard coded...
There is still missing some error detection i.e. if a Dootronic ID does not exists...

# Installtion

For the installation just clone the repository and installed the needed libraries with pip (Requirements.txt will follow)

# Usage

Customize the config.json with your printer interface and model

Write the Dootronics IDs in tags.txt - one ID per line and just 5 digits (omiting 000 of the beginning)

# Acknowledgment

Thanks @pklaus (https://gist.github.com/pklaus) for the great library

https://github.com/pklaus/brother_ql 

