"""

Elite code -- no meaningful use/pure vanity

(c) Copyright 2005 Philip Jenvey
[See end of file]
"""
import random
from Hellanzb.Util import cmHella

__id__ = '$Id: Elite.py 665 2006-02-16 23:27:52Z pjenvey $'

class Codez:
    allCodez = {}
    aolSays = []
    
    def __init__(self, name, codez):
        self.codez = codez
        Codez.allCodez[name] = self.codez

    def asciiArt():
        keys = Codez.allCodez.keys()
        index = keys[random.randint(0, len(keys) - 1)]
        return Codez.allCodez[index]
    asciiArt = staticmethod(asciiArt)

    def aolSay():
        if len(Codez.aolSays):
            return Codez.aolSays[random.randint(0, len(Codez.aolSays) - 1)]
        return None
    aolSay = staticmethod(aolSay)
    
C = Codez

C('cmhella', cmHella())

C('k0w0', """
               MoO0Oo0Oo0
         (__)
         /oo\\\\################
         \\\\/ ################ |
             ################ |
             ################ |
             ################
              | |        | |
              ^ ^        ^ ^
""")

C('k0w1', """
                    Mo000O0oo0OOO
        
         (__) BBBBBB--EEEEEEE-EEEEEEE-FFFFFFF
         /oo\\\\BB---BB-EE------EE------FF-----\\\\ 
         \\\\  /~BBBBB--EEEEEE--EEEEEE--FFFFF-- |
          oo  BB---BB-EE------EE------FF----- |
              BBBBBB--EEEEEEE-EEEEEEE-FF----- ^
               | |                       | |
               ^ ^                       ^ ^
""")
  
C('roflcopter', """
          ROFL:ROFL:LOL:ROFL:ROFL
                    /\ 
          L   /-----------
         LOL===        [] \ 
          L   \            \ 
               \___________ ]
                  I     I
              -----------------/ 
               ROFL COPTER!!!
""")

C('donotfeedtrolls0', """
         +-------------------+             .:\:\:/:/:.            
         |   PLEASE DO NOT   |            :.:\:\:/:/:.:           
         |  FEED THE TROLLS  |           :=.' -   - '.=:          
         |                   |           '=(\ 9   9 /)='          
         |   Thank you,      |              (  (_)  )             
         |       Management  |              /`-vvv-'\             
         +-------------------+             /         \            
                 |  |        @@@          / /|,,,,,|\ \           
                 |  |        @@@         /_//  /^\  \\_\          
   @x@@x@        |  |         |/         WW(  (   )  )WW          
   \||||/        |  |        \|           __\,,\ /,,/__           
    \||/         |  |         |          (______Y______)          
/\/\/\/\/\/\/\/\//\/\\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ 
==================================================================
""")

C('donotfeedtrolls1', """
                       +----------+
                       |  PLEASE  |
                       |  DO NOT  |
                       | FEED THE |
                       |  TROLLS  |
                       +----------+
                           |  |    
                           |  |    
                         .\|.||/.. 
""")

C('bmwplonk', """
        _____________                 _____________
         `-._    ..::|                 `-._    ..::|       .
             `.  ..::|                     `.  ..::|      /|
              |  ..::|                      |  ..::|     /.|
              |  ..::|   _____              |  ..::|    / :|
    .--------.|  ..::|.-'  ..::-.--. .------|  ..::|   / .:|
    | /\    .::. ..:.'       ..::`. '       |  ..::|  / .::| /\\
    |/  \    .::\../           ..::\        |  ..::| / ..::|/  \\
.---'    '---..::bd        _    ..::b.._    |  ..::|/ ..---'    '---.
 `-.      .-' .::PI     .:(_)   ..::m   )   |       ..::`-.      .-'
   /      \  ..:/.q             ..::w  /   .|       .:'   /      \\
  /_.-``-._\..:' ..\           ..::/  /   .:|       ''---/_.-``-._\\
  ' |  ..:.`  |  ..:`.       ..::,'  /   .::|            ..:.     `
    |  ..:|   |  ..::|`-.__..::-':| /  .::' |  ..:::|`.   ..:\\
    |  ..:J  ,'  ..:::.   ,'   ..::/ ..:'  ,'  ..::::. )   .::b
    | ..:/  /____..::::\ /____...:/ .:'   /____..:::::/   ..::P
    |.:,'                        /.:'                /  ..:::'
    |,'                         /.'                 / ..:-'
    '                          '                   /,-'
                                                  '
""")

aolSay = """
ALL OREAND THE GIFCHERRY BUSH DA BOON CHASED DA WHEASELGIFPASTECLITNUGGET SHIT
WH0A WHUT W00D PEEPUHL THEEENK IF DAY GN00 EYE WUZ A JEEEZUS FREEEK?!
EYE WENT TO THE TRAK TO WAATCH THE PONYNUGGETS RHUN AROUND THE GIFPASTE
MY MOM HAS A GARDUN WAREZ SHE GROZE KUMKUWAITS
THERE'S AN ASSNUGGET 4 ALL YA JEWS AND HOMERSEXULES
A DIQ IZ FER DISPENISING JIZZJ00CE IN DA CLITSAQ JIZZPOQIT
NO WAY JAQNAD, EYE GOT ENOUGH OF DEM SHITSTAYN THINGYS FOR GNO MHORE
EYE WHISH I COULD LIFT H?VY TINGS LYKE DOZE GUIZ ON TEEVHEE
 E_MAILWAREZ IS 2 31337 FOR THE CLITSAQLIKES OFF MIZZEE
SIMPSONS WIN95 THEME R0X! THOT I'D LET Y'ALL KNOW
ITZ UHBOWT THAT TYME 4 ME 2 OHPEN UP THA P00PYTANG AND LET THA JIZPEACHBANANAHOLEJ00ZEZ PHLOE.
H0W W00D J00 LYKE IT EEF EYE P00T MAH SAQ IN J00 MOUF?
HAHAHAHAHHAH!!!! YOU ARE FUNNY IRC PEOPLE
WHEN EYE GHO TO THE CLITGIFNUGGETPASTESHOPPINGSENTURS EYE UZE SHNUPPING C?RTZ
SO, WHAT YOUR SAYING IS THE ECCENTRICITY OF THE AFORENAMED SAQ IS BEYOND A REASONABLE DOUBT, THE CORNACOPIA OF THE PLETHORA OF GENTALIA?    DAYOM EYEM SMAERT!
EYE KAN SPEEK IN MANNY DIVVRUNT LUNGAGAGES , MUCHAHASAQ
GO RIGHT AHEAD CLITSAQLIQU0R
H0W MUCH SAQ C00D A SAQNAD SAQ EEF A SAQNAD C00D SAQ NAD?
WOT TYME IS CAPTCLIT ON EMM TEE VEE JAQCUMLAPPER?
DEM FUXIN NIGRUXES BETTR STOP PLAYIN DAT LOUD MUSIK CUZ THE JEWISH KIDZ WIT DA LIDDLE DIKS 'N SAQS CAN'T AFFORD 2 SPEDN MOR CASHES ON DA CLITSAQ ASSNUGGEX CEEDEEZ
WHAT UR J00 TOO FRAID UV DA UREET AOL_MAN?
J00 N0 FUX WIF ME! EYE'LL BUST J00 IN THA GRILL NIG-NUGGET!
IF J00 ORDER TODAY, YOU GET A GINSU KNIFE AND A SMOKELESS ASHTRAY
MUSS BEE YER SPLEAN HURTIN CUZ I JUS BUSS A CAPP IN IT BIZZONITCHEZ
THA S00P D00 J0UR IZ ASSCUNTJUICE WIF BROKKULLI AND BAKKIN NUGGEX
I THOUGHT J00 GNU, CRUNCHYBONERFACEBOY
HEHEHEH WHY DNOT YU GOE PISS ON YER MOMUHZPASTE CLITNUGGSAQ FUXBUDGET
EYE GNEED SOME SUGARS SO EYE CAN RHUN UP AND DEWON THE HALLWAYZ WIF MUH BOOKZBAGZ WIF MUH KUNDUCKTORR
THIS LITTLE NIGGIE WENT W3WP, W3WP, W3WP ALL DA WAY HIZ-OME
J00 MUSS BOW DOWN, BIZZATCH
EYE LYKE TO PUT LUTZ OF M-80Z IN MUH DOGZ BUTTNUGGETZSHIT
FUQ ALL THA JIZZUM, EYE'M GITTIN' A LEG0 WAWPH3WL.
IM CONSIERDRERING RALFING ON MY GIRLFRIENDS BIGG ASS, ANY ADVISE ON HOW 2 GET THA TIMINH RITE?
WHY IT BE DAT GOTTA BE GOING AND DIZZN UP SOME OF DAT SHEET IN YOURMOMA'S LAP LIKE A NIGGA WIT SOME CAKE ALL OVER THEIR PANTSEATIN TITY HAIR OFF THEIR GRANDMOTHER'S DICK?
W00D J00 LYKE TO SEE MUH RED DWARF? ITS BIG TOO
NE1 OFFERING SHITZZZTIT?????
EYE DONT KNOW, MUH MOMUHZ CLITZAQ PARRTYREWMJUICE WUZ ALL FUQEDUP CUZ THE TOSGUIDEZ WERE ALL OVER MY PASTESHIT
DAS RIGHT, ITZ DA SHITZ!!!!
MUH MUDDAH SAD THAT SHE LYKES  CUZ OF ITZ CHATREWMZ AND SHIT BUT I LIKE CHAAATTINNG WITH YOU GUYS ON EYEARSEE AND DOWNLOADING NEKKKED PIXTURES OF HOMOSHEXJ00WALS AND J0UNGG BOYEEEZ
I WNET TO JAHMEKKUH FOR VAYCAYSHUN ONEC AND DAY SED HEY MON AND SO I WUZ LIKE FUQSAQ J0UR ASSCLITSAX RASTANBOOEYZ!!! DEN DEY PUT MUHAYAZZ BACK ON DE PLAYNE HOME...
DAT KICKSAQ ECK BOOME PROOOMISZEDCLIT UZ NIUDEALITIES AGAIN
THERE'Z THIAZS GUY AT #WAREZ-LAME AND HE SZYZ HIS BEST FRIENDZ AT MIDWAY WILL GIVE UZ BUTTALITIES
WHAT THE HELL IZ GOIN ON ROUND THIS ALAME PLACE?
OH YAH THAT WOULD R00L IF EYE DIDNT ARLEADY GNO THEM
BUTTSNATCHFAGAZZNIGGR0XWAREZB0YWH0RE IS IN DA HAY-OH-WAY-OWSE
FUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFU--MY FINGERS R TY-ERD
WHUT IS THA FUKKKINASSLIQSAQFUXXX S00P D00 J00R
H0LD 0NT0 J00R BITCHBUTTPUNXAYAZZ I NEED TO LIQDRINKSIP MY LAYMERSAQPASTE
EYE PLEH DAT NIGGRUX GAME KEY EYE TOO AND MAN DO I SHIZZROQ WIT DAT MAYYUH CHIQSAQ
PHEAL MUH PHLOAX, NIGGER0X!
LIKE HOW CAN YOU TYPE FAG NUGGET CLIT-SAQ WARRIORS OF DOOM-FAGS WITHOUGH LAUGHING YOUR CLIT-SAQ OFF
YER JUST A FAG NUGGET ASS BUDGET HERTZ AQUA VELVA CHEEZ WHIZ NAD SUQ CLITSAQ
J00 BUTT SPANKER CLIT SAQ SUCKER ASS NUGGET SHOOTER WITH CHEEZ BACON AND LETTUCE
WHERES THE ROOM SUPERVISOR? I NEED TO AXE HIM A KWESTYUN
WHUT THA FUCK R J00 SHITTING, NIGGR0X?
MUH SAQ IZ LOSING IT'S WARP CONTAINMENT FIELD... EYEM GONA HAFTA EJECT THA CLIT-SAQ
JEA USERNETSAQ SAID HUMANBALLS SMOKENADS EEZ PLAY
HEY OUDOWM DOO J00 TALX TO THAT CLITSAQ LIQER EDD BEWNM? HE IS THE COOLESST I LOVE THE COMBOOZAQ IN MK#!!!!!!!
EYE JUST HOPE I DONT PFART UNDER THA COVERS LIKE THAT OTHER SLIT-SAQ WITH CHEEZ DID
HEY DONT J00 B TELLING MY KRADDER FRENID SPUDZ JAQMEHAWFF TO SHUT UPP, D00DSAQNUTZ
REAL? W0W CUZ I HERD THAT BUT IF J00 SAW IT TOO IT MUST TRUE BEE
GL00 SUQZ DA NUTTSAQBUTTSMAQ GIVA DOGA BONE!
I GOT GNU SHIT COMING OUT OF MY AYAZZ BITCHNUTZ
ANYTHING NEW?  ANYTHING NEW?   DAMMIT ALL TO HELL, ANYTHING NEW?
AND TOONNIGHT WE HAVE ANN ELITE INTURVIUW WIITH MRSSRS JOHN TURK NUMBAH 1-1,000,000
SUP NIGGRUXSAQJIZZERZ
BUTTCLITNUGGSAQ FAGJIZZREWMNUGGETKICK BUNG-G PUNK
CLOSEHOLE FUNKEEBIDGEGREENAZZSAQPASTE
ONE TYME EYE WENIT 2 THA SKEWL  AND THEY TRIDE TO LERN MUH AYAZZ SUM CRAP BUT EYE KILLT DEM ALL CUZ DEY WUZ UHG-LEE
WEREZ DAT NIGGRUX PHORMIKKAUH
THEREZ NO OPZ IN REWMZ SO PISSOFFSAQJIZZNAG D0RKSAQ
EYE AM GOOD IN BASSABALLZ CAUSE I CAN SHOOT THEM 3 POINTED SHOTS FROM THE FREE THROW LINESHITTT!!!
UHH OKSAQ JAQNAD
SUM KID PISSED ALL OVER IN THE WALMART I USED TO WORK AT AND OF COURSE OUT OF 80 FUXN PPL THEY CALLED ME TO MOP IT UP BUT THAT WUZ KEWL CUZ IT GOT ME CLOSER TO THE CANDY AISLE SO I GOTS ME SUM FREE LUNCH
AOL_MAN IN FULL EFFEKT BOYEEEZ
EYE SHOUDL GET A JOB AT MIHDWEH DOING SUHROWND SOUHNDZ
BAWB CLITSAQ FROM THASHITASSNUGGETREWMJUICE
WHAT'S RAYDEN'S FIRST????
IT'S BEEN EXACTLY 1.5 SECONDS SINCE THE LAST NEW THING...WHERE'S ALL THE NEW STUFF
ECJK BOONE MAILED ME SAY NOOB KEWLIO
HELL YES YOU STUPID ONLIN3HOSTBITCHPUNXNEGROX< OUDOWN IS MY NIGGRUXCLITPASTE, HEEE IS IN N ALL THE CLITREWMSJUICE
MY FR9IEND ECKK BOOME KAN KEEK J00R ASSCLIT
MY MOMMAH MAKES THE VELVETTA NAD CUBES WITH BAKKIN AND CHEEZWHIZ AND MAIRIHNADES ON PARADEZ WITH HER OWN CLITSAQATTAQ JUICES
EYE LYKKE THAT OLD SHOW WITH DOSE GUIZ AND THAT GIRL AHD DEY LIFT IN DIS APORTAMANTOTYPEOSHIT
OREOSMYTH WROTE ALL THA KODES FOR THAT PACMAN GAME CUZ THEY HAD THE POWER OF M00ZIK
FORMICA IZ THA CLIT-SAQ NUGGET SHOOTER OF SEXVILLE BUTT WANKER (WITH CHEEZ WHIZ AND VELVEETA NAD-CUBES)
DAMB ITZ KE0LWIO TO TYEP WIFOUT CHECKYHGN SPEULLTING
EE GEE EEHM SAYZ STREEETDFIGHT ALPHJA BETTETER THAND VEE EFF TOO
NE1 MMING CLITSAQGIFZ? PLZ ADD ME TO J0UR CLITSAQLYST
YYYEAHH CUZ HHHE WANNTED TOO DO XBLOOOSDSTEWRM SOO WE SAID DAMNNNN IT YO R NNOOT COOL ENOUGHH FOR MIDDWAY GO PLATYY KILAH ITSTINXYOOUN SOOSOS STUPIIDID: THARTAT ASSLIQER DANIIYL PISONYAH TTHHAWT CUZUUZ HE WANNTTED TO TOUCH OOOUR CLITSAQS
SKORPYUNN J00 SUQ DA JIZZNIBLTSAQ AND YOU RMOVVA WUZ A FA TTWO BITWHOLEASSNADFUQ
HOW THE FUCKINGJIZZHELLNIGGRUX AM I SUPPOSID TO SWEEP?
DEEZ NUTZ IN YO MUTHAFUXIN MOTUTH, ITS ME WARREN G DA NIGGA WIT DA CLOUT
OV COURSE, II BENT HEER OVAH AND PUMMPED HER CLITSAQPOUCH TILL WEE HAD TO SHEWT HER NUDEALITY WITH ED BEWWN
DOOOOOOD THERE ARE TOO MANY OF MY ASSNUGGEX FLOOOOTIN IN THE ROOMGIFWAREZJUICE
JON TOORK IZ DA BEDSTESDT KOREEOGJRUFFFUR EVUR FRO GAEMZ LYEK EMM KAH TREEH AND HE EVEN I SBETTUR THAN IREORIOSMYTTH
YOU KNOWW ALLL OV JOHNS TURK? WOWOOWOO HIIZ HOUSE SRGS MUST BE A BIIG GIFREWMZPALACENUGGET
MKCORY ROOLZZZ, I AMMM FORMING THHE ALLIANCE OV ERS WWWIT TH  SCAT AAN D MKCORY
NO WAY IS WAS KKKKKONIFRMEZZ BBY MY SAQHOMEZDIQLIQ MKCORY
OUDOWN: YEHA BUT EGMSAQ SEZ DAT SONY R00LLLLZ SO THEY MUUST BVE RIGHT... EEEGM DOESNT LIIE RIGHTH?
EYE KANNOT INDESTAND J00 LANGAGE DAT J00 SPAEK
NO SHE IS NOO T AS ALLEEET AS WE R, SHE DOENSSNMT CALL  LLIKE ALL US NEGRUXES
DAMNIT ALL J00 NEGGIRUX IS CRAMPIN MY BLAQSAQ MOMUHZ TITTIES, SHE IS IN AALLL THE CLIT T REWMSAQSHIZIT WITH ALL THE COG CUNTJIUCENUGGETS WITH BACONCHEEZEWHIZ
J00 MADE OUT WITF TORRY SEPEPPELLLING????
DONT TELL ME THAT CUZ WHEN I WUZ YOUNGRR THEY TRIED TO KILL ME TOO AND IT HURTZ WHEN YOU TALK LIKE THAT
OUDOOOWN, J00 R SOOO ELITTE I BET YOU CAN KIQ THE CHEEZESAQJUICE OUT OFF F TOBYEAZ
DONT FUXN KICK ME J00 ASS NUGGET FUXR OF THA MUTHER DICK SAQ PADDYWHACK GIVE YER DOG A BONER HEH
D00D DONT KIX DA MAN HE GOT CLITSAQNUGGETZ DAT J00 CAN'T EVEN BRING YOUR GIFPASTE NEAR
D00D , LIQSAX MY PHARTKNUKKLENUGGETS WHILE AFTER YOU PASTE THE GIFCLITZ!
HEH 'CAPTNCLIT' (PLAY SUPERHERO THEME HERE) 'LOOK, OVER THERE, ABLE TOLEAP OVER TALL WEENIES IN A SINGLE BOUND, ITS ***CAPTAIN CLIT***!!!
DEEZNUTZ OP MY  SORRY ASS NUGGET CHEEZ WHIZ FUCK BUTT ASS PONY!
MY DAD SAYS THAT HE LIKES TO USE  FOR ITS STOCK QUOTES AND SHIT BUT I LIKE TO CHAT WITH YOU PEOPLLDES AND STUFF ITS FUN AND YOU ALL DONT SUCK SO MUCH
DOOD KAPZ LOKK ROOLZ
J00 MUST B0W D0\\/\\/|\\| 2 ~|~|-|3 ALLMIGHTY A()|_-|\\/|A|\\|
SPUDZ: AT LEEST I DONT HAF 'PUD' IN MY NAME, JAQSAQ-WIT-CHEEZ-IN-BAQ!!!
MOE LESTER? IS THAT J00?
GO TO THE REWMSAQ FOR JAQ
DOOD< ITS OWDOWM THAT GUYY Y FROM THA INTERNUT< HEES ONE OF THOZE GUYYS BUT HE KNOOOW S HOW COOLIO ERS ARR
NO J00 STUPID FUXORSAQLIQER ITS HEYWOOD J00BLOWME
I KAN TAKK GOODLIKE CAUSE IM SMAERT
I GO TOO USERNETT AND BE COOL AND SHIT
ECK BOONNE MAILED ME SAY RAIN HERE1!!!!
NO WAYH IM NOT ANY KEWLLIOHER THAN J00 AND IM FROM THE INTURNUTT
NOWAY MY BROTHER IS STEVEN TYLURZ MOM AND HE SEZ THAT IT WUZ ALL HIS DOING FOR THAT GAME AND SO I MUST BE RITE AND SO YOU JUST ALL SUCK DICK ASS FAG CLIT SAQ!
J00 DON'T EVEN LIVE NEER HIM D00D... PLUS HES FRENDZ WITH MY FREND BILL ITONMYCARD
SO LYKE THERZ A PROBLUM WIT YER AHKKOUNT AND SO EYE WORK FOR AY OH ELL AND EYE NEED J00R PASSWRED SO THAT I CAN FIX THE PROBLUM AY ESS AY PEE
(J00 HAVVE VIOLATE D YOUR TERMMS OF ZERVICE (KEEYWERD: TOSSAQ))
J00 BUNCH OF CLITPUNX NIGGRU0XIZZ!!!!1!
J00 THINK YER FUNNY SPUDZ? WELL J00 ARENT CUZ MY FREND NADSAQ JACQSON QILL KICK YOUR ASS ANYDAY
CUNTPASTE? THAT GUY MICK PHILCRACKIN SED THAT WUZ GOOD.... BUT I TRIYED MY MOMUHZCUNTPASTERREWMZ AND THEY SUQZ A PHATT NUTT
Y0 WHADD ^ MUH NIGGR0X FORMIKAPZ HOW LONG HAF J00 BEEN IN THIZ REWMJUICE, NUGGASS?
DOOD J00 CLITSAQ, ITTS S A JAQSAQ_WIT_CEHEEZE AND BACONBITS J00 BLAQSAQ MOMUHZ TITTIEZ GIFREWMJUICE CUNTPASTE LIQER
DOHNT MAYKE ME HAFTUH PLUS BEE YER AYAZZ!!!!!!!!!
DAMN 12 YR OLDZ THINK THEYRE KRADDER THAN MR MAN
EYE EM UH MASTER BAITER
IM SOO SMAERT THAT DEEZNUTZ HAVE NO IDEEA WHAT MY CLITSAQPASTE WAREZJUICE HAS TO DO WITH THE FAGAPPLE JAGMELLON BUT HOW THE MOMUHAZZNUGG HAS A BIG WAREZGIFREWM
OOPS I MEAN HEY DEWDNUGGET SAQLIQQUR FAGAZZNUGG PORKNADZ!
J00 ALL WANNA BEE L33T LIKE MAN, CUZ EYEM DA NUMMA ONE NUTSAQLIQ0R
HAHAHAHAH CAPS LOCK IS SO EREET, I BET R0B0C0D USES IT ALL THE TIME IN THOSE WAREZ CHANNELZ... HE SAYS LIKE 'GIVE ME WAREZ OR I WILL COLLIDE YOUR AZZ' AND THEY JUST DO
DUZ ANYNOE HAEV ANY BALD 10 YEER OLD CLITSAQ GIFSROOMPASTEZ? I AM LIKE A GIRLNUGGET KOLLEKTER
WELL FUX'N LAMUH OF DA SECOND SUN RISING ON THE CHEEZ NAD NUGGASS CLITSAQ OF LOVE TUNNEL PENISTOUCHR FAG BUTT PINK WEARER!!!!!!!!
SHITT D00D ASS NUGGET FAG PONY CHUNKS
OOPZ HEH IM SO SMAERT
I WISH I COULD BE THAT LEET, I AM A TOTAL LAMER THO BITCH ASS CLITWEARIN PUNXMUVFUX PENISTOUCHN DORKLICK DUDE
RACKBOY DONT FALL OUT OF YOU NADAZZ CHAIR THERE HOMEYNAD FUGHORSENUGGET BUTTAPPLE
JACQUES STRAPPONHEAD PASTENUGG BUTTAPPLE FAGMELON
HORSEBOY JACKKNAD CLITSAQAZZ
HEH IF J00UR GRAFX FILEZ SPIT WHITE CRAP ON MYAZZ ILL HAFTA BUSS A NUTT ALL OVER YOUR PAGEZ
HEH VICUR LYKEZ HORSENADZ AND STUFF LIKE MY FRENID JACK OFFENBEDT
PHUKKEN JERKNAD SHITSUXR FUGNUGGETPASTE SERVISS PROHVYDEUR SUX SHITBALLZ OF WAREZPASTE
J-REK AZZNECK FAGNEGGROX?
D00D, KEEP DAT GIFROOMPASTE TO YOUR OWN SAQNUGGETZ
SPEAK OF THA DEVILHORSE NADAYAZZ
HEH I UZED TO TAKE THA BUSS TO SKEWL
HELL YES, ITS ALL ABOUT WHEN YOU GO INTO THOSE ROOMS WITH ALL FORTYFIVE EATIN BITCH PUSSY CLIT CHUNX WAREZ GIFZ OF CUNT CHICK ASS LICKERS DUDE
THERE GOES MY ASSCHUCK SIDE PAINS AGAIN
HEHE IM CRING
I HATE THE WAREZ ROOMS ON  THEY ARE ALL SO ANGRYEE AT ME CUZ I LEECH OR WHATEEVR FROM THE CLITSAQ STASH BUT THEY DONT UDNERSNAD WHAT THEY ARE DOING CUZ IM A MEMBER OF A BIG WAREZ ELEET GROUP AND CAN GET -1DAY WAREZ ALL THE TIME
BITCH MY PUNK ASSCHEESELICK CARPAL TUNNELS ARE HURTIN LIKE A PINK BUTT HOT DOG ASS JUICE DRINK BITCHPUNX
BEEEATCH, ARE J000 ST3PPIN TO MY CLIT SAQ LEECH ASS HOTDAMN WAREZ TALKIN CUNTPUNX?
HAHHA OK HERE WE GO, NOW WE HE STARTING TO SENSE NO MAKE OUT OF OUR CLITSAX
FUX NO, CLIT BAG BIG SAQ SWINGER PUNX-ASS JAQ-OFF!
EAT MY SAQPUNX WAREZ CAT CUNT LICKER, I AM MORE ELITE THAN YOUR BITCHPUNX CLITGIF ROOM DRINK
DONT EVEN TELL ME ABOUT YOUR MOMUHZ CLIT HOT DOG JUICE SAQ CUZ I ALREADY HEARD ABOUT IT FROM JAQ THA BLAQ SAQ'S BIG MAQ WITH CHEEZ AND BACON!
DAMNNIT NEGROX, MY SAQ ATTAQIN CLITPUNX IS ABOUT TO TAKE ALL YOUR DOG CUNT WAREZ GIFS FOR MY BIG ASS MOMUHZ CUM PARTY ROOM CLITMONGER SHIT
I GOT SHIT COMING OUT OF MY NOSE IM LAUGHING SO HARD
OW MY HEAD HURTZ BAD ASS CLIT SAQ NIGGRUX
THESE ASSNUGGETPONYS ARE JUST TOO DAMN CLITFUXIN FUNNY
MAN THIS SUXKS I KANT STOP LAFFING
DAMN MY CLIT NUGGET WAREZBITCH IS CUMMIN WITH THAT ROOMJUICE, IM ABOUT TO BITCHFUCK THE DOGPISS NIGGEROX THAT FUNX MY GIFMOMSCLIT SHITFUX
EYE THINK FORMICAPS HAS SPENT A LITTLE TOO MUCH CLITFUXINTIME IN A  ROOMJUICE
J00 FUXN WAREZMONGER MOMSCLITSUX'R ASS PONY BIZZNATCH NEGROXZ
BITCH I HAVENT CLITFUXED IN THAT ROOMSHITBITCHPUNX ON NUGGET SINCE I HAD TO GIFSTRADESHITFUCK MONEY FOR SOME CLITSHITASSLICKIN JUICE
GO DAMN IM BEGINNING TO CLITFUX UNDERNDASDTD YOU
YOU KNOW WHATS NUGGET FUXED UP IS THAT I UNDERSTOOD THOSE ASSNUGGETS THE FIRST TIME YOU TYPED THEM
I CAN MAKE A GOOD OMELETTE OUT OF MY ASS NUGGETS AND I ADD CHEEZ AND BAKIN TO MY MOMS CLIT-SAQ JUICES THEN I MIX IT UP IN MY STRAWBERRY SHORTCAKE PLAY OVEN AND IT COMES OUT ALL TASTY AND GOOEY GOOD LIKE REAL OMELLETZ ARE
BITCHPUNX, IF J00 ASSLICKED MY NUGGEX FROM THAT NIGGEROX CLITJUICER, J00 N33D TO TRADEGIFSPONYXS MY MOMUHZ KEYWORD BITCHSLAPHOEATER
SUX BUTZ NUTZ IN THA CLITSAQ JAQ AND THA BIG BLAQ MAQ DADDEEE
I THINK IM GONNA VOMIT
J00'V3 G0+ M4IL!!!!!!!!!!!
J00VE GOT BITCHPUNX!!!
MUST BE SOME CLITGIFJUICEBITCHPUNX PONYASSLCIKWAREZ SHIT
D00D SAVE THIS BITCHAZZ NIGGRUX CHANNEL WINDOWZ CLIT SAQ! DCC IT TO ME L8R ON SHIT NUGGASS
K TO THIS STUFF LIKE A BITCHPUNX TO ASSNUGGETS
I WILL COPY IT TO THE NUGGETBOARD
HAHAHAHHAHAHAHAHA OBVIOUSLY HE MEANT CLITJUICEPASTE FOR THOSE NIGGEROX IN THE WAREZ GIF MOMUHZFUX ASS DOG KILLAH REWMZ
HEHEHE POST I ON THE WAREZNEGGRUX FOR MY CLITASSROOMGIFS DOG HOT SUX ASSFUCKSHIT UP HEY?
GODDAMNIT I JUST SPIT COKE ALL OVER MY ASSPUNX NUGGETSBLANKETSHIT
LAUGHING LIKE A BITCHASSNIGGEROX IN A CLITFUXROOMWAREZJUICE
NIGGEROX THATS SO FUCKEDUPPONYASS
HOLY ASSPUNX AND NIGGRUX BATMANSHIT FUXN LAMUHS BITCHASSNIGRUSAXINDAROOM WITH GIFS AND SHITTOO?
DAMN RIGHT ITS LIKE WHEN YOUR PONYASSNUGGETJUICE GETS INTO YER MOUHZ BLAQSAQATTAQ AND FUXORS GIFJUICE YOUR CLITSAQ
HEHEHHE EYEM SEW MUVFUXN EREET
OK, IM GONNA PEE MY PANTS,
DIE J00 ST00PID ASSFUX PONY NUGGET AUTOGREETS CLITJUICE ASS DOG LICKER
I THINK IT MUST BE ASSPONYCUNTFUX DAY OR SOMETHING...
HEHHE CLITJUICESAQLIQ SHAOKAPS IZ GONNA BITCHAZZ PIZZ IN HIZZASS PANTS OF HELLSHITFIRE WITH THE NIGGRUXROOMJUICEWARES
J00 NUTSAQ FAGASS PONYDICKJUICE FUQOR COCKFIGHTIN TAQ NAQ (SHEEET!)
||THAT SHITASSPONYNIGGEROXJUICE PASTEWAREZ||
ITS ALL ABOUT THE  WAREZ TRADEGIFCUNTPASTE PONYNUGGET CLITSAQ
KCUF FFO, DAWKCID!
HEHE YAH J00 FAQSAQ BUTTSMAQ NIGGRUH OF THA BLAQJAQ WAREZJUICE REWMZ OF DOOM!
HEH JAG ME OFF HEHEHE I'M FUNNY AS HELL
EYE WHISH MY MHOMMA WHOULD CHANGE MY LITTEL SISTR IN PHR0NT OF MH3 STILLLL
HEY J00 CUNTSAQ CLITSAQLIQ0R SAQPRODCOWPROD NIGGR0X OF A PONYASS
EYE M KRADDEST TO THE NEHGATIVE 4TEETH POWAHZ DOODZSPOOGE
DATS ALOT OF SAQNUGGETSPOOGEPASTE
DON'T MAKE ME BREAK OUT THE SAQ MUCHING BUTTCHOADERS
I USED TO WURK AT J00L IN MELOSR PAERK WIF DA NUTZBALL SPOOGE LOADERS... IT SUQD AYAZZPONYNUGGETZ
WHUT IN THE CLITSAQS R U DOING?
EYE KUNT FUXING HAIR JOO CLITSAQSNATCHSPOOGATHONBASTICH
EYE PLAY WIF PHISHEZZ LYKE SACQUE J00STEAU
HEY THERE BUNGSPELUNKURR WASSUP??/?
J00 SAQSNAKKK0R!!!
LLOK ITZ THIS GUY D00DSAQZ!!!1!
HEH HE SAYD JOYN HEHHEHEH
WOW WHRED J00 CUMM FOMR NUTSAQLIQ0R?
EYEARSEE IS DA SHYTT D00DZNUT!
KEWLI0, EYEV BIN WAITNIG FER J00, WHERE ARE DOZE KIDDIESEXGIFOGRAFZ DATJ00 SAID J00D GIB MEE????
"""
Codez.aolSays.extend(aolSay.strip().split('\n'))
     
"""
Copyright (c) 2005 Philip Jenvey <pjenvey@groovie.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author or contributors may not be used to endorse or
   promote products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

$Id: Elite.py 665 2006-02-16 23:27:52Z pjenvey $
"""
