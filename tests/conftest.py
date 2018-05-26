import datetime
from io import StringIO

from pytest import fixture

from gnss_tec import ObsFileV2, ObsFileV3

RNX_V2 = """\
     2.11           OBSERVATION DATA    M (MIXED)           RINEX VERSION / TYPE
teqc  2016Nov7      NOAA/NOS/NGS/CORS   20170707 04:06:33UTCPGM / RUN BY / DATE
ASPA                                                        MARKER NAME
50503S006                                                   MARKER NUMBER
Giovanni Sella      NGS                                     OBSERVER / AGENCY
4733K06635          TRIMBLE NETR5       4.85                REC # / TYPE / VERS
30517456            TRM55971.00     NONE                    ANT # / TYPE
 -6100258.8690  -996506.1670 -1567978.8630                  APPROX POSITION XYZ
        0.0000        0.0000        0.0000                  ANTENNA: DELTA H/E/N
     1     1                                                WAVELENGTH FACT L1/2
    11    L1    L2    L5    C1    P1    C2    P2    C5    S1# / TYPES OF OBSERV
          S2    S5                                          # / TYPES OF OBSERV
    30.0000                                                 INTERVAL
    18                                                      LEAP SECONDS
  2017     7     6     0     0    0.0000000     GPS         TIME OF FIRST OBS
                                                            END OF HEADER
                            4  5
ASPA (COGO code)                                            COMMENT
   0.000      (antenna height)                              COMMENT
 -14.32609534 (latitude)                                    COMMENT
-170.72243361 (longitude)                                   COMMENT
0053.667      (elevation)                                   COMMENT
 17  7  6  0  0  0.0000000  0 18G18R15G31G03R06G16G01R09G25G22R05G29-0.000392832
                                R16G26R04G10G32G14
 129609926.497 6 100994793.77642                  24663965.641
                  24663974.148                          38.600          17.800

 120505665.941 6  93726662.377 6                  22550992.016    22550991.051
                  22550998.707                          41.700          39.400

 113401304.102 8  88364763.776 7                  21579566.188
  21579571.359    21579571.531                          50.300          46.200

 132701874.619 5 103404140.724 5                  25252336.969
  25252347.414                                          33.700          34.400

 119263436.899 6  92760508.769 5                  22349925.250    22349924.051
                  22349927.602                          38.100          35.100

 116184238.344 7  90533145.56945                  22109098.484
                  22109105.234                          45.600          33.200

 129470789.804 6 100886299.783 6                  24637455.992
  24637464.797    24637466.082                          37.100          37.300

 114931261.449 7  89391042.915 7                  21522933.477    21522934.391
                  21522939.465                          45.900          43.900

 131228058.513 6 102255791.926 6                  24971881.508
  24971889.785    24971890.309                          38.400          36.300

 119420387.410 7  93054887.93344                  22724945.750
                  22724949.512                          43.200          29.400

 104095002.622 7  80962839.312 7                  19473125.563    19473125.184
                  19473131.082                          43.900          42.200

 131232157.556 6 102258880.431 5                  24972645.516
  24972654.613    24972654.199                          38.300          34.800

 106080541.169 7  82507163.624 7                  19858497.734    19858498.063
                  19858503.371                          44.000          42.800

 108649979.923 8  84662364.399 8                  20675386.594
  20675395.574    20675395.805                          48.400          51.100

 112909742.180 8  87818759.471 7                  21085104.797    21085103.715
                  21085108.438                          48.100          44.700

 115661530.779 8  90125872.381 7                  22009648.641
  22009657.211    22009657.441                          48.500          47.600

 115505192.609 7  90004072.298 7                  21979890.539
  21979899.461    21979899.281                          47.500          47.600

 113491920.675 7  88435293.67545                  21596788.523
                  21596794.160                          46.100          32.700

 17  7  6  0  1  0.0000000  0 18 18R15G31G03R06G16G01R09G25G22R05G29
                                R16G26R04G10G32G14
 129714491.092 6 101076272.53043                  24683863.789
                  24683872.414                          39.200          18.600

 120613774.752 7  93810746.963 6                  22571222.727    22571222.703
                  22571230.711                          42.500          39.700

 113438416.847 8  88393682.795 7                  21586628.695
  21586633.398    21586633.336                          50.300          46.600

 132599072.037 5 103324034.869 6                  25232775.227
  25232785.262    25232781.449                          34.600          36.400

 119149217.493 6  92671671.486 5                  22328518.555    22328518.293
                  22328522.430                          38.300          35.000

 116099973.097 7  90467484.36845                  22093063.586
                  22093069.574                          45.900          33.100

 129470125.015 6 100885781.713 6                  24637328.750
  24637339.078    24637340.129                          36.200          37.000

 114869248.525 7  89342810.692 7                  21511321.695    21511321.555
                  21511325.922                          46.600          44.500

 131324730.690 6 102331120.877 6                  24990277.883
  24990285.867    24990286.273                          38.900          37.100

 119340545.428 7  92992673.42545                  22709753.359
                  22709755.480                          46.100          31.200

 104062372.020 7  80937459.929 7                  19467020.781    19467021.227
                  19467027.590                          44.100          42.700

 131219712.462 6 102249182.977 6                  24970277.469
  24970285.688    24970286.094                          39.900          36.900

 106112572.378 7  82532076.791 7                  19864493.438    19864493.176
                  19864498.133                          43.700          42.700

 108609118.768 8  84630524.539 8                  20667611.063
  20667619.516    20667619.746                          48.500          51.000

 112981641.858 7  87874681.372 7                  21098530.055    21098530.383
                  21098535.574                          47.800          45.400

 115746528.568 8  90192104.390 7                  22025823.547
  22025831.473    22025832.172                          49.600          47.100

 115506300.717 8  90004935.735 7                  21980103.695
  21980111.211    21980110.855                          48.800          47.200

 113479270.250 7  88425436.16745                  21594381.758
                  21594386.398                          45.500          32.700

"""
RNX_HEADER_V2 = """\
     2.11           OBSERVATION DATA    M (MIXED)           RINEX VERSION / TYPE
teqc  2016Apr1      BKG Frankfurt       20170707 00:23:29UTCPGM / RUN BY / DATE
ADIS                                                        MARKER NAME
31502M001                                                   MARKER NUMBER
NTRIPS05-769322-52  ADDIS ABABA UNIVERSITY                  OBSERVER / AGENCY
MT300102915         JPS LEGACY          2.6.1 JAN,10,2008   REC # / TYPE / VERS
0220173805          TRM29659.00     NONE                    ANT # / TYPE
  4913652.8072  3945922.6351   995383.2858                  APPROX POSITION XYZ
        0.0010        0.0000        0.0000                  ANTENNA: DELTA H/E/N
     1     1                                                WAVELENGTH FACT L1/2
    21    L1    P1    C1    L2    P2    D1    D2    S1    S2# / TYPES OF OBSERV
          L5    C5    D5    S5    L7    C7    D7    S7    L8# / TYPES OF OBSERV
          C8    D8    S8                                    # / TYPES OF OBSERV
    30.0000                                                 INTERVAL
    17                                                      LEAP SECONDS
     0                                                      RCV CLOCK OFFS APPL
  2017     7     6     0     0    0.0000000     GPS         TIME OF FIRST OBS
Linux 2.4.21-27.ELsmp|Opteron|gcc -static|Linux x86_64|=+   COMMENT
MAKERINEX 2.0.20973 AAU/NTRIPS05        2017-07-06 01:04    COMMENT
                                                            END OF HEADER
"""

RNX_V3 = '''\
     3.02           OBSERVATION DATA    M                   RINEX VERSION / TYPE
Converto v3.4.8     IGN-RGP             20170627 013115 UTC PGM / RUN BY / DATE
AJAC                                                        MARKER NAME
10077M005                                                   MARKER NUMBER
Automatic           Institut Geographique National          OBSERVER / AGENCY
1830139             LEICA GR25          4.02                REC # / TYPE / VERS
4611118324          TRM57971.00     NONE                    ANT # / TYPE
  4696989.7040   723994.2090  4239678.3140                  APPROX POSITION XYZ
        0.0000        0.0000        0.0000                  ANTENNA: DELTA H/E/N
G   12 C1C L1C D1C S1C C2W L2W D2W S2W C5Q L5Q D5Q S5Q      SYS / # / OBS TYPES
R    8 C1C L1C D1C S1C C2P L2P D2P S2P                      SYS / # / OBS TYPES
E   16 C1C L1C D1C S1C C5Q L5Q D5Q S5Q C7Q L7Q D7Q S7Q C8Q  SYS / # / OBS TYPES
       L8Q D8Q S8Q                                          SYS / # / OBS TYPES
C    8 C1I L1I D1I S1I C7I L7I D7I S7I                      SYS / # / OBS TYPES
S    4 C1C L1C D1C S1C                                      SYS / # / OBS TYPES
DBHZ                                                        SIGNAL STRENGTH UNIT
    30.000                                                  INTERVAL
  2017    06    26    00    00    0.0000000     GPS         TIME OF FIRST OBS
  2017    06    26    23    59   30.0000000     GPS         TIME OF LAST OBS
     0                                                      RCV CLOCK OFFS APPL
G L2S -0.25000                                              SYS / PHASE SHIFT
G L2X -0.25000                                              SYS / PHASE SHIFT
R L2P  0.25000                                              SYS / PHASE SHIFT
E L8Q -0.25000                                              SYS / PHASE SHIFT
 24 R01  1 R02 -4 R03  5 R04  6 R05  1 R06 -4 R07  5 R08  6 GLONASS SLOT / FRQ #
    R09 -2 R10 -7 R11  0 R12 -1 R13 -2 R14 -7 R15  0 R16 -1 GLONASS SLOT / FRQ #
    R17  4 R18 -3 R19  3 R20  2 R21  4 R22 -3 R23  3 R24  2 GLONASS SLOT / FRQ #
 C1C  -71.940 C1P  -71.940 C2C  -71.940 C2P  -71.940        GLONASS COD/PHS/BIS
    18    18  1929     7                                    LEAP SECONDS
                                                            END OF HEADER
> 2017 06 26 00 00  0.0000000  0  4
G06  20835332.939   109490435.32508      -587.633          50.500    20835328.717    85317207.80808      -457.896          48.250    20835330.401    81762343.64108      -438.821          52.350
R04  24135247.881   129243249.65706     -2964.509          39.250    24135244.262   100522446.54306     -2305.728          39.000
E02  25206580.771   132461485.07148      1704.855          50.900    25206579.417    98916045.45308      1273.096          50.150    25206576.244   101496450.89908      1306.281          51.950    25206577.942   100206247.02308      1289.659          48.650
C10  38625935.135   201135401.51606       436.003          40.600    38625926.793   155530626.32107       337.087          45.300
>                              4  1
                                                                         COMMENT
> 2017 06 26 00 00 30.0000000  0  5
G02  23269584.628   122282497.09607      2373.850          45.900    23269574.831    95285049.78406      1849.752          40.000
R06  20254437.775   108081579.18807      1594.895          44.050    20254434.977    84063449.71306      1240.474          41.000
E03  26199562.760   137679722.61448     -1953.987          49.350    26199562.201   102812831.22108     -1459.200          48.450    26199559.507   105494888.18008     -1497.248          50.800    26199561.223   104153862.04807     -1478.202          46.700
C05  39875325.769   207641286.35906         2.988          37.750    39875315.615   160561383.77107         2.041          43.350
S20  38144728.445   200451840.25607       -84.098          44.000
'''
RNX_HEADER_V3 = '''\
     3.02           OBSERVATION DATA    M: MIXED            RINEX VERSION / TYPE
G   16 C1C L1C D1C S1C C2S L2S D2S S2S C2W L2W D2W S2W C5Q  SYS / # / OBS TYPES
       L5Q D5Q S5Q                                          SYS / # / OBS TYPES
R   12 C1C L1C D1C S1C C2P L2P D2P S2P C2C L2C D2C S2C      SYS / # / OBS TYPES
E   16 C1C L1C D1C S1C C5Q L5Q D5Q S5Q C7Q L7Q D7Q S7Q C8Q  SYS / # / OBS TYPES
       L8Q D8Q S8Q                                          SYS / # / OBS TYPES
C    8 C1I L1I D1I S1I C7I L7I D7I S7I                      SYS / # / OBS TYPES
J   12 C1C L1C D1C S1C C2S L2S D2S S2S C5Q L5Q D5Q S5Q      SYS / # / OBS TYPES
S    4 C1C L1C D1C S1C                                      SYS / # / OBS TYPES
    30.000                                                  INTERVAL
  2015    12    19    00    00    0.0000000     GPS         TIME OF FIRST OBS
  2015    12    19    23    59   30.0000000     GPS         TIME OF LAST OBS
                                                            END OF HEADER
'''


@fixture
def dumb_obs_v2():
    obs_file = StringIO(RNX_HEADER_V2)
    return ObsFileV2(
        obs_file,
        version=2.11,
    )


@fixture
def glo_freq_nums_v2():
    return {
        4: {datetime.datetime(2017, 7, 6, 0, 15): 6.0},
        5: {datetime.datetime(2017, 7, 6, 0, 15): 1.0},
        6: {datetime.datetime(2017, 7, 6, 0, 15): -4.0},
        9: {datetime.datetime(2017, 7, 6, 0, 15): -2.0},
        15: {datetime.datetime(2017, 7, 6, 0, 15): 0.0},
        16: {datetime.datetime(2017, 7, 6, 0, 15): -1.0},
    }


@fixture
def obs_v2(glo_freq_nums_v2):
    obs_file = StringIO(RNX_V2)
    return ObsFileV2(
        obs_file,
        version=2.11,
        glo_freq_nums=glo_freq_nums_v2,
    )


@fixture
def obs_absent_slot_v2(glo_freq_nums_v2):
    del glo_freq_nums_v2[16]
    obs_file = StringIO(RNX_V2)
    return ObsFileV2(
        obs_file,
        version=2.11,
        glo_freq_nums=glo_freq_nums_v2,
    )


@fixture
def dumb_obs_v3():
    obs_file = StringIO(RNX_HEADER_V3)
    return ObsFileV3(
        obs_file,
        version=3.02,
    )


@fixture
def glo_freq_nums_v3():
    return {
        4: {datetime.datetime(2017, 6, 26, 0): 6},
        6: {datetime.datetime(2017, 6, 26, 0): -4},
    }


@fixture
def obs_v3(glo_freq_nums_v3):
    obs_file = StringIO(RNX_V3)
    return ObsFileV3(
        obs_file,
        version=3.02,
        glo_freq_nums=glo_freq_nums_v3,
    )


@fixture
def obs_absent_slot_v3(glo_freq_nums_v3):
    del glo_freq_nums_v3[4]
    obs_file = StringIO(RNX_V3)
    return ObsFileV3(
        obs_file,
        version=3.02,
        glo_freq_nums=glo_freq_nums_v3,
    )


@fixture(params=['obs_absent_slot_v2', 'obs_absent_slot_v3'])
def obs_absent_slot(request):
    return request.getfixturevalue(request.param)
