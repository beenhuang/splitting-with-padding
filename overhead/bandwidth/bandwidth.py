#!/usr/bin/env python3

"""
<file>    bandwidth.py
<brief>   evaluate bandwidth overhead for defended traces.
"""

def bandwidth_overhead(real_sent, pad_sent, real_recv, pad_recv):
    lines = []

    # real/pad sent/recv
    lines.append(f"real sent:{format(real_sent, ',')} , padding sent:{format(pad_sent, ',')} \n")
    lines.append(f"real recv:{format(real_recv, ',')} , padding recv:{format(pad_recv, ',')} \n\n")

    # original sent/recv
    lines.append(f"original sent packets:{format(real_sent, ',')} , sent/total={float(real_sent)/float(real_sent+real_recv):.0%} \n")
    lines.append(f"original recv packets:{format(real_recv, ',')} , recv/total={float(real_recv)/float(real_sent+real_recv):.0%} \n")
    lines.append(f"original total packets:{format(real_sent+real_recv, ',')} \n\n")
    
    # defended sent/recv
    lines.append(f"defended sent packets:{format(real_sent+pad_sent, ',')} , sent/total={float(real_sent+pad_sent)/float(real_sent+pad_sent+real_recv+pad_recv):.0%} \n")
    lines.append(f"defended recv packets:{format(real_recv+pad_recv, ',')} , recv/total={float(real_recv+pad_recv)/float(real_sent+pad_sent+real_recv+pad_recv):.0%} \n")
    lines.append(f"defended total packets:{format(real_sent+pad_sent+real_recv+pad_recv, ',')} \n\n")

    # bandwidth
    # sent/recv bandwidth overhead
    lines.append(f"sent bandwidth overhead(pad_sent/real_sent)={float(pad_sent)/float(real_sent):.0%} \n")
    lines.append(f"recv bandwidth overhead(pad_recv/real_recv)={float(pad_recv)/float(real_recv):.0%} \n\n")

    # total bandwidth overhead
    lines.append(f"total bandwidth overhead(padding/total)={float(pad_sent+pad_recv)/float(real_sent+real_recv):.0%} \n\n\n") 

    return lines   
