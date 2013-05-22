#!/usr/bin/env python2.7


""" 
Gets assets table, coordinates parsing, dumping, and distributing of 
data held therein. 

by Andrew Pedelty 11/19/2012

deprecated as of 1/2/2013

"""

import csv
import toolset
import pdb
from collections import defaultdict
from toolset import custom_map, intify

local_netlist_path = "/u/psmith/netlist.data"
local_host_path = "/u/psmith/host.ethers"

def main(): 
    """ 
    Does stuff.
    """
    host_ethers = []
    netlist_data = []
    moin_tables = ""
    moin_tree = toolset.tree()
    table = toolset.pull_assets()
    as_dict = defaultdict(lambda: [])
    # Build the flat files: 
    for el in table: 
        as_dict[tuple(el[2:])].append((custom_map[el[0]], intify(el[1])))
    for key, val in as_dict: 
        pass
    for i in range(0,len(table), 3):
        # Make up for WHD's silly way of storing custom vals: 
        # This is not foolproof, needs some fixing perhaps. 
        jack, hub, hubport = (intify(z['number_value']) for z in (table[i+x] for x in (0,1,2)))  # TODO Fix fix fix this, please
        host = table[i]
        hostname = host['network_name']
        ip = host['network_address']
        macaddr = host['mac_address']
        username = host['user_name']
        location = toolset.loc_map[host['location_id']]
        room = host['room_name']
        # TODO: possibly split this into several functions
        host_ethers.append(defaultdict(toolset.dne, {
            'Hostname': hostname,
            'Ip': ip if ip else '--.--', 
            'MAC Address': macaddr,
            'Additional Info': ', '.join([str(jack), str(hub), str(hubport), str(username)])
            } ))
        netlist_data.append(defaultdict(toolset.dne, {
            'Building': location, 
            'Hostname': hostname,
            'Room No.': room,
            'Jack No.': jack if jack else "lacking",
            'Hub No. ': hub if hub else "lacking",
            'Port No.': hubport if hubport else "lacking", 
            'Comments': '' # Nothing for now- what to do with this? 
            } ))
        # Build tree structure for data: 
        moin_tree[location][room][jack] = (hostname, username)
    # Write it out! 
    with open(local_host_path, 'wb') as fh: 
        writer1 = csv.DictWriter(fh, ["Hostname", "Ip",
                                    "MAC Address", "Additional Info"],
                                    delimiter='\t')
        writer1.writeheader()
        for row in host_ethers: 
            writer1.writerow(row)
    with open(local_netlist_path, 'wb') as fh: 
        writer2 = csv.DictWriter(fh, ["Building", "Hostname", "Room No.", "Jack No.",
                                    "Hub No. ", "Port No.", "Comments"],
                                    delimiter='\t')
        writer2.writeheader()
        for row in netlist_data: 
            writer2.writerow(row)

    # Distribute files. TODO: manage backups in a sensible fashion.
    toolset.transfer(local_host_path, 'lacquer:.')
    toolset.transfer(local_netlist_path, 'lacquer:.')
    # Push data to flat files for Wiki: 
    

if __name__ == "__main__": 
    main()
