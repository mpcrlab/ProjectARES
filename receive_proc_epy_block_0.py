"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(
    gr.sync_block
):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name="Embedded Python Block",  # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32],
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.is_enabled = False

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if not self.is_enabled:
            if input_items[0][0] != 0:
                self.is_enabled = True
                print("enabled")
                output_items[0][:] = input_items[0]
            else:
                output_items[0][:] = -150

        else:
            output_items[0][:] = input_items[0]
        return len(output_items[0])
