#!/usr/bin/env python

"""
An example of reading a rinex file and extracting the
pseudrange obs and computing a biased multipath observation.

This is a port of the older C++ example3.cpp.

Usage:

  python example3.py <rinex3obs_filename>

For example:
  python example3.py rinex3obs_data.txt

"""

# We recommend only using
#     'import gpstk',
# but if you need constants fairly often, then importing them specifically at once
# may be easier than referring to them by gpstk.L1_FREQ_GPS.
from gpstk import C_MPS, GAMMA_GPS, L1_FREQ_GPS
import gpstk
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rinex3obs_filename')
    args = parser.parse_args()

    user_input = raw_input('Name your PRN of interest, by number: 1 through 32: ')
    int_prn = int(user_input)

    try:
        print('Reading {}'.format(args.rinex3obs_filename))
        header, data = gpstk.readRinex3Obs(args.rinex3obs_filename)  # read in everything
        print(header)

        # Now we loop through all the epochs and process the data for each one
        for d in data:
            # Let's use the CivilTime class to print an easy to understand time:
            civtime = gpstk.CivilTime(d.time)
            print(civtime,)

            # Make a GPSTk SatID for the user's PRN so we can search for it
            prn = gpstk.RinexSatID(int_prn, gpstk.SatID.systemGPS)

            # Check if the PRN is in view (by searching for it)
            if d.obs.find(prn) == d.obs.end():
                print('PRN {} not in view'.format(int_prn))

            else:
                P1 = d.getObs(prn, "P1", header).data
                P2 = d.getObs(prn, "P2", header).data
                L1 = d.getObs(prn, "L1", header).data
                mu = P1 - L1 * (C_MPS / L1_FREQ_GPS) - 2 * (P1 - P2) / (1 - GAMMA_GPS)
                print('PRN {} biased multipath {}'.format(int_prn, mu))

    # We can catch any custom gpstk exception like this:
    except gpstk.Exception as e:
        print(e)


if __name__ == '__main__':
    main()
