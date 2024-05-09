from sympy.ntheory.residue_ntheory import _discrete_log_pohlig_hellman
from sympy.ntheory.generate import nextprime
from Crypto.Util.Padding import unpad
from binascii import unhexlify
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from random import *

n = 32
q = nextprime(int(0x1337**7.331))
class MPDH:
    n = n
    q = q

    def __init__(self, G=None) -> None:
        if G is None:
            J = list(range(n))
            random.shuffle(J)
            self.G = [(j, random.randrange(1, q)) for j in J]
        else:
            self.G = list(G)

    def one(self) -> "list[tuple[int, int]]":
        return [(i, 1) for i in range(self.n)]
    
    def mul(self, P1, P2) -> "list[tuple[int, int]]":
        return [(j2, p1 * p2 % self.q) for j1, p1 in P1 for i, (j2, p2) in enumerate(P2) if i == j1]
    
    def pow(self, e: int) -> "list[tuple[int, int]]":
        if e == 0:
            return self.one()
        if e == 1:
            return self.G
        P = self.pow(e // 2)
        P = self.mul(P, P)
        if e & 1:
            P = self.mul(P, self.G)
        return P
    
#init the parametres from output.txt
G = [(27, 576541852123473587453857143), (30, 308980336947737739763074), (6, 576714242100541088718412974), (11, 1017521109886718025389915352), (20, 615193145962558940278327472), (12, 774509555531937439357120893), (24, 391779828897913324288259341), (25, 1132346405423843029463395751), (17, 594716697452065812978523890), (2, 874290081291134689931777129), (16, 644032523338979410723343744), (18, 244488812784099805004187754), (19, 54815969515927953895853451), (9, 892140525838877200234351579), (0, 1035172473739368720125340516), (10, 234010850171107217602645148), (26, 553068209418440460159908973), (28, 651193673685909515396288108), (31, 267516544679225145124968529), (13, 3722516306860717226547644), (8, 857702104242983655334684378), (23, 500026403121464110459452949), (15, 393364613163450702786356662), (5, 391244609349178989213844009), (21, 910952131475658388469885212), (14, 1063603244922744366730490287), (22, 522514755575633668715407598), (29, 27480420186327768941808142), (4, 827060121449712411364823752), (1, 467138395536172087812149564), (7, 783191131338886861441909143), (3, 238143058061139720334364157)]
A = [(25, 273008280467213406175416805), (27, 943657629504459112645642081), (24, 316701975132704813349071861), (18, 543729617132645012704764994), (8, 110100949907365106433128666), (19, 944145596656650197716035667), (21, 890198584794775150261186974), (1, 873602224504593045527876882), (28, 1000433668998187424712957289), (6, 1127145469901814775978446034), (26, 503191286162303022464799119), (31, 277323961242214423865389684), (13, 375006774381025063844129254), (2, 510529079414309374660426968), (7, 496225947769868752575110700), (16, 295143273981733480773428526), (22, 1003811899180511864866263073), (4, 10228662774908237610924369), (3, 500710475772526994835698180), (9, 7496942222944282461701565), (17, 167633976955451772213119729), (5, 384356832696130802764324171), (10, 710260018957017894423176790), (12, 863141034240913175327236748), (23, 970983963062595395708061768), (30, 514947228922181370947107139), (15, 902589545964430861158170602), (14, 867305148718991889371163870), (20, 537182850069028682788943667), (0, 1010749862898479232893393376), (29, 802381119841919204768407299), (11, 384369937982519086769079851)]
B = [(1, 782600336147009768563544087), (25, 687558078975168130300209032), (6, 807579624938236259117891793), (31, 99133910481549791717858165), (20, 439602176040564575742898780), (12, 255280386109252412847848050), (24, 1152562316990961993959855434), (0, 23246396609063508683030867), (17, 530639708909497737117485182), (2, 77481133193883612536937789), (16, 573714323694342264667232585), (3, 693742194062597314608206945), (19, 927107311973134188028374991), (9, 1061734583944205401955671370), (29, 908983938628414127393375179), (10, 43142131249923285265877928), (26, 740675318357986834571433656), (28, 495963818473656831343876495), (11, 135231787675816896598274583), (13, 758599570504803377453126189), (8, 343941821851395014975992004), (23, 639414397805593304073482261), (15, 737067484099889298558086725), (5, 581543674461436789232292571), (21, 1068066654841130375256561203), (27, 521565551790419200595293009), (22, 415590621854957319360086820), (30, 719515548436047527442650729), (4, 601699130125654413251066471), (7, 263974673437366679284021053), (14, 961194260316625145270271178), (18, 1152731197458539775406558799)]
flag_enc = b"3eb11fb88b1e83460ea9351819e7a9b1739a9af4d0ccde098b9cd414c1ac5273522184727f823e7362e396e16ba04357c7f9512ace28ea8764283a649ac58ba40b797498a5dfbeca63ff54e1c2d0fc31146b17265760161ec9e3783d09431b4e"

#init the generator
mpdhG=MPDH(G=G)

#calculate the residues x mod 40
IA,IB=[],[]
for i in range(1,41):
    residue=mpdhG.pow(i)
    flagA,flagB = 1,1
    for j in range(0,32):
        if residue[j][0]!=A[j][0]:
            flagA=0
        if residue[j][0]!=B[j][0]:
            flagB=0
    if flagA==1:
        IA=residue
        print("Ak",i)
    if flagB==1:
        IB=residue
        print("Bk",i)

#remove the residues so I can apply the dlog
toLogA = (A[0][1]*pow(IA[0][1],-1,q))%q
toLogB = (B[0][1]*pow(IB[0][1],-1,q))%q

#calculate the base
base   = mpdhG.pow(40)[0][1] 

print(base)

#dlog part "10-15 minutes but i have potato vm"
print(_discrete_log_pohlig_hellman(n=q,a=toLogA,b=base))
print(_discrete_log_pohlig_hellman(n=q,a=toLogB,b=base))

a=22332758456281397012971666*40+22
b=19826724756938157275682660*40+11

print(mpdhG.pow(a)==A)
print(mpdhG.pow(b)==B)

#x^ab
Ka = MPDH(G=B).pow(a)

key = SHA256.new(str(Ka).encode()).digest()[:AES.key_size[-1]]

f=unpad(AES.new(key, AES.MODE_ECB).decrypt(unhexlify(flag_enc)), AES.block_size)
print(f)

#b'srdnlen{MPDH_st@nds_f0r_Multiplicative-Permutation_Diffie-Hellman_0bv10usly_2FJ8IVnp4bkhCPv3}'