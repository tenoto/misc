#!/usr/bin/env python

import os 
import sys 
import datetime 

# ======================
vmargin = 3 # mm
hmargin = 2 # mm
width   = 176 # 210 - 17*2
# ======================

now    = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
tmpdir = 'tmp_%s' % now
cmd    = 'mkdir -p %s' % tmpdir
#print cmd; 
os.system(cmd)
os.chdir(tmpdir)

if len(sys.argv) <= 2:
	sys.stdout.write("Usage %s 2x3 out.eps file.eps file.eps ...\n" % sys.argv[0])
	quit()

num_of_input_epsfiles = len(sys.argv) - 3
matrix   = sys.argv[1]
num_of_x = int(matrix.split('x')[0])
num_of_y = int(matrix.split('x')[1])

outeps = sys.argv[2]

if num_of_x*num_of_y != num_of_input_epsfiles:
	sys.stdout.write("error: mismatch of AxB with input eps files.\n")
	sys.stdout.write("error: %s ==> %d files are requires.\n" % (matrix, num_of_x*num_of_y))
	sys.stdout.write("error: num_of_input_epsfiles: %d\n" % num_of_input_epsfiles)
	quit()

input_epsfiles_list = []
sys.stdout.write("input files: \n")
for i in range(3,num_of_input_epsfiles+3):
	input_epsfiles_list.append(sys.argv[i])	
	sys.stdout.write("  %s\n" % sys.argv[i])	


tex_header = """
\\documentclass[11pt, oneside]{article} 
\\usepackage{geometry}                	
%\\geometry{letterpaper}                 
\\geometry{a4paper, total={210mm,297mm}, left=17mm, right=17mm, top=18mm, bottom=18mm,}
\\usepackage{graphicx}			
\\pagestyle{empty}"""
tex_header += "\\def\\vmargin{%dmm}\n" % vmargin
tex_header += """
\\begin{document}
\\begin{figure}[htbp]
\\begin{tabular}{cc}
\\vspace{\\vmargin}
% =========================
""" 

tex_footer = """
\\end{tabular}
\\end{figure}
\\end{document}  
"""

ratio = 1.0/float(num_of_x)
fig_width = int((width - hmargin * (num_of_x-1))/float(num_of_x))
id_of_x = 0
id_of_y = 0
tex_body = ""
for eps in input_epsfiles_list:
	i = input_epsfiles_list.index(eps)
	tex_body += """
\\begin{minipage}{%.3f\\hsize}
\\begin{center}
\\includegraphics[width=%dmm]{../%s}
\\end{center}
\\end{minipage}
""" % (ratio, fig_width, eps)
	print eps, id_of_x, id_of_y
	if id_of_x +1 == num_of_x:
		id_of_x = 0
		id_of_y += 1
		tex_body += "\\\\"
		tex_body += "\\vspace{\\vmargin}"
	else:
		id_of_x += 1 

print tex_header
print tex_body
print tex_footer

basename = os.path.splitext(outeps)[0]
texfile = '%s.tex' % basename
f = open(texfile, 'w')
f.write(tex_header)
f.write(tex_body)
f.write(tex_footer)
f.close()

cmd  = 'latex %s.tex\n' % basename
cmd += 'dvips %s.dvi\n' % basename
#cmd += 'ps2eps %s.ps\n' % basename
cmd += 'ps2epsi %s.ps\n' % basename
cmd += 'cp %s.epsi ../\n' % basename
cmd += 'cp %s.ps ../\n' % basename
print cmd
os.system(cmd)

os.chdir('../')
cmd    = 'rm -rf %s' % tmpdir
print cmd; 
os.system(cmd)
