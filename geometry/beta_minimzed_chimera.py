import cPickle, base64
try:
	from SimpleSession.versions.v65 import beginRestore,\
	    registerAfterModelsCB, reportRestoreError, checkVersion
except ImportError:
	from chimera import UserError
	raise UserError('Cannot open session that was saved in a'
	    ' newer version of Chimera; update your version')
checkVersion([1, 12, 41613])
import chimera
from chimera import replyobj
replyobj.status('Restoring session...', \
    blankAfter=0)
replyobj.status('Beginning session restore...', \
    blankAfter=0, secondary=True)
beginRestore()

def restoreCoreModels():
	from SimpleSession.versions.v65 import init, restoreViewer, \
	     restoreMolecules, restoreColors, restoreSurfaces, \
	     restoreVRML, restorePseudoBondGroups, restoreModelAssociations
	molInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVRFyaWJib25JbnNpZGVDb2xvcnECSwJOfYdVCWJhbGxTY2FsZXEDSwJHP9AAAAAAAAB9h1UJcG9pbnRTaXplcQRLAkc/8AAAAAAAAH2HVQVjb2xvcnEFSwJLAH1xBksBXXEHSwFhc4dVCnJpYmJvblR5cGVxCEsCSwB9h1UKc3RpY2tTY2FsZXEJSwJHP/AAAAAAAAB9h1UMbW1DSUZIZWFkZXJzcQpdcQsoTk5lVQxhcm9tYXRpY01vZGVxDEsCSwF9h1UKdmR3RGVuc2l0eXENSwJHQBQAAAAAAAB9h1UGaGlkZGVucQ5LAol9h1UNYXJvbWF0aWNDb2xvcnEPSwJOfYdVD3JpYmJvblNtb290aGluZ3EQSwJLAH2HVQlhdXRvY2hhaW5xEUsCiH2HVQpwZGJWZXJzaW9ucRJLAksAfYdVCG9wdGlvbmFscRN9VQ9sb3dlckNhc2VDaGFpbnNxFEsCiX2HVQlsaW5lV2lkdGhxFUsCRz/wAAAAAAAAfYdVD3Jlc2lkdWVMYWJlbFBvc3EWSwJLAH2HVQRuYW1lcRdLAlgYAAAAYmV0YV9nYWZmX21pbmltaXplZC5yc3Q3fXEYWBwAAABiZXRhX3NtaXJub2ZmX21pbmltaXplZC5yc3Q3XXEZSwFhc4dVD2Fyb21hdGljRGlzcGxheXEaSwKJfYdVD3JpYmJvblN0aWZmbmVzc3EbSwJHP+mZmZmZmZp9h1UKcGRiSGVhZGVyc3EcXXEdKH1xHn1xH2VVA2lkc3EgSwJLAUsAhn1xIUsASwCGXXEiSwBhc4dVDnN1cmZhY2VPcGFjaXR5cSNLAke/8AAAAAAAAH2HVRBhcm9tYXRpY0xpbmVUeXBlcSRLAksCfYdVFHJpYmJvbkhpZGVzTWFpbmNoYWlucSVLAoh9h1UHZGlzcGxheXEmSwKIfYd1Lg=='))
	resInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVQZpbnNlcnRxAksOVQEgfYdVC2ZpbGxEaXNwbGF5cQNLDol9h1UEbmFtZXEESw5YAwAAAE1HT32HVQVjaGFpbnEFSw5YAQAAAEF9h1UOcmliYm9uRHJhd01vZGVxBksOSwJ9h1UCc3NxB0sOiYmGfYdVCG1vbGVjdWxlcQhLDksAfXEJSwFOXXEKSwdLB4ZxC2GGc4dVC3JpYmJvbkNvbG9ycQxLDksCfXENSwNOXXEOSwdLB4ZxD2GGc4dVBWxhYmVscRBLDlgAAAAAfYdVCmxhYmVsQ29sb3JxEUsOSwJ9cRJLA05dcRNLB0sHhnEUYYZzh1UIZmlsbE1vZGVxFUsOSwF9h1UFaXNIZXRxFksOiX2HVQtsYWJlbE9mZnNldHEXSw5OfYdVCHBvc2l0aW9ucRhdcRkoSwFLB4ZxGksBSweGcRtlVQ1yaWJib25EaXNwbGF5cRxLDol9h1UIb3B0aW9uYWxxHX1VBHNzSWRxHksOSv////99h3Uu'))
	atomInfo = cPickle.loads(base64.b64decode('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'))
	bondInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVQVjb2xvcnECTTQBTn2HVQVhdG9tc3EDXXEEKF1xBShLIEsjZV1xBihLHUsfZV1xByhLHUsgZV1xCChLG0sdZV1xCShLG0uQZV1xCihLF0sZZV1xCyhLF0sbZV1xDChLE0sVZV1xDShLE0sXZV1xDihLEkswZV1xDyhLEEsSZV1xEChLEEsTZV1xEShLEEsfZV1xEihLNUs4ZV1xEyhLMks0ZV1xFChLMks1ZV1xFShLMEsyZV1xFihLLEsuZV1xFyhLLEswZV1xGChLKEsqZV1xGShLKEssZV1xGihLJ0tFZV1xGyhLJUsnZV1xHChLJUsoZV1xHShLJUs0ZV1xHihLSktNZV1xHyhLR0tJZV1xIChLR0tKZV1xIShLRUtHZV1xIihLQUtDZV1xIyhLQUtFZV1xJChLPUs/ZV1xJShLPUtBZV1xJihLPEtaZV1xJyhLOks8ZV1xKChLOks9ZV1xKShLOktJZV1xKihLX0tiZV1xKyhLXEteZV1xLChLXEtfZV1xLShLWktcZV1xLihLVktYZV1xLyhLVktaZV1xMChLUktUZV1xMShLUktWZV1xMihLUUtvZV1xMyhLT0tRZV1xNChLT0tSZV1xNShLT0teZV1xNihLdEt3ZV1xNyhLcUtzZV1xOChLcUt0ZV1xOShLb0txZV1xOihLa0ttZV1xOyhLa0tvZV1xPChLZ0tpZV1xPShLZ0trZV1xPihLZkuEZV1xPyhLZEtmZV1xQChLZEtnZV1xQShLZEtzZV1xQihLiUuMZV1xQyhLhkuIZV1xRChLhkuJZV1xRShLhEuGZV1xRihLgEuCZV1xRyhLgEuEZV1xSChLfEt+ZV1xSShLfEuAZV1xSihLe0uZZV1xSyhLeUt7ZV1xTChLeUt8ZV1xTShLeUuIZV1xTihLnkuhZV1xTyhLm0udZV1xUChLm0ueZV1xUShLmUubZV1xUihLlUuXZV1xUyhLlUuZZV1xVChLkUuTZV1xVShLkUuVZV1xVihLjkuQZV1xVyhLjkuRZV1xWChLjkudZV1xWShLI0skZV1xWihLIEshZV1xWyhLIEsiZV1xXChLHUseZV1xXShLG0scZV1xXihLGUsaZV1xXyhLF0sYZV1xYChLFUsWZV1xYShLE0sUZV1xYihLEEsRZV1xYyhLOEs5ZV1xZChLNUs2ZV1xZShLNUs3ZV1xZihLMkszZV1xZyhLMEsxZV1xaChLLksvZV1xaShLLEstZV1xaihLKksrZV1xayhLKEspZV1xbChLJUsmZV1xbShLTUtOZV1xbihLSktLZV1xbyhLSktMZV1xcChLR0tIZV1xcShLRUtGZV1xcihLQ0tEZV1xcyhLQUtCZV1xdChLP0tAZV1xdShLPUs+ZV1xdihLOks7ZV1xdyhLYktjZV1xeChLX0tgZV1xeShLX0thZV1xeihLXEtdZV1xeyhLWktbZV1xfChLWEtZZV1xfShLVktXZV1xfihLVEtVZV1xfyhLUktTZV1xgChLT0tQZV1xgShLd0t4ZV1xgihLdEt1ZV1xgyhLdEt2ZV1xhChLcUtyZV1xhShLb0twZV1xhihLbUtuZV1xhyhLa0tsZV1xiChLaUtqZV1xiShLZ0toZV1xiihLZEtlZV1xiyhLjEuNZV1xjChLiUuKZV1xjShLiUuLZV1xjihLhkuHZV1xjyhLhEuFZV1xkChLgkuDZV1xkShLgEuBZV1xkihLfkt/ZV1xkyhLfEt9ZV1xlChLeUt6ZV1xlShLoUuiZV1xlihLnkufZV1xlyhLnkugZV1xmChLm0ucZV1xmShLmUuaZV1xmihLl0uYZV1xmyhLlUuWZV1xnChLk0uUZV1xnShLkUuSZV1xnihLjkuPZV1xnyhLo0ulZV1xoChLo0umZV1xoShLo0uyZV1xoihLpUvDZV1xoyhLpkuoZV1xpChLpkuqZV1xpShLqkusZV1xpihLqkuuZV1xpyhLrkuwZV1xqChLrk0jAWVdcakoS7BLsmVdcaooS7BLs2VdcasoS7NLtmVdcawoS7hLumVdca0oS7hLu2Vdca4oS7hLx2Vdca8oS7pL2GVdcbAoS7tLvWVdcbEoS7tLv2VdcbIoS79LwWVdcbMoS79Lw2VdcbQoS8NLxWVdcbUoS8VLx2VdcbYoS8VLyGVdcbcoS8hLy2VdcbgoS81Lz2VdcbkoS81L0GVdcbooS81L3GVdcbsoS89L7WVdcbwoS9BL0mVdcb0oS9BL1GVdcb4oS9RL1mVdcb8oS9RL2GVdccAoS9hL2mVdccEoS9pL3GVdccIoS9pL3WVdccMoS91L4GVdccQoS+JL5GVdccUoS+JL5WVdccYoS+JL8WVdcccoS+RNAgFlXXHIKEvlS+dlXXHJKEvlS+llXXHKKEvpS+tlXXHLKEvpS+1lXXHMKEvtS+9lXXHNKEvvS/FlXXHOKEvvS/JlXXHPKEvyS/VlXXHQKEv3S/llXXHRKEv3S/plXXHSKEv3TQYBZV1x0yhL+U0XAWVdcdQoS/pL/GVdcdUoS/pL/mVdcdYoS/5NAAFlXXHXKEv+TQIBZV1x2ChNAgFNBAFlXXHZKE0EAU0GAWVdcdooTQQBTQcBZV1x2yhNBwFNCgFlXXHcKE0MAU0OAWVdcd0oTQwBTQ8BZV1x3ihNDAFNGwFlXXHfKE0OAU0sAWVdceAoTQ8BTREBZV1x4ShNDwFNEwFlXXHiKE0TAU0VAWVdceMoTRMBTRcBZV1x5ChNFwFNGQFlXXHlKE0ZAU0bAWVdceYoTRkBTRwBZV1x5yhNHAFNHwFlXXHoKE0hAU0jAWVdcekoTSEBTSQBZV1x6ihNIQFNMAFlXXHrKE0kAU0mAWVdcewoTSQBTSgBZV1x7ShNKAFNKgFlXXHuKE0oAU0sAWVdce8oTSwBTS4BZV1x8ChNLgFNMAFlXXHxKE0uAU0xAWVdcfIoTTEBTTQBZV1x8yhLo0ukZV1x9ChLpkunZV1x9ShLqEupZV1x9ihLqkurZV1x9yhLrEutZV1x+ChLrkuvZV1x+ShLsEuxZV1x+ihLs0u0ZV1x+yhLs0u1ZV1x/ChLtku3ZV1x/ShLuEu5ZV1x/ihLu0u8ZV1x/yhLvUu+ZV1yAAEAAChLv0vAZV1yAQEAAChLwUvCZV1yAgEAAChLw0vEZV1yAwEAAChLxUvGZV1yBAEAAChLyEvJZV1yBQEAAChLyEvKZV1yBgEAAChLy0vMZV1yBwEAAChLzUvOZV1yCAEAAChL0EvRZV1yCQEAAChL0kvTZV1yCgEAAChL1EvVZV1yCwEAAChL1kvXZV1yDAEAAChL2EvZZV1yDQEAAChL2kvbZV1yDgEAAChL3UveZV1yDwEAAChL3UvfZV1yEAEAAChL4EvhZV1yEQEAAChL4kvjZV1yEgEAAChL5UvmZV1yEwEAAChL50voZV1yFAEAAChL6UvqZV1yFQEAAChL60vsZV1yFgEAAChL7UvuZV1yFwEAAChL70vwZV1yGAEAAChL8kvzZV1yGQEAAChL8kv0ZV1yGgEAAChL9Uv2ZV1yGwEAAChL90v4ZV1yHAEAAChL+kv7ZV1yHQEAAChL/Ev9ZV1yHgEAAChL/kv/ZV1yHwEAAChNAAFNAQFlXXIgAQAAKE0CAU0DAWVdciEBAAAoTQQBTQUBZV1yIgEAAChNBwFNCAFlXXIjAQAAKE0HAU0JAWVdciQBAAAoTQoBTQsBZV1yJQEAAChNDAFNDQFlXXImAQAAKE0PAU0QAWVdcicBAAAoTREBTRIBZV1yKAEAAChNEwFNFAFlXXIpAQAAKE0VAU0WAWVdcioBAAAoTRcBTRgBZV1yKwEAAChNGQFNGgFlXXIsAQAAKE0cAU0dAWVdci0BAAAoTRwBTR4BZV1yLgEAAChNHwFNIAFlXXIvAQAAKE0hAU0iAWVdcjABAAAoTSQBTSUBZV1yMQEAAChNJgFNJwFlXXIyAQAAKE0oAU0pAWVdcjMBAAAoTSoBTSsBZV1yNAEAAChNLAFNLQFlXXI1AQAAKE0uAU0vAWVdcjYBAAAoTTEBTTIBZV1yNwEAAChNMQFNMwFlXXI4AQAAKE00AU01AWVlVQVsYWJlbHI5AQAATTQBWAAAAAB9h1UIaGFsZmJvbmRyOgEAAE00AYh9h1UGcmFkaXVzcjsBAABNNAFHP8mZmaAAAAB9h1ULbGFiZWxPZmZzZXRyPAEAAE00AU59h1UIZHJhd01vZGVyPQEAAE00AUsBfYdVCG9wdGlvbmFscj4BAAB9VQdkaXNwbGF5cj8BAABNNAFLAn2HdS4='))
	crdInfo = cPickle.loads(base64.b64decode('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'))
	surfInfo = {'category': (0, None, {}), 'probeRadius': (0, None, {}), 'pointSize': (0, None, {}), 'name': [], 'density': (0, None, {}), 'colorMode': (0, None, {}), 'useLighting': (0, None, {}), 'transparencyBlendMode': (0, None, {}), 'molecule': [], 'smoothLines': (0, None, {}), 'lineWidth': (0, None, {}), 'allComponents': (0, None, {}), 'twoSidedLighting': (0, None, {}), 'customVisibility': [], 'drawMode': (0, None, {}), 'display': (0, None, {}), 'customColors': []}
	vrmlInfo = {'subid': (0, None, {}), 'display': (0, None, {}), 'id': (0, None, {}), 'vrmlString': [], 'name': (0, None, {})}
	colors = {u'Ru': ((0.141176, 0.560784, 0.560784), 1, u'default'), u'Re': ((0.14902, 0.490196, 0.670588), 1, u'default'), u'Rf': ((0.8, 0, 0.34902), 1, u'default'), u'Ra': ((0, 0.490196, 0), 1, u'default'), u'Rb': ((0.439216, 0.180392, 0.690196), 1, u'default'), u'Rn': ((0.258824, 0.509804, 0.588235), 1, u'default'), u'Rh': ((0.0392157, 0.490196, 0.54902), 1, u'default'), u'Be': ((0.760784, 1, 0), 1, u'default'), u'Ba': ((0, 0.788235, 0), 1, u'default'), u'Bh': ((0.878431, 0, 0.219608), 1, u'default'), u'Bi': ((0.619608, 0.309804, 0.709804), 1, u'default'), u'Bk': ((0.541176, 0.309804, 0.890196), 1, u'default'), u'Br': ((0.65098, 0.160784, 0.160784), 1, u'default'), u'H': ((1, 1, 1), 1, u'default'), u'P': ((1, 0.501961, 0), 1, u'default'), u'Os': ((0.14902, 0.4, 0.588235), 1, u'default'), u'Ge': ((0.4, 0.560784, 0.560784), 1, u'default'), u'Gd': ((0.270588, 1, 0.780392), 1, u'default'), u'Ga': ((0.760784, 0.560784, 0.560784), 1, u'default'), u'Pr': ((0.85098, 1, 0.780392), 1, u'default'), u'Pt': ((0.815686, 0.815686, 0.878431), 1, u'default'), u'Pu': ((0, 0.419608, 1), 1, u'default'),
u'C': ((0.564706, 0.564706, 0.564706), 1, u'default'), u'Pb': ((0.341176, 0.34902, 0.380392), 1, u'default'), u'Pa': ((0, 0.631373, 1), 1, u'default'), u'Pd': ((0, 0.411765, 0.521569), 1, u'default'), u'Cd': ((1, 0.85098, 0.560784), 1, u'default'), u'Po': ((0.670588, 0.360784, 0), 1, u'default'), u'Pm': ((0.639216, 1, 0.780392), 1, u'default'), u'Hs': ((0.901961, 0, 0.180392), 1, u'default'), u'Ho': ((0, 1, 0.611765), 1, u'default'), u'Hf': ((0.301961, 0.760784, 1), 1, u'default'), u'Hg': ((0.721569, 0.721569, 0.815686), 1, u'default'), u'He': ((0.85098, 1, 1), 1, u'default'), u'Md': ((0.701961, 0.0509804, 0.65098), 1, u'default'), u'Mg': ((0.541176, 1, 0), 1, u'default'), u'K': ((0.560784, 0.25098, 0.831373), 1, u'default'), u'Mn': ((0.611765, 0.478431, 0.780392), 1, u'default'), u'O': ((1, 0.0509804, 0.0509804), 1, u'default'), u'Zr': ((0.580392, 0.878431, 0.878431), 1, u'default'), u'S': ((1, 1, 0.188235), 1, u'default'), u'W': ((0.129412, 0.580392, 0.839216), 1, u'default'), u'Zn': ((0.490196, 0.501961, 0.690196), 1, u'default'), u'Mt': ((0.921569, 0, 0.14902), 1, u'default'),
u'gaff': ((1, 0.498039, 0.054902), 1, u'default'), u'Eu': ((0.380392, 1, 0.780392), 1, u'default'), u'Es': ((0.701961, 0.121569, 0.831373), 1, u'default'), u'Er': ((0, 0.901961, 0.458824), 1, u'default'), u'Ni': ((0.313725, 0.815686, 0.313725), 1, u'default'), u'No': ((0.741176, 0.0509804, 0.529412), 1, u'default'), u'Na': ((0.670588, 0.360784, 0.94902), 1, u'default'), u'Nb': ((0.45098, 0.760784, 0.788235), 1, u'default'), u'Nd': ((0.780392, 1, 0.780392), 1, u'default'), u'Ne': ((0.701961, 0.890196, 0.960784), 1, u'default'), u'Np': ((0, 0.501961, 1), 1, u'default'), u'smirnoff': ((0.121569, 0.466667, 0.705882), 1, u'default'), u'Fr': ((0.258824, 0, 0.4), 1, u'default'), u'Fe': ((0.878431, 0.4, 0.2), 1, u'default'), u'Fm': ((0.701961, 0.121569, 0.729412), 1, u'default'), u'B': ((1, 0.709804, 0.709804), 1, u'default'), u'F': ((0.564706, 0.878431, 0.313725), 1, u'default'), u'Sr': ((0, 1, 0), 1, u'default'), u'N': ((0.188235, 0.313725, 0.972549), 1, u'default'), u'Kr': ((0.360784, 0.721569, 0.819608), 1, u'default'), u'Si': ((0.941176, 0.784314, 0.627451), 1, u'default'),
u'Sn': ((0.4, 0.501961, 0.501961), 1, u'default'), u'Sm': ((0.560784, 1, 0.780392), 1, u'default'), u'V': ((0.65098, 0.65098, 0.670588), 1, u'default'), u'Sc': ((0.901961, 0.901961, 0.901961), 1, u'default'), u'Sb': ((0.619608, 0.388235, 0.709804), 1, u'default'), u'Sg': ((0.85098, 0, 0.270588), 1, u'default'), u'Se': ((1, 0.631373, 0), 1, u'default'), u'Co': ((0.941176, 0.564706, 0.627451), 1, u'default'), u'Cm': ((0.470588, 0.360784, 0.890196), 1, u'default'), u'Cl': ((0.121569, 0.941176, 0.121569), 1, u'default'), u'Ca': ((0.239216, 1, 0), 1, u'default'), u'Cf': ((0.631373, 0.211765, 0.831373), 1, u'default'), u'Ce': ((1, 1, 0.780392), 1, u'default'), u'Xe': ((0.258824, 0.619608, 0.690196), 1, u'default'), u'Lu': ((0, 0.670588, 0.141176), 1, u'default'), u'Cs': ((0.341176, 0.0901961, 0.560784), 1, u'default'), u'Cr': ((0.541176, 0.6, 0.780392), 1, u'default'), u'Cu': ((0.784314, 0.501961, 0.2), 1, u'default'), u'La': ((0.439216, 0.831373, 1), 1, u'default'), u'Li': ((0.8, 0.501961, 1), 1, u'default'), u'Tl': ((0.65098, 0.329412, 0.301961), 1, u'default'),
u'Tm': ((0, 0.831373, 0.321569), 1, u'default'), u'Lr': ((0.780392, 0, 0.4), 1, u'default'), u'Th': ((0, 0.729412, 1), 1, u'default'), u'Ti': ((0.74902, 0.760784, 0.780392), 1, u'default'), u'tan': ((0.823529, 0.705882, 0.54902), 1, u'default'), u'Te': ((0.831373, 0.478431, 0), 1, u'default'), u'Tb': ((0.188235, 1, 0.780392), 1, u'default'), u'Tc': ((0.231373, 0.619608, 0.619608), 1, u'default'), u'Ta': ((0.301961, 0.65098, 1), 1, u'default'), u'Yb': ((0, 0.74902, 0.219608), 1, u'default'), u'Db': ((0.819608, 0, 0.309804), 1, u'default'), u'Dy': ((0.121569, 1, 0.780392), 1, u'default'), u'I': ((0.580392, 0, 0.580392), 1, u'default'), u'U': ((0, 0.560784, 1), 1, u'default'), u'Y': ((0.580392, 1, 1), 1, u'default'), u'Ac': ((0.439216, 0.670588, 0.980392), 1, u'default'), u'Ag': ((0.752941, 0.752941, 0.752941), 1, u'default'), u'Ir': ((0.0901961, 0.329412, 0.529412), 1, u'default'), u'Am': ((0.329412, 0.360784, 0.94902), 1, u'default'), u'Al': ((0.74902, 0.65098, 0.65098), 1, u'default'), u'As': ((0.741176, 0.501961, 0.890196), 1, u'default'), u'Ar': ((0.501961, 0.819608, 0.890196), 1, u'default'),
u'Au': ((1, 0.819608, 0.137255), 1, u'default'), u'At': ((0.458824, 0.309804, 0.270588), 1, u'default'), u'In': ((0.65098, 0.458824, 0.45098), 1, u'default'), u'Mo': ((0.329412, 0.709804, 0.709804), 1, u'default')}
	materials = {u'default': ((0, 0, 0), 30)}
	pbInfo = {'category': [u'distance monitor'], 'bondInfo': [{'color': (0, None, {}), 'atoms': [], 'label': (0, None, {}), 'halfbond': (0, None, {}), 'labelColor': (0, None, {}), 'labelOffset': (0, None, {}), 'drawMode': (0, None, {}), 'display': (0, None, {})}], 'lineType': (1, 2, {}), 'color': (1, 4, {}), 'optional': {'fixedLabels': (True, False, (1, 0, {}))}, 'display': (1, True, {}), 'showStubBonds': (1, False, {}), 'lineWidth': (1, 2, {}), 'stickScale': (1, 1, {}), 'id': [-2]}
	modelAssociations = {}
	colorInfo = (7, (u'smirnoff', (0.121569, 0.466667, 0.705882, 1)), {(u'', (0.0279974, 0.740341, 0.113875, 1)): [0], (u'gaff', (1, 0.498039, 0.054902, 1)): [2], (u'', (1, 1, 1, 1)): [5], (u'', (0.917139, 0.291375, 0.761588, 1)): [1], (u'', (0, 0, 1, 1)): [4], (u'', (0.545455, 0, 1, 1)): [6]})
	viewerInfo = {'cameraAttrs': {'center': (19.903639964022, 20.15816532901, 32.711784002826), 'fieldOfView': 29.71298472849, 'nearFar': (41.612841502735, 23.810726502916), 'ortho': True, 'eyeSeparation': 50.8, 'focal': 32.711784002826}, 'viewerAttrs': {'silhouetteColor': None, 'clipping': False, 'showSilhouette': True, 'showShadows': False, 'viewSize': 11.847955217755, 'labelsOnTop': True, 'depthCueRange': (0.5, 1), 'silhouetteWidth': 2, 'singleLayerTransparency': True, 'shadowTextureSize': 2048, 'backgroundImage': [None, 1, 2, 1, 0, 0], 'backgroundGradient': [('Chimera default', [(1, 1, 1, 1), (0, 0, 1, 1)], 1), 1, 0, 0], 'depthCue': True, 'highlight': 0, 'scaleFactor': 1.2211993774666, 'angleDependentTransparency': True, 'backgroundMethod': 0}, 'viewerHL': 6, 'cameraMode': 'mono', 'detail': 1.5, 'viewerFog': None, 'viewerBG': 5}

	replyobj.status("Initializing session restore...", blankAfter=0,
		secondary=True)
	from SimpleSession.versions.v65 import expandSummary
	init(dict(enumerate(expandSummary(colorInfo))))
	replyobj.status("Restoring colors...", blankAfter=0,
		secondary=True)
	restoreColors(colors, materials)
	replyobj.status("Restoring molecules...", blankAfter=0,
		secondary=True)
	restoreMolecules(molInfo, resInfo, atomInfo, bondInfo, crdInfo)
	replyobj.status("Restoring surfaces...", blankAfter=0,
		secondary=True)
	restoreSurfaces(surfInfo)
	replyobj.status("Restoring VRML models...", blankAfter=0,
		secondary=True)
	restoreVRML(vrmlInfo)
	replyobj.status("Restoring pseudobond groups...", blankAfter=0,
		secondary=True)
	restorePseudoBondGroups(pbInfo)
	replyobj.status("Restoring model associations...", blankAfter=0,
		secondary=True)
	restoreModelAssociations(modelAssociations)
	replyobj.status("Restoring camera...", blankAfter=0,
		secondary=True)
	restoreViewer(viewerInfo)

try:
	restoreCoreModels()
except:
	reportRestoreError("Error restoring core models")

	replyobj.status("Restoring extension info...", blankAfter=0,
		secondary=True)


try:
	import StructMeasure
	from StructMeasure.DistMonitor import restoreDistances
	registerAfterModelsCB(restoreDistances, 1)
except:
	reportRestoreError("Error restoring distances in session")


def restoreMidasBase():
	formattedPositions = {}
	import Midas
	Midas.restoreMidasBase(formattedPositions)
try:
	restoreMidasBase()
except:
	reportRestoreError('Error restoring Midas base state')


def restoreMidasText():
	from Midas import midas_text
	midas_text.aliases = {}
	midas_text.userSurfCategories = {}

try:
	restoreMidasText()
except:
	reportRestoreError('Error restoring Midas text state')


def restore_cap_attributes():
 cap_attributes = \
  {
   'cap_attributes': [ ],
   'cap_color': None,
   'cap_offset': 0.01,
   'class': 'Caps_State',
   'default_cap_offset': 0.01,
   'mesh_style': False,
   'shown': True,
   'subdivision_factor': 1.0,
   'version': 1,
  }
 import SurfaceCap.session
 SurfaceCap.session.restore_cap_attributes(cap_attributes)
registerAfterModelsCB(restore_cap_attributes)


def restore_volume_data():
 volume_data_state = \
  {
   'class': 'Volume_Manager_State',
   'data_and_regions_state': [ ],
   'version': 2,
  }
 from VolumeViewer import session
 session.restore_volume_data_state(volume_data_state)

try:
  restore_volume_data()
except:
  reportRestoreError('Error restoring volume data')

geomData = {'AxisManager': {}, 'CentroidManager': {}, 'PlaneManager': {}}

try:
	from StructMeasure.Geometry import geomManager
	geomManager._restoreSession(geomData)
except:
	reportRestoreError("Error restoring geometry objects in session")


def restoreSession_RibbonStyleEditor():
	import SimpleSession
	import RibbonStyleEditor
	userScalings = []
	userXSections = []
	userResidueClasses = []
	residueData = [(2, 'Chimera default', 'rounded', u'unknown'), (3, 'Chimera default', 'rounded', u'unknown'), (4, 'Chimera default', 'rounded', u'unknown'), (5, 'Chimera default', 'rounded', u'unknown'), (6, 'Chimera default', 'rounded', u'unknown'), (7, 'Chimera default', 'rounded', u'unknown'), (8, 'Chimera default', 'rounded', u'unknown'), (9, 'Chimera default', 'rounded', u'unknown'), (10, 'Chimera default', 'rounded', u'unknown'), (11, 'Chimera default', 'rounded', u'unknown'), (12, 'Chimera default', 'rounded', u'unknown'), (13, 'Chimera default', 'rounded', u'unknown'), (14, 'Chimera default', 'rounded', u'unknown'), (15, 'Chimera default', 'rounded', u'unknown')]
	flags = RibbonStyleEditor.NucleicDefault1
	SimpleSession.registerAfterModelsCB(RibbonStyleEditor.restoreState,
				(userScalings, userXSections,
				userResidueClasses, residueData, flags))
try:
	restoreSession_RibbonStyleEditor()
except:
	reportRestoreError("Error restoring RibbonStyleEditor state")

trPickle = 'gAJjQW5pbWF0ZS5UcmFuc2l0aW9ucwpUcmFuc2l0aW9ucwpxASmBcQJ9cQMoVQxjdXN0b21fc2NlbmVxBGNBbmltYXRlLlRyYW5zaXRpb24KVHJhbnNpdGlvbgpxBSmBcQZ9cQcoVQZmcmFtZXNxCEsBVQ1kaXNjcmV0ZUZyYW1lcQlLAVUKcHJvcGVydGllc3EKXXELVQNhbGxxDGFVBG5hbWVxDWgEVQRtb2RlcQ5VBmxpbmVhcnEPdWJVCGtleWZyYW1lcRBoBSmBcRF9cRIoaAhLFGgJSwFoCl1xE2gMYWgNaBBoDmgPdWJVBXNjZW5lcRRoBSmBcRV9cRYoaAhLAWgJSwFoCl1xF2gMYWgNaBRoDmgPdWJ1Yi4='
scPickle = 'gAJjQW5pbWF0ZS5TY2VuZXMKU2NlbmVzCnEBKYFxAn1xA1UHbWFwX2lkc3EEfXNiLg=='
kfPickle = 'gAJjQW5pbWF0ZS5LZXlmcmFtZXMKS2V5ZnJhbWVzCnEBKYFxAn1xA1UHZW50cmllc3EEXXEFc2Iu'
def restoreAnimation():
	'A method to unpickle and restore animation objects'
	# Scenes must be unpickled after restoring transitions, because each
	# scene links to a 'scene' transition. Likewise, keyframes must be 
	# unpickled after restoring scenes, because each keyframe links to a scene.
	# The unpickle process is left to the restore* functions, it's 
	# important that it doesn't happen prior to calling those functions.
	import SimpleSession
	from Animate.Session import restoreTransitions
	from Animate.Session import restoreScenes
	from Animate.Session import restoreKeyframes
	SimpleSession.registerAfterModelsCB(restoreTransitions, trPickle)
	SimpleSession.registerAfterModelsCB(restoreScenes, scPickle)
	SimpleSession.registerAfterModelsCB(restoreKeyframes, kfPickle)
try:
	restoreAnimation()
except:
	reportRestoreError('Error in Animate.Session')

def restoreLightController():
	import Lighting
	Lighting._setFromParams({'ratio': 1.25, 'brightness': 1.16, 'material': [30.0, (0.85, 0.85, 0.85), 0.0], 'back': [(0.3574067443365933, 0.6604015517481455, -0.6604015517481456), (1.0, 1.0, 1.0), 0.0], 'mode': 'two-point', 'key': [(-0.3574067443365933, 0.6604015517481455, 0.6604015517481456), (1.0, 1.0, 1.0), 1.0], 'contrast': 0.83, 'fill': [(0.2505628070857316, 0.2505628070857316, 0.9351131265310294), (1.0, 1.0, 1.0), 0.0]})
try:
	restoreLightController()
except:
	reportRestoreError("Error restoring lighting parameters")

mdmovieData = {'length': 1, 'startFrame': None, 'endFrame': None, 'molecule': 0, 'name': 'beta_gaff_minimized.rst7'}

try:
	from Movie import restoreSession
	mdmovie = restoreSession(mdmovieData)
except:
	reportRestoreError("Error restoring MD Movie interface")

mdmovieData = {'length': 1, 'startFrame': None, 'endFrame': None, 'molecule': 1, 'name': 'beta_smirnoff_minimized.rst7'}

try:
	from Movie import restoreSession
	mdmovie = restoreSession(mdmovieData)
except:
	reportRestoreError("Error restoring MD Movie interface")


def restoreRemainder():
	from SimpleSession.versions.v65 import restoreWindowSize, \
	     restoreOpenStates, restoreSelections, restoreFontInfo, \
	     restoreOpenModelsAttrs, restoreModelClip, restoreSilhouettes

	curSelIds =  []
	savedSels = []
	openModelsAttrs = { 'cofrMethod': 4 }
	windowSize = (1414, 1201)
	xformMap = {0: (((0.73839102906353, 0.11257174740301, 0.66491073828382), 0.037643491021789), (21.150615242816, 20.643226026659, 33.062776639553), True), 1: (((0, 0, 1), 0), (0, 0, 0), True)}
	fontInfo = {'face': ('Sans Serif', 'Normal', 16)}
	clipPlaneInfo = {}
	silhouettes = {0: True, 1: True, 618: True}

	replyobj.status("Restoring window...", blankAfter=0,
		secondary=True)
	restoreWindowSize(windowSize)
	replyobj.status("Restoring open states...", blankAfter=0,
		secondary=True)
	restoreOpenStates(xformMap)
	replyobj.status("Restoring font info...", blankAfter=0,
		secondary=True)
	restoreFontInfo(fontInfo)
	replyobj.status("Restoring selections...", blankAfter=0,
		secondary=True)
	restoreSelections(curSelIds, savedSels)
	replyobj.status("Restoring openModel attributes...", blankAfter=0,
		secondary=True)
	restoreOpenModelsAttrs(openModelsAttrs)
	replyobj.status("Restoring model clipping...", blankAfter=0,
		secondary=True)
	restoreModelClip(clipPlaneInfo)
	replyobj.status("Restoring per-model silhouettes...", blankAfter=0,
		secondary=True)
	restoreSilhouettes(silhouettes)

	replyobj.status("Restoring remaining extension info...", blankAfter=0,
		secondary=True)
try:
	restoreRemainder()
except:
	reportRestoreError("Error restoring post-model state")
from SimpleSession.versions.v65 import makeAfterModelsCBs
makeAfterModelsCBs()

from SimpleSession.versions.v65 import endRestore
replyobj.status('Finishing restore...', blankAfter=0, secondary=True)
endRestore({})
replyobj.status('', secondary=True)
replyobj.status('Restore finished.')

