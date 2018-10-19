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
	molInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVRFyaWJib25JbnNpZGVDb2xvcnECSwJOfYdVCWJhbGxTY2FsZXEDSwJHP9AAAAAAAAB9h1UJcG9pbnRTaXplcQRLAkc/8AAAAAAAAH2HVQVjb2xvcnEFSwJLAH1xBksBXXEHSwFhc4dVCnJpYmJvblR5cGVxCEsCSwB9h1UKc3RpY2tTY2FsZXEJSwJHP/AAAAAAAAB9h1UMbW1DSUZIZWFkZXJzcQpdcQsoTk5lVQxhcm9tYXRpY01vZGVxDEsCSwF9h1UKdmR3RGVuc2l0eXENSwJHQBQAAAAAAAB9h1UGaGlkZGVucQ5LAol9h1UNYXJvbWF0aWNDb2xvcnEPSwJOfYdVD3JpYmJvblNtb290aGluZ3EQSwJLAH2HVQlhdXRvY2hhaW5xEUsCiH2HVQpwZGJWZXJzaW9ucRJLAksAfYdVCG9wdGlvbmFscRN9VQ9sb3dlckNhc2VDaGFpbnNxFEsCiX2HVQlsaW5lV2lkdGhxFUsCRz/wAAAAAAAAfYdVD3Jlc2lkdWVMYWJlbFBvc3EWSwJLAH2HVQRuYW1lcRdLAlgPAAAAYWxwaGFfZ2FmZi5yc3Q3fXEYWB0AAABhbHBoYV9zbWlybm9mZl9taW5pbWl6ZWQucnN0N11xGUsBYXOHVQ9hcm9tYXRpY0Rpc3BsYXlxGksCiX2HVQ9yaWJib25TdGlmZm5lc3NxG0sCRz/pmZmZmZmafYdVCnBkYkhlYWRlcnNxHF1xHSh9cR59cR9lVQNpZHNxIEsCSwFLAIZ9cSFLAEsAhl1xIksAYXOHVQ5zdXJmYWNlT3BhY2l0eXEjSwJHv/AAAAAAAAB9h1UQYXJvbWF0aWNMaW5lVHlwZXEkSwJLAn2HVRRyaWJib25IaWRlc01haW5jaGFpbnElSwKIfYdVB2Rpc3BsYXlxJksCiH2HdS4='))
	resInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVQZpbnNlcnRxAksMVQEgfYdVC2ZpbGxEaXNwbGF5cQNLDIl9h1UEbmFtZXEESwxYAwAAAE1HT32HVQVjaGFpbnEFSwxYAQAAAEF9h1UOcmliYm9uRHJhd01vZGVxBksMSwJ9h1UCc3NxB0sMiYmGfYdVCG1vbGVjdWxlcQhLDEsAfXEJSwFOXXEKSwZLBoZxC2GGc4dVC3JpYmJvbkNvbG9ycQxLDEsCfXENSwNOXXEOSwZLBoZxD2GGc4dVBWxhYmVscRBLDFgAAAAAfYdVCmxhYmVsQ29sb3JxEUsMSwJ9cRJLA05dcRNLBksGhnEUYYZzh1UIZmlsbE1vZGVxFUsMSwF9h1UFaXNIZXRxFksMiX2HVQtsYWJlbE9mZnNldHEXSwxOfYdVCHBvc2l0aW9ucRhdcRkoSwFLBoZxGksBSwaGcRtlVQ1yaWJib25EaXNwbGF5cRxLDIl9h1UIb3B0aW9uYWxxHX1VBHNzSWRxHksMSv////99h3Uu'))
	atomInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVQdyZXNpZHVlcQJL/EsCfXEDKEsDTl1xBEsVSxWGcQVhhksETl1xBksqSxWGcQdhhksFTl1xCEs/SxWGcQlhhksGTl1xCktUSxWGcQthhksHTl1xDEtpSxWGcQ1hhksITl1xDkt+SxWGcQ9hhksJTl1xEEuTSxWGcRFhhksKTl1xEkuoSxWGcRNhhksLTl1xFEu9SxWGcRVhhksMTl1xFkvSSxWGcRdhhksNTl1xGEvnSxWGcRlhhnWHVQh2ZHdDb2xvcnEaS/xLAn1xG0sDXXEcKEt+S39LgEuBS4JLg0uES4VLhkuHS4hLiUuKS4tLjEuNS45Lj0uQS5FLkkuTS5RLlUuWS5dLmEuZS5pLm0ucS51LnkufS6BLoUuiS6NLpEulS6ZLp0uoS6lLqkurS6xLrUuuS69LsEuxS7JLs0u0S7VLtku3S7hLuUu6S7tLvEu9S75Lv0vAS8FLwkvDS8RLxUvGS8dLyEvJS8pLy0vMS81LzkvPS9BL0UvSS9NL1EvVS9ZL10vYS9lL2kvbS9xL3UveS99L4EvhS+JL40vkS+VL5kvnS+hL6UvqS+tL7EvtS+5L70vwS/FL8kvzS/RL9Uv2S/dL+Ev5S/pL+2Vzh1UEbmFtZXEdS/xYAgAAAE81fXEeKFgDAAAASDYyXXEfKEsSSydLPEtRS2ZLe0uQS6VLukvPS+RL+WVYAgAAAEgyXXEgKEsESxlLLktDS1hLbUuCS5dLrEvBS9ZL62VYAgAAAEgzXXEhKEsISx1LMktHS1xLcUuGS5tLsEvFS9pL72VYAgAAAEgxXXEiKEsBSxZLK0tAS1VLakt/S5RLqUu+S9NL6GVYAgAAAEg0XXEjKEsMSyFLNktLS2BLdUuKS59LtEvJS95L82VYAgAAAEg1XXEkKEsOSyNLOEtNS2JLd0uMS6FLtkvLS+BL9WVYAwAAAEhPNl1xJShLFEspSz5LU0toS31LkkunS7xL0UvmS/tlWAMAAABINjFdcSYoSxFLJks7S1BLZUt6S49LpEu5S85L40v4ZVgCAAAAQzVdcScoSw1LIks3S0xLYUt2S4tLoEu1S8pL30v0ZVgDAAAASE8yXXEoKEsGSxtLMEtFS1pLb0uES5lLrkvDS9hL7WVYAwAAAEhPM11xKShLCksfSzRLSUteS3NLiEudS7JLx0vcS/FlWAIAAABPNl1xKihLE0soSz1LUktnS3xLkUumS7tL0EvlS/plWAIAAABDM11xKyhLB0scSzFLRktbS3BLhUuaS69LxEvZS+5lWAIAAABDMl1xLChLA0sYSy1LQktXS2xLgUuWS6tLwEvVS+plWAIAAABDMV1xLShLAEsVSypLP0tUS2lLfkuTS6hLvUvSS+dlWAIAAABDNl1xLihLEEslSzpLT0tkS3lLjkujS7hLzUviS/dlWAIAAABPM11xLyhLCUseSzNLSEtdS3JLh0ucS7FLxkvbS/BlWAIAAABPMl1xMChLBUsaSy9LREtZS25Lg0uYS61LwkvXS+xlWAIAAABPMV1xMShLAksXSyxLQUtWS2tLgEuVS6pLv0vUS+llWAIAAABDNF1xMihLC0sgSzVLSktfS3RLiUueS7NLyEvdS/JldYdVA3Zkd3EzS/yJfYdVDnN1cmZhY2VEaXNwbGF5cTRL/Il9h1UFY29sb3JxNUv8SwJ9cTZLA11xNyhLfkt/S4BLgUuCS4NLhEuFS4ZLh0uIS4lLikuLS4xLjUuOS49LkEuRS5JLk0uUS5VLlkuXS5hLmUuaS5tLnEudS55Ln0ugS6FLokujS6RLpUumS6dLqEupS6pLq0usS61LrkuvS7BLsUuyS7NLtEu1S7ZLt0u4S7lLuku7S7xLvUu+S79LwEvBS8JLw0vES8VLxkvHS8hLyUvKS8tLzEvNS85Lz0vQS9FL0kvTS9RL1UvWS9dL2EvZS9pL20vcS91L3kvfS+BL4UviS+NL5EvlS+ZL50voS+lL6kvrS+xL7UvuS+9L8EvxS/JL80v0S/VL9kv3S/hL+Uv6S/tlc4dVCWlkYXRtVHlwZXE4S/yJfYdVBmFsdExvY3E5S/xVAH2HVQVsYWJlbHE6S/xYAAAAAH2HVQ5zdXJmYWNlT3BhY2l0eXE7S/xHv/AAAAAAAAB9h1UHZWxlbWVudHE8S/xLAX1xPShLCF1xPihLAksFSwlLD0sTSxdLGkseSyRLKEssSy9LM0s5Sz1LQUtES0hLTktSS1ZLWUtdS2NLZ0trS25Lckt4S3xLgEuDS4dLjUuRS5VLmEucS6JLpkuqS61LsUu3S7tLv0vCS8ZLzEvQS9RL10vbS+FL5UvpS+xL8Ev2S/plSwZdcT8oSwBLA0sHSwtLDUsQSxVLGEscSyBLIkslSypLLUsxSzVLN0s6Sz9LQktGS0pLTEtPS1RLV0tbS19LYUtkS2lLbEtwS3RLdkt5S35LgUuFS4lLi0uOS5NLlkuaS55LoEujS6hLq0uvS7NLtUu4S71LwEvES8hLykvNS9JL1UvZS91L30viS+dL6kvuS/JL9Ev3ZXWHVQpsYWJlbENvbG9ycUBL/EsCfXFBSwNdcUIoS35Lf0uAS4FLgkuDS4RLhUuGS4dLiEuJS4pLi0uMS41LjkuPS5BLkUuSS5NLlEuVS5ZLl0uYS5lLmkubS5xLnUueS59LoEuhS6JLo0ukS6VLpkunS6hLqUuqS6tLrEutS65Lr0uwS7FLskuzS7RLtUu2S7dLuEu5S7pLu0u8S71Lvku/S8BLwUvCS8NLxEvFS8ZLx0vIS8lLykvLS8xLzUvOS89L0EvRS9JL00vUS9VL1kvXS9hL2UvaS9tL3EvdS95L30vgS+FL4kvjS+RL5UvmS+dL6EvpS+pL60vsS+1L7kvvS/BL8UvyS/NL9Ev1S/ZL90v4S/lL+kv7ZXOHVQxzdXJmYWNlQ29sb3JxQ0v8SwJ9cURLA11xRShLfkt/S4BLgUuCS4NLhEuFS4ZLh0uIS4lLikuLS4xLjUuOS49LkEuRS5JLk0uUS5VLlkuXS5hLmUuaS5tLnEudS55Ln0ugS6FLokujS6RLpUumS6dLqEupS6pLq0usS61LrkuvS7BLsUuyS7NLtEu1S7ZLt0u4S7lLuku7S7xLvUu+S79LwEvBS8JLw0vES8VLxkvHS8hLyUvKS8tLzEvNS85Lz0vQS9FL0kvTS9RL1UvWS9dL2EvZS9pL20vcS91L3kvfS+BL4UviS+NL5EvlS+ZL50voS+lL6kvrS+xL7UvuS+9L8EvxS/JL80v0S/VL9kv3S/hL+Uv6S/tlc4dVD3N1cmZhY2VDYXRlZ29yeXFGS/xYBAAAAG1haW59h1UGcmFkaXVzcUdL/Ec/8AAAAAAAAH1xSChHP/szM0AAAABdcUkoSwBLA0sHSwtLDUsQSxVLGEscSyBLIkslSypLLUsxSzVLN0s6Sz9LQktGS0pLTEtPS1RLV0tbS19LYUtkS2lLbEtwS3RLdkt5S35LgUuFS4lLi0uOS5NLlkuaS55LoEujS6hLq0uvS7NLtUu4S71LwEvES8hLykvNS9JL1UvZS91L30viS+dL6kvuS/JL9Ev3ZUc/+AAAAAAAAF1xSihLAksFSwlLD0sTSxdLGkseSyRLKEssSy9LM0s5Sz1LQUtES0hLTktSS1ZLWUtdS2NLZ0trS25Lckt4S3xLgEuDS4dLjUuRS5VLmEucS6JLpkuqS61LsUu3S7tLv0vCS8ZLzEvQS9RL10vbS+FL5UvpS+xL8Ev2S/pldYdVCmNvb3JkSW5kZXhxS11xTChLAEt+hnFNSwBLfoZxTmVVC2xhYmVsT2Zmc2V0cU9L/E59h1USbWluaW11bUxhYmVsUmFkaXVzcVBL/EcAAAAAAAAAAH2HVQhkcmF3TW9kZXFRS/xLAn2HVQhvcHRpb25hbHFSfXFTKFUGY2hhcmdlcVSIiUv8Rz+tYgbqu2oLfXFVKEe/3P+uv66ToV1xVihLAksXSyxLQUtWS2tlRz+xip4g8vqsXXFXKEsOSyNLOEtNS2JLd2VHP8IPTkWvxIFdcVgoSxBLJUs6S09LZEt5ZUe/4sYf3mRlVl1xWShLg0uYS61LwkvXS+xlRz+3mtQkmKX/XXFaKEuBS5ZLq0vAS9VL6mVHP9N9y6VokLddcVsoSwBLFUsqSz9LVEtpZUc/tz31BaQfxV1xXChLf0uUS6lLvkvTS+hlRz/a8nwmrGcLXXFdKEsKSx9LNEtJS15Lc2VHP9s00AdZ+LtdcV4oSwZLG0swS0VLWktvZUe/4vaw2DfE9V1xXyhLh0ucS7FLxkvbS/BlRz+6WeOGtKWqXXFgKEsESxlLLktDS1hLbWVHv9tayzZu5QZdcWEoS41Loku3S8xL4Uv2ZUc/urbCqmAK0l1xYihLi0ugS7VLykvfS/RlRz+0pp1rIjzuXXFjKEuKS59LtEvJS95L82VHP7pZ44trhJddcWQoS4JLl0usS8FL1kvrZUc/sIFOjbynrV1xZShLhkubS7BLxUvaS+9lRz+3mtQuBmPZXXFmKEsDSxhLLUtCS1dLbGVHv+L+yPGmYUFdcWcoSxNLKEs9S1JLZ0t8ZUc/t90oD0rRZ11xaChLB0scSzFLRktbS3BlR7/bWsswik5eXXFpKEsPSyRLOUtOS2NLeGVHP7SmnW/ZG9pdcWooSwxLIUs2S0tLYEt1ZUc/wg9OUEs6Fl1xayhLjkujS7hLzUviS/dlR7/c/67Pl8QAXXFsKEuAS5VLqku/S9RL6WVHP9N9y7ExvgddcW0oS35Lk0uoS71L0kvnZUc/2wMIsi4eIl1xbihLkkunS7xL0UvmS/tlRz/bNNATIyYMXXFvKEuES5lLrkvDS9hL7WVHP7q2wrYpOCFdcXAoSw1LIks3S0xLYUt2ZUe/4vawyXxMUV1xcShLCUseSzNLSEtdS3JlRz+33SgYuI9BXXFyKEuFS5pLr0vES9lL7mVHP8BWNrqGPjJdcXMoSwtLIEs1S0pLX0t0ZUc/2wMIuwUAHl1xdChLFEspSz5LU0toS31lRz+xip4lqdmZXXF1KEuMS6FLtkvLS+BL9WVHv+LGH+RI+/9dcXYoSwVLGksvS0RLWUtuZUc/2vJ8HT6pMV1xdyhLiEudS7JLx0vcS/FlR7/i/sji6uidXXF4KEuRS6ZLu0vQS+VL+mVHP7CBTp48s+pdcXkoSwhLHUsyS0dLXEtxZUc/rWIG73JI911xeihLEUsSSyZLJ0s7SzxLUEtRS2VLZkt6S3tlRz+3PfT+kdFiXXF7KEsBSxZLK0tAS1VLamVHP8BWNq/qyJ5dcXwoS4lLnkuzS8hL3UvyZXWHh1UMc2VyaWFsTnVtYmVycX2IiF1xfihLAUt+hnF/SwFLfoZxgGWHVQdiZmFjdG9ycYGIiUv8RwAAAAAAAAAAfYeHVQlvY2N1cGFuY3lxgoiJS/xHP/AAAAAAAAB9h4d1VQdkaXNwbGF5cYNL/Ih9h3Uu'))
	bondInfo = cPickle.loads(base64.b64decode('gAJ9cQEoVQVjb2xvcnECTQgBTn2HVQVhdG9tc3EDXXEEKF1xBShLHkshZV1xBihLG0sdZV1xByhLG0seZV1xCChLGUsbZV1xCShLGUt5ZV1xCihLFUsXZV1xCyhLFUsZZV1xDChLEUsTZV1xDShLEUsVZV1xDihLEEsuZV1xDyhLDksQZV1xEChLDksRZV1xEShLDksdZV1xEihLM0s2ZV1xEyhLMEsyZV1xFChLMEszZV1xFShLLkswZV1xFihLKkssZV1xFyhLKksuZV1xGChLJksoZV1xGShLJksqZV1xGihLJUtDZV1xGyhLI0slZV1xHChLI0smZV1xHShLI0syZV1xHihLSEtLZV1xHyhLRUtHZV1xIChLRUtIZV1xIShLQ0tFZV1xIihLP0tBZV1xIyhLP0tDZV1xJChLO0s9ZV1xJShLO0s/ZV1xJihLOktYZV1xJyhLOEs6ZV1xKChLOEs7ZV1xKShLOEtHZV1xKihLXUtgZV1xKyhLWktcZV1xLChLWktdZV1xLShLWEtaZV1xLihLVEtWZV1xLyhLVEtYZV1xMChLUEtSZV1xMShLUEtUZV1xMihLT0ttZV1xMyhLTUtPZV1xNChLTUtQZV1xNShLTUtcZV1xNihLckt1ZV1xNyhLb0txZV1xOChLb0tyZV1xOShLbUtvZV1xOihLaUtrZV1xOyhLaUttZV1xPChLZUtnZV1xPShLZUtpZV1xPihLZEuCZV1xPyhLYktkZV1xQChLYktlZV1xQShLYktxZV1xQihLh0uKZV1xQyhLhEuGZV1xRChLhEuHZV1xRShLgkuEZV1xRihLfkuAZV1xRyhLfkuCZV1xSChLekt8ZV1xSShLekt+ZV1xSihLd0t5ZV1xSyhLd0t6ZV1xTChLd0uGZV1xTShLIUsiZV1xTihLHksfZV1xTyhLHksgZV1xUChLG0scZV1xUShLGUsaZV1xUihLF0sYZV1xUyhLFUsWZV1xVChLE0sUZV1xVShLEUsSZV1xVihLDksPZV1xVyhLNks3ZV1xWChLM0s0ZV1xWShLM0s1ZV1xWihLMEsxZV1xWyhLLksvZV1xXChLLEstZV1xXShLKksrZV1xXihLKEspZV1xXyhLJksnZV1xYChLI0skZV1xYShLS0tMZV1xYihLSEtJZV1xYyhLSEtKZV1xZChLRUtGZV1xZShLQ0tEZV1xZihLQUtCZV1xZyhLP0tAZV1xaChLPUs+ZV1xaShLO0s8ZV1xaihLOEs5ZV1xayhLYEthZV1xbChLXUteZV1xbShLXUtfZV1xbihLWktbZV1xbyhLWEtZZV1xcChLVktXZV1xcShLVEtVZV1xcihLUktTZV1xcyhLUEtRZV1xdChLTUtOZV1xdShLdUt2ZV1xdihLcktzZV1xdyhLckt0ZV1xeChLb0twZV1xeShLbUtuZV1xeihLa0tsZV1xeyhLaUtqZV1xfChLZ0toZV1xfShLZUtmZV1xfihLYktjZV1xfyhLikuLZV1xgChLh0uIZV1xgShLh0uJZV1xgihLhEuFZV1xgyhLgkuDZV1xhChLgEuBZV1xhShLfkt/ZV1xhihLfEt9ZV1xhyhLekt7ZV1xiChLd0t4ZV1xiShLjEuOZV1xiihLjEuPZV1xiyhLjEubZV1xjChLjkusZV1xjShLj0uRZV1xjihLj0uTZV1xjyhLk0uVZV1xkChLk0uXZV1xkShLl0uZZV1xkihLl0v3ZV1xkyhLmUubZV1xlChLmUucZV1xlShLnEufZV1xlihLoUujZV1xlyhLoUukZV1xmChLoUuwZV1xmShLo0vBZV1xmihLpEumZV1xmyhLpEuoZV1xnChLqEuqZV1xnShLqEusZV1xnihLrEuuZV1xnyhLrkuwZV1xoChLrkuxZV1xoShLsUu0ZV1xoihLtku4ZV1xoyhLtku5ZV1xpChLtkvFZV1xpShLuEvWZV1xpihLuUu7ZV1xpyhLuUu9ZV1xqChLvUu/ZV1xqShLvUvBZV1xqihLwUvDZV1xqyhLw0vFZV1xrChLw0vGZV1xrShLxkvJZV1xrihLy0vNZV1xryhLy0vOZV1xsChLy0vaZV1xsShLzUvrZV1xsihLzkvQZV1xsyhLzkvSZV1xtChL0kvUZV1xtShL0kvWZV1xtihL1kvYZV1xtyhL2EvaZV1xuChL2EvbZV1xuShL20veZV1xuihL4EviZV1xuyhL4EvjZV1xvChL4EvvZV1xvShL4k0AAWVdcb4oS+NL5WVdcb8oS+NL52VdccAoS+dL6WVdccEoS+dL62VdccIoS+tL7WVdccMoS+1L72VdccQoS+1L8GVdccUoS/BL82VdccYoS/VL92VdcccoS/VL+GVdccgoS/VNBAFlXXHJKEv4S/plXXHKKEv4S/xlXXHLKEv8S/5lXXHMKEv8TQABZV1xzShNAAFNAgFlXXHOKE0CAU0EAWVdcc8oTQIBTQUBZV1x0ChNBQFNCAFlXXHRKEuMS41lXXHSKEuPS5BlXXHTKEuRS5JlXXHUKEuTS5RlXXHVKEuVS5ZlXXHWKEuXS5hlXXHXKEuZS5plXXHYKEucS51lXXHZKEucS55lXXHaKEufS6BlXXHbKEuhS6JlXXHcKEukS6VlXXHdKEumS6dlXXHeKEuoS6llXXHfKEuqS6tlXXHgKEusS61lXXHhKEuuS69lXXHiKEuxS7JlXXHjKEuxS7NlXXHkKEu0S7VlXXHlKEu2S7dlXXHmKEu5S7plXXHnKEu7S7xlXXHoKEu9S75lXXHpKEu/S8BlXXHqKEvBS8JlXXHrKEvDS8RlXXHsKEvGS8dlXXHtKEvGS8hlXXHuKEvJS8plXXHvKEvLS8xlXXHwKEvOS89lXXHxKEvQS9FlXXHyKEvSS9NlXXHzKEvUS9VlXXH0KEvWS9dlXXH1KEvYS9llXXH2KEvbS9xlXXH3KEvbS91lXXH4KEveS99lXXH5KEvgS+FlXXH6KEvjS+RlXXH7KEvlS+ZlXXH8KEvnS+hlXXH9KEvpS+plXXH+KEvrS+xlXXH/KEvtS+5lXXIAAQAAKEvwS/FlXXIBAQAAKEvwS/JlXXICAQAAKEvzS/RlXXIDAQAAKEv1S/ZlXXIEAQAAKEv4S/llXXIFAQAAKEv6S/tlXXIGAQAAKEv8S/1lXXIHAQAAKEv+S/9lXXIIAQAAKE0AAU0BAWVdcgkBAAAoTQIBTQMBZV1yCgEAAChNBQFNBgFlXXILAQAAKE0FAU0HAWVdcgwBAAAoTQgBTQkBZWVVBWxhYmVscg0BAABNCAFYAAAAAH2HVQhoYWxmYm9uZHIOAQAATQgBiH2HVQZyYWRpdXNyDwEAAE0IAUc/yZmZoAAAAH2HVQtsYWJlbE9mZnNldHIQAQAATQgBTn2HVQhkcmF3TW9kZXIRAQAATQgBSwF9h1UIb3B0aW9uYWxyEgEAAH1VB2Rpc3BsYXlyEwEAAE0IAUsCfYd1Lg=='))
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
	colorInfo = (7, (u'smirnoff', (0.121569, 0.466667, 0.705882, 1)), {(u'', (0.106829, 0.702586, 0.652042, 1)): [0], (u'gaff', (1, 0.498039, 0.054902, 1)): [2], (u'', (1, 1, 1, 1)): [5], (u'', (0.872595, 0.686884, 0.111531, 1)): [1], (u'', (0, 0, 1, 1)): [4], (u'', (0.545455, 0, 1, 1)): [6]})
	viewerInfo = {'cameraAttrs': {'center': (-1.4556257433974e-15, -4.3422056074228e-15, 11.595297413516), 'fieldOfView': 29.71298472849, 'nearFar': (19.45220558605, 3.5627489307088), 'ortho': True, 'eyeSeparation': 50.8, 'focal': 1.4395}, 'viewerAttrs': {'silhouetteColor': None, 'clipping': True, 'showSilhouette': True, 'showShadows': False, 'viewSize': 747.59668037663, 'labelsOnTop': True, 'depthCueRange': (0.5, 1), 'silhouetteWidth': 2, 'singleLayerTransparency': True, 'shadowTextureSize': 2048, 'backgroundImage': [None, 1, 2, 1, 0, 0], 'backgroundGradient': [('Chimera default', [(1, 1, 1, 1), (0, 0, 1, 1)], 1), 1, 0, 0], 'depthCue': True, 'highlight': 0, 'scaleFactor': 116.66851090338, 'angleDependentTransparency': True, 'backgroundMethod': 0}, 'viewerHL': 6, 'cameraMode': 'mono', 'detail': 1.5, 'viewerFog': None, 'viewerBG': 5}

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
	residueData = [(2, 'Chimera default', 'rounded', u'unknown'), (3, 'Chimera default', 'rounded', u'unknown'), (4, 'Chimera default', 'rounded', u'unknown'), (5, 'Chimera default', 'rounded', u'unknown'), (6, 'Chimera default', 'rounded', u'unknown'), (7, 'Chimera default', 'rounded', u'unknown'), (8, 'Chimera default', 'rounded', u'unknown'), (9, 'Chimera default', 'rounded', u'unknown'), (10, 'Chimera default', 'rounded', u'unknown'), (11, 'Chimera default', 'rounded', u'unknown'), (12, 'Chimera default', 'rounded', u'unknown'), (13, 'Chimera default', 'rounded', u'unknown')]
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

mdmovieData = {'length': 2, 'startFrame': None, 'endFrame': None, 'molecule': 0, 'name': 'alpha_gaff.rst7'}

try:
	from Movie import restoreSession
	mdmovie = restoreSession(mdmovieData)
except:
	reportRestoreError("Error restoring MD Movie interface")

mdmovieData = {'length': 1, 'startFrame': None, 'endFrame': None, 'molecule': 1, 'name': 'alpha_smirnoff_minimized.rst7'}

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
	xformMap = {0: (((0.16664287571865, -0.98495102912909, -0.045843453074275), 175.93880605514), (-0.20712954455289, -0.19178520767831, 12.94311677131), True), 1: (((0.16700821376824, -0.9848900174521, -0.045824775582005), 175.93451559455), (27.15853775123, -14.516613398096, 42.221352170629), True)}
	fontInfo = {'face': ('Sans Serif', 'Normal', 16)}
	clipPlaneInfo = {}
	silhouettes = {0: True, 1: True, 530: True}

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

