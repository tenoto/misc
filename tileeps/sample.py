#!/usr/bin/env python

import os 

cmd  = './tileeps.py 3x3 out.eps '
cmd += 'data/fig1.eps data/fig2.eps data/fig3.eps '
cmd += 'data/fig4.eps data/fig5.eps data/fig6.eps '
cmd += 'data/fig7.eps data/fig8.eps data/fig9.eps '
print cmd
os.system(cmd)