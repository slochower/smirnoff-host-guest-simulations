systems = """./a-bam-p
./a-bam-s
./a-but-p
./a-but-s
./a-cbu-p
./a-chp-p
./a-cbu-s
./a-chp-s
./a-cpe-p
./a-coc-p
./a-coc-s
./a-cpe-s
./a-hep-p
./a-ham-s
./a-ham-p
./a-hep-s
./a-hp6-p
./a-hex-p
./a-hex-s
./a-hp6-s
./a-hx2-p
./a-hpa-s
./a-hpa-p
./a-hx2-s
./a-mba-p
./a-hx3-s
./a-hx3-p
./a-mba-s
./a-mhp-p
./a-mha-p
./a-mha-s
./a-mhp-s
./a-nmh-p
./a-nmb-p
./a-nmb-s
./a-nmh-s
./a-oct-p
./a-oam-p
./a-oam-s
./a-oct-s
./a-pnt-p
./a-pam-p
./a-pam-s
./a-pnt-s
./b-ben-s
./a-xxxx-s
./b-ben-p
./b-cbu-p
./b-cbu-s
./b-chp-s
./b-chp-p
./b-coc-s
./b-coc-p
./b-cpe-s
./b-cpe-p
./b-ham-s
./b-ham-p
./b-hep-s
./b-hep-p
./b-hex-p
./b-hex-s
./b-m4c-s
./b-m4c-p
./b-m4t-p
./b-m4t-s
./b-mch-s
./b-mha-s
./b-mha-p
./b-mch-p
./b-mo3-s
./b-mo4-p
./b-mo4-s
./b-mo3-p
./b-mp3-s
./b-mp4-s
./b-mp4-p
./b-mp3-p
./b-oam-s
./b-pb3-s
./b-pb3-p
./b-oam-p
./b-pb4-s
./b-pha-s
./b-pb4-p
./b-pha-p
./b-pnt-s
./b-pnt-p"""
systems = systems.split("\n")
systems = [i[2:] for i in systems]
systems = [i for i in systems if "xxxx" not in i]


experimental_deltaG = """a-bam	-1.58	0.02
a-nmb	-1.69	0.02
a-mba	-1.76	0.02
a-pam	-2.72	0.00
a-ham	-3.53	0.00
a-nmh	-3.52	0.01
a-mha	-3.60	0.00
a-hpa	-4.14	0.00
a-mhp	-4.17	0.00
a-oam	-4.61	0.01
b-ham	-2.49	0.08
b-mha	-2.56	0.07
b-oam	-3.59	0.12
a-cbu	-2.02	0.02
a-cpe	-2.13	0.02
a-chp	-2.51	0.06
a-coc	-3.23	1.14
b-cbu	-1.55	0.17
b-cpe	-3.05	0.01
b-mch	-4.18	0.01
b-m4c	-4.32	0.01
b-m4t	-4.54	0.01
b-chp	-4.56	0.01
b-coc	-4.97	0.04
a-but	-1.51	0.04
a-pnt	-2.60	0.01
a-hex	-3.38	0.01
a-hx2	-3.34	0.01
a-hx3	-3.01	0.01
a-hep	-3.99	0.01
a-hp6	-3.60	0.00
a-oct	-4.62	0.02
b-pnt	-1.27	0.32
b-hex	-2.28	0.03
b-hep	-3.39	0.18
b-ben	-1.64	0.02
b-pha	-1.70	0.05
b-mp3	-1.46	0.04
b-mp4	-2.19	0.01
b-mo3	-2.16	0.01
b-mo4	-2.51	0.01
b-pb3	-3.52	0.01
b-pb4	-3.60	0.02"""

chemical_types = {
    'aliphatic_ammoniums': ['a-bam', 'a-nmb', 'a-mba', 'a-pam', 'a-ham', 'a-nmh', 'a-mha', 'a-hpa', 'a-mhp', 'a-oam', 'b-ham', 'b-mha', 'b-oam'],
    'cyclic_alcohols': ['a-cbu', 'a-cpe', 'a-chp', 'a-coc', 'b-cbu', 'b-cpe', 'b-mch', 'b-m4c', 'b-m4t', 'b-chp', 'b-coc'],
    'aliphatic_carboxylates': ['a-but', 'a-pnt', 'a-hex', 'a-hx2', 'a-hx3', 'a-hep', 'a-hp6', 'a-oct', 'b-pnt', 'b-hex', 'b-hep', 'b-ben',
                              'b-pha', 'b-mp3', 'b-mp4', 'b-mo3', 'b-mo4', 'b-pb3', 'b-pb4'],
}
guest_types = {}
for k, v in chemical_types.items():
    for i in v:
        guest_types[i] = k

colors = {'aliphatic_ammoniums': 'darkorange',
          'cyclic_alcohols': 'cornflowerblue',
          'aliphatic_carboxylates': 'purple'
}

