#!/usr/local/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������
# perl5�ѤǤ���

#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ᥤ�󥹥���ץ�(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# �Ƽ�������
# (����ʹߤ���ʬ�γ������ͤ�Ŭ�ڤ��ͤ��ѹ����Ƥ�������)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ���ɬ�����ꤹ����ʬ
#----------------------------------------------------------------------

# ���Υե�������֤��ǥ��쥯�ȥ�
# my($baseDir) = 'http://�����С�/�ǥ��쥯�ȥ�';
#
# ��)
# http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa/hako-main.cgi
# �Ȥ����֤���硢
# my($baseDir) = 'http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa';
# �Ȥ��롣�Ǹ�˥���å���(/)���դ��ʤ���

my($baseDir) = 'http://�����С�/�ǥ��쥯�ȥ�';

# �����ե�������֤��ǥ��쥯�ȥ�
# my($imageDir) = 'http://�����С�/�ǥ��쥯�ȥ�';
my($imageDir) = 'http://�����С�/�ǥ��쥯�ȥ�';

# jcode.pl�ΰ���

# my($jcode) = '/usr/libperl/jcode.pl';  # �٥å�����ξ��
# my($jcode) = './jcode.pl';             # Ʊ���ǥ��쥯�ȥ���֤����
my($jcode) = './jcode.pl';

# �ޥ������ѥ����
# ���Υѥ���ɤϡ����٤Ƥ���Υѥ���ɤ����ѤǤ��ޤ���
# �㤨�С���¾����Υѥ�����ѹ�������Ǥ��ޤ���
my($masterPassword) = 'yourpassword';

# �ü�ѥ����
# ���Υѥ���ɤǡ�̾���ѹ��פ�Ԥ��ȡ�������λ�⡢�����������ͤˤʤ�ޤ���
# (�ºݤ�̾�����Ѥ���ɬ�פϤ���ޤ���)
$HspecialPassword = 'yourspecialpassword';

# ������̾
my($adminName) = '�����Ԥ�̾��';

# �����ԤΥ᡼�륢�ɥ쥹
my($email) = '������@�ɤ���.�ɤ���.�ɤ���';

# �Ǽ��ĥ��ɥ쥹
my($bbs) = 'http://�����С�/�Ǽ���.cgi';

# �ۡ���ڡ����Υ��ɥ쥹
my($toppage) = 'http://�����С�/�ۡ���ڡ���.html';

# �ǥ��쥯�ȥ�Υѡ��ߥå����
# �̾��0755�Ǥ褤����0777��0705��0704���Ǥʤ��ȤǤ��ʤ������С��⤢��餷��
$HdirMode = 0755;

# �ǡ����ǥ��쥯�ȥ��̾��
# ���������ꤷ��̾���Υǥ��쥯�ȥ�ʲ��˥ǡ�������Ǽ����ޤ���
# �ǥե���ȤǤ�'data'�ȤʤäƤ��ޤ������������ƥ��Τ���
# �ʤ�٤��㤦̾�����ѹ����Ƥ���������
$HdirName = 'data';

# �ǡ����ν񤭹�����

# ��å�������
# 1 �ǥ��쥯�ȥ�
# 2 �����ƥॳ����(��ǽ�ʤ�кǤ�˾�ޤ���)
# 3 ����ܥ�å����
# 4 �̾�ե�����(���ޤꤪ����Ǥʤ�)
my($lockMode) = 2;

# (��)
# 4�����򤹤���ˤϡ�'key-free'�Ȥ������ѡ��ߥ����666�ζ��Υե������
# ���Υե������Ʊ���֤��֤��Ʋ�������

#----------------------------------------------------------------------
# ɬ�����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ������ߤˤ�ä����ꤹ����ʬ
#----------------------------------------------------------------------
#----------------------------------------
# ������οʹԤ�ե�����ʤ�
#----------------------------------------
# 1�����󤬲��ä�
$HunitTime = 21600; # 6����

# �۾ｪλ������
# (��å��岿�äǡ�����������뤫)
my($unlockTime) = 120;

# ��κ����
$HmaxIsland = 30;

# �ȥåץڡ�����ɽ��������Υ������
$HtopLogTurn = 1;

# ���ե������ݻ��������
$HlogMax = 8; 

# �Хå����åפ򲿥����󤪤��˼�뤫
$HbackupTurn = 12;

# �Хå����åפ򲿲�ʬ�Ĥ���
$HbackupTimes = 4;

# ȯ�����ݻ��Կ�
$HhistoryMax = 10;

# �������ޥ�ɼ�ư���ϥ������
$HgiveupTurn = 28;

# ���ޥ�����ϸ³���
# (�����ब�ϤޤäƤ����ѹ�����ȡ��ǡ����ե�����θߴ�����̵���ʤ�ޤ���)
$HcommandMax = 20;

# ������Ǽ��ĹԿ�����Ѥ��뤫�ɤ���(0:���Ѥ��ʤ���1:���Ѥ���)
$HuseLbbs = 0;

# ������Ǽ��ĹԿ�
$HlbbsMax = 10;

# ����礭��
# (�ѹ��Ǥ��ʤ�����)
$HislandSize = 12;

# ¾�ͤ�����򸫤��ʤ����뤫
# 0 �����ʤ�
# 1 ������
# 2 100�ΰ̤ǻͼθ���
$HhideMoneyMode = 2;

# �ѥ���ɤΰŹ沽(0���ȰŹ沽���ʤ���1���ȰŹ沽����)
my($cryptOn) = 1;

# �ǥХå��⡼��(1���ȡ��֥������ʤ��ץܥ��󤬻��ѤǤ���)
$Hdebug = 0;

#----------------------------------------
# ��⡢�����ʤɤ������ͤ�ñ��
#----------------------------------------
# ������
$HinitialMoney = 100;

# �������
$HinitialFood = 100;

# �����ñ��
$HunitMoney = '����';

# ������ñ��
$HunitFood = '00�ȥ�';

# �͸���ñ��
$HunitPop = '00��';

# ������ñ��
$HunitArea = '00����';

# �ڤο���ñ��
$HunitTree = '00��';

# �ڤ�ñ�������������
$HtreeValue = 5;

# ̾���ѹ��Υ�����
$HcostChangeName = 500;

# �͸�1ñ�̤�����ο���������
$HeatenFood = 0.2;

#----------------------------------------
# ���Ϥηи���
#----------------------------------------
# �и��ͤκ�����
$HmaxExpPoint = 200; # ������������Ǥ�255�ޤ�

# ��٥�κ�����
my($maxBaseLevel) = 5;  # �ߥ��������
my($maxSBaseLevel) = 3; # �������

# �и��ͤ������Ĥǥ�٥륢�åפ�
my(@baseLevelUp, @sBaseLevelUp);
@baseLevelUp = (20, 60, 120, 200); # �ߥ��������
@sBaseLevelUp = (50, 200);         # �������

#----------------------------------------
# �ɱһ��ߤμ���
#----------------------------------------
# ���ä�Ƨ�ޤ줿����������ʤ�1�����ʤ��ʤ�0
$HdBaseAuto = 1;

#----------------------------------------
# �ҳ�
#----------------------------------------
# �̾�ҳ�ȯ��Ψ(��Ψ��0.1%ñ��)
$HdisEarthquake = 5;  # �Ͽ�
$HdisTsunami    = 15; # ����
$HdisTyphoon    = 20; # ����
$HdisMeteo      = 15; # ���
$HdisHugeMeteo  = 5;  # �������
$HdisEruption   = 10; # ʮ��
$HdisFire       = 10; # �к�
$HdisMaizo      = 10; # ��¢��

# ��������
$HdisFallBorder = 90; # �����³��ι���(Hex��)
$HdisFalldown   = 30; # ���ι�����Ķ�������γ�Ψ

# ����
$HdisMonsBorder1 = 1000; # �͸����1(���å�٥�1)
$HdisMonsBorder2 = 2500; # �͸����2(���å�٥�2)
$HdisMonsBorder3 = 4000; # �͸����3(���å�٥�3)
$HdisMonster     = 3;    # ñ�����Ѥ�����νи�Ψ(0.01%ñ��)

# ����
$HmonsterNumber  = 8; 

# �ƴ��ˤ����ƽФƤ�����ä��ֹ�κ�����
$HmonsterLevel1  = 2; # ���󥸥�ޤ�    
$HmonsterLevel2  = 5; # ���Τ饴�����Ȥޤ�
$HmonsterLevel3  = 7; # ���󥰤��Τ�ޤ�(����)

# ̾��
@HmonsterName = 
    (
     '�ᥫ���Τ�',     # 0(��¤)
     '���Τ�',         # 1
     '���󥸥�',       # 2
     '��åɤ��Τ�',   # 3
     '���������Τ�',   # 4
     '���Τ饴������', # 5
     '������',         # 6
     '���󥰤��Τ�'    # 7
);

# �������ϡ����Ϥ������ü�ǽ�ϡ��и��͡����Τ�����
@HmonsterBHP     = ( 2, 1, 1, 3, 2, 1, 4, 5);
@HmonsterDHP     = ( 0, 2, 2, 2, 2, 0, 2, 2);
@HmonsterSpecial = ( 0, 0, 3, 0, 1, 2, 4, 0);
@HmonsterExp     = ( 5, 5, 7,12,15,10,20,30);
@HmonsterValue   = ( 0, 400, 500, 1000, 800, 300, 1500, 2000);

# �ü�ǽ�Ϥ����Ƥϡ�
# 0 �äˤʤ�
# 1 ­��®��(����2�⤢�뤯)
# 2 ­���ȤƤ�®��(���粿�⤢�뤯������)
# 3 ���������ϹŲ�
# 4 ����������ϹŲ�

# �����ե�����
@HmonsterImage =
    (
     'monster7.gif',
     'monster0.gif',
     'monster5.gif',
     'monster1.gif',
     'monster2.gif',
     'monster8.gif',
     'monster6.gif',
     'monster3.gif'
     );

# �����ե����뤽��2(�Ų���)
@HmonsterImage2 =
    ('', '', 'monster4.gif', '', '', '', 'monster4.gif', '');


#----------------------------------------
# ����
#----------------------------------------
# ���Ĥμ���
$HoilMoney = 1000;

# ���Ĥθϳ��Ψ
$HoilRatio = 40;

#----------------------------------------
# ��ǰ��
#----------------------------------------
# �����ढ�뤫
$HmonumentNumber = 3;

# ̾��
@HmonumentName = 
    (
     '��Υꥹ', 
     'ʿ�µ�ǰ��', 
     '�襤����'
    );

# �����ե�����
@HmonumentImage = 
    (
     'monument0.gif',
     'monument0.gif',
     'monument0.gif'
     );

#----------------------------------------
# �޴ط�
#----------------------------------------
# �������դ򲿥�������˽Ф���
$HturnPrizeUnit = 100;

# �ޤ�̾��
$Hprize[0] = '��������';
$Hprize[1] = '�˱ɾ�';
$Hprize[2] = 'Ķ�˱ɾ�';
$Hprize[3] = '����˱ɾ�';
$Hprize[4] = 'ʿ�¾�';
$Hprize[5] = 'Ķʿ�¾�';
$Hprize[6] = '���ʿ�¾�';
$Hprize[7] = '�����';
$Hprize[8] = 'Ķ�����';
$Hprize[9] = '��˺����';

#----------------------------------------
# �����ط�
#----------------------------------------
# <BODY>�����Υ��ץ����
my($htmlBody) = 'BGCOLOR="#EEFFFF"';

# ������Υ����ȥ�ʸ��
$Htitle = 'Ȣ����磲';

# ����
# �����ȥ�ʸ��
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# H1������
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# �礭��ʸ��
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# ���̾���ʤ�
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# �����ʤä����̾��
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# ���ɽ�ˤ����븫����
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# ��ȯ�ײ��̾��
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# �ҳ�
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';

# �̾��ʸ����(��������Ǥʤ���BODY�����Υ��ץ�����������ѹ����٤�
$HnormalColor = '#000000';

# ���ɽ�������°��
$HbgTitleCell   = 'BGCOLOR="#ccffcc"'; # ���ɽ���Ф�
$HbgNumberCell  = 'BGCOLOR="#ccffcc"'; # ���ɽ���
$HbgNameCell    = 'BGCOLOR="#ccffff"'; # ���ɽ���̾��
$HbgInfoCell    = 'BGCOLOR="#ccffff"'; # ���ɽ��ξ���
$HbgCommentCell = 'BGCOLOR="#ccffcc"'; # ���ɽ��������
$HbgInputCell   = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ�ե�����
$HbgMapCell     = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ��Ͽ�
$HbgCommandCell = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ����ϺѤ߷ײ�

#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ����ʹߤΥ�����ץȤϡ��ѹ�����뤳�Ȥ����ꤷ�Ƥ��ޤ��󤬡�
# �����äƤ⤫�ޤ��ޤ���
# ���ޥ�ɤ�̾�������ʤʤɤϲ��䤹���Ȼפ��ޤ���
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �Ƽ����
#----------------------------------------------------------------------
# ���Υե�����
$HthisFile = "$baseDir/hako-main.cgi";

# �Ϸ��ֹ�
$HlandSea      = 0;  # ��
$HlandWaste    = 1;  # ����
$HlandPlains   = 2;  # ʿ��
$HlandTown     = 3;  # Į��
$HlandForest   = 4;  # ��
$HlandFarm     = 5;  # ����
$HlandFactory  = 6;  # ����
$HlandBase     = 7;  # �ߥ��������
$HlandDefence  = 8;  # �ɱһ���
$HlandMountain = 9;  # ��
$HlandMonster  = 10; # ����
$HlandSbase    = 11; # �������
$HlandOil      = 12; # ��������
$HlandMonument = 13; # ��ǰ��
$HlandHaribote = 14; # �ϥ�ܥ�

# ���ޥ��
$HcommandTotal = 28; # ���ޥ�ɤμ���

# �ײ��ֹ������
# ���Ϸ�
$HcomPrepare  = 01; # ����
$HcomPrepare2 = 02; # �Ϥʤ餷
$HcomReclaim  = 03; # ���Ω��
$HcomDestroy  = 04; # ����
$HcomSellTree = 05; # Ȳ��

# ����
$HcomPlant    = 11; # ����
$HcomFarm     = 12; # ��������
$HcomFactory  = 13; # �������
$HcomMountain = 14; # �η�������
$HcomBase     = 15; # �ߥ�������Ϸ���
$HcomDbase    = 16; # �ɱһ��߷���
$HcomSbase    = 17; # ������Ϸ���
$HcomMonument = 18; # ��ǰ���¤
$HcomHaribote = 19; # �ϥ�ܥ�����

# ȯ�ͷ�
$HcomMissileNM   = 31; # �ߥ�����ȯ��
$HcomMissilePP   = 32; # PP�ߥ�����ȯ��
$HcomMissileST   = 33; # ST�ߥ�����ȯ��
$HcomMissileLD   = 34; # Φ���˲���ȯ��
$HcomSendMonster = 35; # �����ɸ�

# ���ķ�
$HcomDoNothing  = 41; # ��ⷫ��
$HcomSell       = 42; # ����͢��
$HcomMoney      = 43; # �����
$HcomFood       = 44; # �������
$HcomPropaganda = 45; # Ͷ�׳�ư
$HcomGiveup     = 46; # �������

# ��ư���Ϸ�
$HcomAutoPrepare  = 61; # �ե�����
$HcomAutoPrepare2 = 62; # �ե��Ϥʤ餷
$HcomAutoDelete   = 63; # �����ޥ�ɾõ�

# ����
@HcomList =
    ($HcomPrepare, $HcomSell, $HcomPrepare2, $HcomReclaim, $HcomDestroy,
     $HcomSellTree, $HcomPlant, $HcomFarm, $HcomFactory, $HcomMountain,
     $HcomBase, $HcomDbase, $HcomSbase, $HcomMonument, $HcomHaribote,
     $HcomMissileNM, $HcomMissilePP,
     $HcomMissileST, $HcomMissileLD, $HcomSendMonster, $HcomDoNothing,
     $HcomMoney, $HcomFood, $HcomPropaganda, $HcomGiveup,
     $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoDelete);

# �ײ��̾��������
$HcomName[$HcomPrepare]      = '����';
$HcomCost[$HcomPrepare]      = 5;
$HcomName[$HcomPrepare2]     = '�Ϥʤ餷';
$HcomCost[$HcomPrepare2]     = 100;
$HcomName[$HcomReclaim]      = '���Ω��';
$HcomCost[$HcomReclaim]      = 150;
$HcomName[$HcomDestroy]      = '����';
$HcomCost[$HcomDestroy]      = 200;
$HcomName[$HcomSellTree]     = 'Ȳ��';
$HcomCost[$HcomSellTree]     = 0;
$HcomName[$HcomPlant]        = '����';
$HcomCost[$HcomPlant]        = 50;
$HcomName[$HcomFarm]         = '��������';
$HcomCost[$HcomFarm]         = 20;
$HcomName[$HcomFactory]      = '�������';
$HcomCost[$HcomFactory]      = 100;
$HcomName[$HcomMountain]     = '�η�������';
$HcomCost[$HcomMountain]     = 300;
$HcomName[$HcomBase]         = '�ߥ�������Ϸ���';
$HcomCost[$HcomBase]         = 300;
$HcomName[$HcomDbase]        = '�ɱһ��߷���';
$HcomCost[$HcomDbase]        = 800;
$HcomName[$HcomSbase]        = '������Ϸ���';
$HcomCost[$HcomSbase]        = 8000;
$HcomName[$HcomMonument]     = '��ǰ���¤';
$HcomCost[$HcomMonument]     = 9999;
$HcomName[$HcomHaribote]     = '�ϥ�ܥ�����';
$HcomCost[$HcomHaribote]     = 1;
$HcomName[$HcomMissileNM]    = '�ߥ�����ȯ��';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PP�ߥ�����ȯ��';
$HcomCost[$HcomMissilePP]    = 50;
$HcomName[$HcomMissileST]    = 'ST�ߥ�����ȯ��';
$HcomCost[$HcomMissileST]    = 50;
$HcomName[$HcomMissileLD]    = 'Φ���˲���ȯ��';
$HcomCost[$HcomMissileLD]    = 100;
$HcomName[$HcomSendMonster]  = '�����ɸ�';
$HcomCost[$HcomSendMonster]  = 3000;
$HcomName[$HcomDoNothing]    = '��ⷫ��';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomSell]         = '����͢��';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomMoney]        = '�����';
$HcomCost[$HcomMoney]        = 100;
$HcomName[$HcomFood]         = '�������';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomPropaganda]   = 'Ͷ�׳�ư';
$HcomCost[$HcomPropaganda]   = 1000;
$HcomName[$HcomGiveup]       = '�������';
$HcomCost[$HcomGiveup]       = 0;
$HcomName[$HcomAutoPrepare]  = '���ϼ�ư����';
$HcomCost[$HcomAutoPrepare]  = 0;
$HcomName[$HcomAutoPrepare2] = '�Ϥʤ餷��ư����';
$HcomCost[$HcomAutoPrepare2] = 0;
$HcomName[$HcomAutoDelete]   = '���ײ�����ű��';
$HcomCost[$HcomAutoDelete]   = 0;

#----------------------------------------------------------------------
# �ѿ�
#----------------------------------------------------------------------

# COOKIE
my($defaultID);       # ���̾��
my($defaultTarget);   # �������åȤ�̾��


# ��κ�ɸ��
$HpointNumber = $HislandSize * $HislandSize;

#----------------------------------------------------------------------
# �ᥤ��
#----------------------------------------------------------------------

# jcode.pl��require
require($jcode);

# �����ץ��
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}�ȥåפ����${H_tagBig}</A>";

# ��å��򤫤���
if(!hakolock()) {
    # ��å�����
    # �إå�����
    tempHeader();

    # ��å����ԥ�å�����
    tempLockFail();

    # �եå�����
    tempFooter();

    # ��λ
    exit(0);
}

# ����ν����
srand(time^$$);

# COOKIE�ɤߤ���
cookieInput();

# CGI�ɤߤ���
cgiInput();

# ��ǡ������ɤߤ���
if(readIslandsFile($HcurrentID) == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}

# �ƥ�ץ졼�Ȥ�����
tempInitialize();

# COOKIE����
cookieOutput();

# �إå�����
tempHeader();

if($HmainMode eq 'turn') {
    # ������ʹ�
    require('hako-turn.cgi');
    require('hako-top.cgi');
    turnMain();

} elsif($HmainMode eq 'new') {
    # ��ο�������
    require('hako-turn.cgi');
    require('hako-map.cgi');
    newIslandMain();

} elsif($HmainMode eq 'print') {
    # �Ѹ��⡼��
    require('hako-map.cgi');
    printIslandMain();

} elsif($HmainMode eq 'owner') {

    # ��ȯ�⡼��
    require('hako-map.cgi');
    ownerMain();

} elsif($HmainMode eq 'command') {
    # ���ޥ�����ϥ⡼��
    require('hako-map.cgi');
    commandMain();

} elsif($HmainMode eq 'comment') {
    # ���������ϥ⡼��
    require('hako-map.cgi');
    commentMain();

} elsif($HmainMode eq 'lbbs') {

    # ������Ǽ��ĥ⡼��
    require('hako-map.cgi');
    localBbsMain();

} elsif($HmainMode eq 'change') {
    # �����ѹ��⡼��
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} else {
    # ����¾�ξ��ϥȥåץڡ����⡼��
    require('hako-top.cgi');
    topPageMain();
}

# �եå�����
tempFooter();

# ��λ
exit(0);

# ���ޥ�ɤ����ˤ��餹
sub slideFront {
    my($command, $number) = @_;
    my($i);

    # ���줾�줺�餹
    splice(@$command, $number, 1);

    # �Ǹ�˻�ⷫ��
    $command->[$HcommandMax - 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0
	};
}

# ���ޥ�ɤ��ˤ��餹
sub slideBack {
    my($command, $number) = @_;
    my($i);

    # ���줾�줺�餹
    return if $number == $#$command;
    pop(@$command);
    splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# ��ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readIslandsFile {
    my($num) = @_; # 0�����Ϸ��ɤߤ��ޤ�
                   # -1�������Ϸ����ɤ�
                   # �ֹ���Ȥ�������Ϸ��������ɤߤ���

    # �ǡ����ե�����򳫤�
    if(!open(IN, "${HdirName}/hakojima.dat")) {
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	if(!open(IN, "${HdirName}/hakojima.dat")) {
	    return 0;
	}
    }

    # �ƥѥ�᡼�����ɤߤ���
    $HislandTurn     = int(<IN>); # �������
    if($HislandTurn == 0) {
	return 0;
    }
    $HislandLastTime = int(<IN>); # �ǽ���������
    if($HislandLastTime == 0) {
	return 0;
    }
    $HislandNumber   = int(<IN>); # ������
    $HislandNextID   = int(<IN>); # ���˳�����Ƥ�ID

    # ���������Ƚ��
    my($now) = time;
    if((($Hdebug == 1) && 
	($HmainMode eq 'Hdebugturn')) ||
       (($now - $HislandLastTime) >= $HunitTime)) {
	$HmainMode = 'turn';
	$num = -1; # �����ɤߤ���
    }

    # ����ɤߤ���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 $Hislands[$i] = readIsland($num);
	 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
    }

    # �ե�������Ĥ���
    close(IN);

    return 1;
}

# ��ҤȤ��ɤߤ���
sub readIsland {
    my($num) = @_;
    my($name, $id, $prize, $absent, $comment, $password, $money, $food,
       $pop, $area, $farm, $factory, $mountain, $score);
    $name = <IN>; # ���̾��
    chomp($name);
    if($name =~ s/,(.*)$//g) {
	$score = int($1);
    } else {
	$score = 0;
    }
    $id = int(<IN>); # ID�ֹ�
    $prize = <IN>; # ����
    chomp($prize);
    $absent = int(<IN>); # Ϣ³��ⷫ���
    $comment = <IN>; # ������
    chomp($comment);
    $password = <IN>; # �Ź沽�ѥ����
    chomp($password);
    $money = int(<IN>);    # ���
    $food = int(<IN>);     # ����
    $pop = int(<IN>);      # �͸�
    $area = int(<IN>);     # ����
    $farm = int(<IN>);     # ����
    $factory = int(<IN>);  # ����
    $mountain = int(<IN>); # �η���

    # HidToName�ơ��֥����¸
    $HidToName{$id} = $name;	# 

    # �Ϸ�
    my(@land, @landValue, $line, @command, @lbbs);

    if(($num == -1) || ($num == $id)) {
	if(!open(IIN, "${HdirName}/island.$id")) {
	    rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
	    if(!open(IIN, "${HdirName}/island.$id")) {
		exit(0);
	    }
	}
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    $line = <IIN>;
	    for($x = 0; $x < $HislandSize; $x++) {
		$line =~ s/^(.)(..)//;
		$land[$x][$y] = hex($1);
		$landValue[$x][$y] = hex($2);
	    }
	}

	# ���ޥ��
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    $line = <IIN>;
	    $line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
	    $command[$i] = {
		'kind' => int($1),
		'target' => int($2),
		'x' => int($3),
		'y' => int($4),
		'arg' => int($5)
		}
	}

	# ������Ǽ���
	for($i = 0; $i < $HlbbsMax; $i++) {
	    $line = <IIN>;
	    chomp($line);
	    $lbbs[$i] = $line;
	}

	close(IIN);
    }

    # �緿�ˤ����֤�
    return {
	 'name' => $name,
	 'id' => $id,
	 'score' => $score,
	 'prize' => $prize,
	 'absent' => $absent,
	 'comment' => $comment,
	 'password' => $password,
	 'money' => $money,
	 'food' => $food,
	 'pop' => $pop,
	 'area' => $area,
	 'farm' => $farm,
	 'factory' => $factory,
	 'mountain' => $mountain,
	 'land' => \@land,
	 'landValue' => \@landValue,
	 'command' => \@command,
	 'lbbs' => \@lbbs,
    };
}

# ����ǡ����񤭹���
sub writeIslandsFile {
    my($num) = @_;

    # �ե�����򳫤�
    open(OUT, ">${HdirName}/hakojima.tmp");

    # �ƥѥ�᡼���񤭹���
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";

    # ��ν񤭤���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIsland($Hislands[$i], $num);
    }

    # �ե�������Ĥ���
    close(OUT);

    # �����̾���ˤ���
    unlink("${HdirName}/hakojima.dat");
    rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
}

# ��ҤȤĽ񤭹���
sub writeIsland {
    my($island, $num) = @_;
    my($score);
    $score = int($island->{'score'});
    print OUT $island->{'name'} . ",$score\n";
    print OUT $island->{'id'} . "\n";
    print OUT $island->{'prize'} . "\n";
    print OUT $island->{'absent'} . "\n";
    print OUT $island->{'comment'} . "\n";
    print OUT $island->{'password'} . "\n";
    print OUT $island->{'money'} . "\n";
    print OUT $island->{'food'} . "\n";
    print OUT $island->{'pop'} . "\n";
    print OUT $island->{'area'} . "\n";
    print OUT $island->{'farm'} . "\n";
    print OUT $island->{'factory'} . "\n";
    print OUT $island->{'mountain'} . "\n";

    # �Ϸ�
    if(($num <= -1) || ($num == $island->{'id'})) {
	open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}");

	my($land, $landValue);
	$land = $island->{'land'};
	$landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    for($x = 0; $x < $HislandSize; $x++) {
		printf IOUT ("%x%02x", $land->[$x][$y], $landValue->[$x][$y]);
	    }
	    print IOUT "\n";
	}

	# ���ޥ��
	my($command, $cur, $i);
	$command = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
	    printf IOUT ("%d,%d,%d,%d,%d\n", 
			 $command->[$i]->{'kind'},
			 $command->[$i]->{'target'},
			 $command->[$i]->{'x'},
			 $command->[$i]->{'y'},
			 $command->[$i]->{'arg'}
			 );
	}

	# ������Ǽ���
	my($lbbs);
	$lbbs = $island->{'lbbs'};
	for($i = 0; $i < $HlbbsMax; $i++) {
	    print IOUT $lbbs->[$i] . "\n";
	}

	close(IOUT);
	unlink("${HdirName}/island.$island->{'id'}");
	rename("${HdirName}/islandtmp.$island->{'id'}", "${HdirName}/island.$island->{'id'}");
    }
}

#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------

# ɸ����Ϥؤν���
sub out {
    print STDOUT jcode::sjis($_[0]);
}

# �ǥХå���
sub HdebugOut {
   open(DOUT, ">>debug.log");
   print DOUT ($_[0]);
   close(DOUT);
}

# CGI���ɤߤ���
sub cgiInput {
    my($line, $getLine);

    # ���Ϥ������ä����ܸ쥳���ɤ�EUC��
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $line = jcode::euc($line);
    $line =~ s/[\x00-\x1f\,]//g;

    # GET�Τ�Ĥ�������
    $getLine = $ENV{'QUERY_STRING'};

    # �оݤ���
    if($line =~ /CommandButton([0-9]+)=/) {
	# ���ޥ�������ܥ���ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }

    if($line =~ /ISLANDNAME=([^\&]*)\&/){
	# ̾������ξ��
	$HcurrentName = cutColumn($1, 32);
    }

    if($line =~ /ISLANDID=([0-9]+)\&/){
	# ����¾�ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }

    # �ѥ����
    if($line =~ /OLDPASS=([^\&]*)\&/) {
	$HoldPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$HinputPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD2=([^\&]*)\&/) {
	$HinputPassword2 = $1;
    }

    # ��å�����
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$Hmessage = cutColumn($1, 80);
    }

    # ������Ǽ���
    if($line =~ /LBBSNAME=([^\&]*)\&/) {
	$HlbbsName = $1;
	$HdefaultName = $1;
    }
    if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
	$HlbbsMessage = cutColumn($1, 80);
    }

    # main mode�μ���
    if($line =~ /TurnButton/) {
	if($Hdebug == 1) {
	    $HmainMode = 'Hdebugturn';
	}
    } elsif($line =~ /OwnerButton/) {
	$HmainMode = 'owner';
    } elsif($getLine =~ /Sight=([0-9]*)/) {
	$HmainMode = 'print';
	$HcurrentID = $1;
    } elsif($line =~ /NewIslandButton/) {
	$HmainMode = 'new';
    } elsif($line =~ /LbbsButton(..)([0-9]*)/) {
	$HmainMode = 'lbbs';
	if($1 eq 'SS') {
	    # �Ѹ���
	    $HlbbsMode = 0;
	} elsif($1 eq 'OW') {
	    # ���
	    $HlbbsMode = 1;
	} else {
	    # ���
	    $HlbbsMode = 2;
	}
	$HcurrentID = $2;

	# ������⤷��ʤ��Τǡ��ֹ�����
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;

    } elsif($line =~ /ChangeInfoButton/) {
	$HmainMode = 'change';
    } elsif($line =~ /MessageButton([0-9]*)/) {
	$HmainMode = 'comment';
	$HcurrentID = $1;
    } elsif($line =~ /CommandButton/) {
	$HmainMode = 'command';

	# ���ޥ�ɥ⡼�ɤξ�硢���ޥ�ɤμ���
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;
	$line =~ /COMMAND=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HcommandArg = $1;
	$line =~ /TARGETID=([^\&]*)\&/;
	$HcommandTarget = $1;
	$defaultTarget = $1;
	$line =~ /POINTX=([^\&]*)\&/;
	$HcommandX = $1;
	$HdefaultX = $1;
        $line =~ /POINTY=([^\&]*)\&/;
	$HcommandY = $1;
	$HdefaultY = $1;
	$line =~ /COMMANDMODE=(write|insert|delete)/;
	$HcommandMode = $1;
    } else {
	$HmainMode = 'top';
    }

}


#cookie����
sub cookieInput {
    my($cookie);

    $cookie = jcode::euc($ENV{'HTTP_COOKIE'});

    if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
	$defaultID = $1;
    }
    if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
	$HdefaultPassword = $1;
    }
    if($cookie =~ /${HthisFile}TARGETISLANDID=\(([^\)]*)\)/) {
	$defaultTarget = $1;
    }
    if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
	$HdefaultName = $1;
    }
    if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
	$HdefaultX = $1;
    }
    if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
	$HdefaultY = $1;
    }
    if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
	$HdefaultKind = $1;
    }

}

#cookie����
sub cookieOutput {
    my($cookie, $info);

    # �ä�����¤�����
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # ���� + 30��

    # 2������
    $year += 1900;
    if ($date < 10) { $date = "0$date"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min  = "0$min"; }
    if ($sec < 10) { $sec  = "0$sec"; }

    # ������ʸ����
    $day = ("Sunday", "Monday", "Tuesday", "Wednesday",
	    "Thursday", "Friday", "Saturday")[$day];

    # ���ʸ����
    $mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
	    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

    # �ѥ��ȴ��¤Υ��å�
    $info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
    $cookie = '';
    
    if(($HcurrentID) && ($HmainMode eq 'owner')){
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
    }
    if($HinputPassword) {
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
    }
    if($HcommandTarget) {
	$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
    }
    if($HlbbsName) {
	$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
    }
    if($HcommandX) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
    }
    if($HcommandY) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
    }
    if($HcommandKind) {
	# ��ư�ϰʳ�
	$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
    }

    out($cookie);
}

#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------
sub hakolock {
    if($lockMode == 1) {
	# directory����å�
	return hakolock1();

    } elsif($lockMode == 2) {
	# flock����å�
	return hakolock2();
    } elsif($lockMode == 3) {
	# symlink����å�
	return hakolock3();
    } else {
	# �̾�ե����뼰��å�
	return hakolock4();
    }
}

sub hakolock1 {
    # ��å���
    if(mkdir('hakojimalock', $HdirMode)) {
	# ����
	return 1;
    } else {
	# ����
	my($b) = (stat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # �������
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

sub hakolock2 {
    open(LOCKID, '>>hakojimalockflock');
    if(flock(LOCKID, 2)) {
	# ����
	return 1;
    } else {
	# ����
	return 0;
    }
}

sub hakolock3 {
    # ��å���
    if(symlink('hakojimalockdummy', 'hakojimalock')) {
	# ����
	return 1;
    } else {
	# ����
	my($b) = (lstat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # �������
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

sub hakolock4 {
    # ��å���
    if(unlink('key-free')) {
	# ����
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    } else {
	# ��å����֥����å�
	if(!open(IN, 'key-locked')) {
	    return 0;
	}

	my($t);
	$t = <IN>;
	close(IN);
	if(($t != 0) && (($t + $unlockTime) < time)) {
	    # 120�ðʾ�вᤷ�Ƥ��顢����Ū�˥�å��򳰤�
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

# ��å��򳰤�
sub unlock {
    if($lockMode == 1) {
	# directory����å�
	rmdir('hakojimalock');

    } elsif($lockMode == 2) {
	# flock����å�
	close(LOCKID);

    } elsif($lockMode == 3) {
	# symlink����å�
	unlink('hakojimalock');
    } else {
	# �̾�ե����뼰��å�
	my($i);
	$i = rename('key-locked', 'key-free');
    }
}

# �����������֤�
sub min {
    return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# �ѥ���ɥ��󥳡���
sub encode {
    if($cryptOn == 1) {
	return crypt($_[0], 'h2');
    } else {
	return $_[0];
    }
}

# �ѥ���ɥ����å�
sub checkPassword {
    my($p1, $p2) = @_;

    # null�����å�
    if($p2 eq '') {
	return 0;
    }

    # �ޥ������ѥ���ɥ����å�
    if($masterPassword eq $p2) {
	return 1;
    }

    # ����Υ����å�
    if($p1 eq encode($p2)) {
	return 1;
    }

    return 0;
}

# 1000��ñ�̴ݤ�롼����
sub aboutMoney {
    my($m) = @_;
    if($m < 500) {
	return "����500${HunitMoney}̤��";
    } else {
	$m = int(($m + 500) / 1000);
	return "����${m}000${HunitMoney}";
    }
}

# ����������ʸ���ν���
sub htmlEscape {
    my($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/\"/&quot;/g; #"
    return $s;
}

# 80�������ڤ�·��
sub cutColumn {
    my($s, $c) = @_;
    if(length($s) <= $c) {
	return $s;
    } else {
	# ���80�����ˤʤ�ޤ��ڤ���
	my($ss) = '';
	my($count) = 0;
	while($count < $c) {
	    $s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
	    if($1) {
		$ss .= $1;
		$count ++;
	    } else {
		$ss .= $2;
	    }
	    $count ++;
	}
	return $ss;
    }
}

# ���̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToNumber {
    my($name) = @_;

    # ���礫��õ��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # ���Ĥ���ʤ��ä����
    return -1;
}

# ���äξ���
sub monsterSpec {
    my($lv) = @_;

    # ����
    my($kind) = int($lv / 10);

    # ̾��
    my($name);
    $name = $HmonsterName[$kind];

    # ����
    my($hp) = $lv - ($kind * 10);
    
    return ($kind, $name, $hp);
}

# �и��Ϥ����٥�򻻽�
sub expToLevel {
    my($kind, $exp) = @_;
    my($i);
    if($kind == $HlandBase) {
	# �ߥ��������
	for($i = $maxBaseLevel; $i > 1; $i--) {
	    if($exp >= $baseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    } else {
	# �������
	for($i = $maxSBaseLevel; $i > 1; $i--) {
	    if($exp >= $sBaseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    }

}

# (0,0)����(size - 1, size - 1)�ޤǤο��������ŤĽФƤ���褦��
# (@Hrpx, @Hrpy)������
sub makeRandomPointArray {
    # �����
    my($y);
    @Hrpx = (0..$HislandSize-1) x $HislandSize;
    for($y = 0; $y < $HislandSize; $y++) {
	push(@Hrpy, ($y) x $HislandSize);
    }

    # ����åե�
    my ($i);
    for ($i = $HpointNumber; --$i; ) {
	my($j) = int(rand($i+1)); 
	if($i == $j) { next; }
	@Hrpx[$i,$j] = @Hrpx[$j,$i];
	@Hrpy[$i,$j] = @Hrpy[$j,$i];
    }
}

# 0����(n - 1)�����
sub random {
    return int(rand(1) * $_[0]);
}

#----------------------------------------------------------------------
# ��ɽ��
#----------------------------------------------------------------------
# �ե������ֹ����ǥ�ɽ��
sub logFilePrint {
    my($fileNumber, $id, $mode) = @_;
    open(LIN, "${HdirName}/hakojima.log$_[0]");
    my($line, $m, $turn, $id1, $id2, $message);
    while($line = <LIN>) {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# ��̩�ط�
	if($m == 1) {
	    if(($mode == 0) || ($id1 != $id)) {
		# ��̩ɽ�������ʤ�
		next;
	    }
	    $m = '<B>(��̩)</B>';
	} else {
	    $m = '';
	}

	# ɽ��Ū�Τ�
	if($id != 0) {
	    if(($id != $id1) &&
	       ($id != $id2)) {
		next;
	    }
	}

	# ɽ��
	out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
    }
    close(LIN);
}

#----------------------------------------------------------------------
# �ƥ�ץ졼��
#----------------------------------------------------------------------
# �����
sub tempInitialize {
    # �祻�쥯��(�ǥե���ȼ�ʬ)
    $HislandList = getIslandList($defaultID);
    $HtargetList = getIslandList($defaultTarget);
}

# ��ǡ����Υץ�������˥塼��
sub getIslandList {
    my($select) = @_;
    my($list, $name, $id, $s, $i);

    #��ꥹ�ȤΥ�˥塼
    $list = '';
    for($i = 0; $i < $HislandNumber; $i++) {
	$name = $Hislands[$i]->{'name'};
	$id = $Hislands[$i]->{'id'};
	if($id eq $select) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .=
	    "<OPTION VALUE=\"$id\" $s>${name}��\n";
    }
    return $list;
}


# �إå�
sub tempHeader {
    out(<<END);
Content-type: text/html

<HTML>
<HEAD>
<TITLE>
$Htitle
</TITLE>
<BASE HREF="$imageDir/">
</HEAD>
<BODY $htmlBody>
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">Ȣ����祹����ץ����۸�</A><HR>
END
}

# �եå�
sub tempFooter {
    out(<<END);
<HR>
<P align=center>
������:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
�Ǽ���(<A HREF="$bbs">$bbs</A>)<BR>
�ȥåץڡ���(<A HREF="$toppage">$toppage</A>)<BR>
Ȣ�����Υڡ���(<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html</A>)<BR>
</P>
</BODY>
</HTML>
END
}

# ��å�����
sub tempLockFail {
    # �����ȥ�
    out(<<END);
${HtagBig_}Ʊ�������������顼�Ǥ���<BR>
�֥饦���Ρ����ץܥ���򲡤���<BR>
���Ф餯�ԤäƤ�����٤����������${H_tagBig}$HtempBack
END
}

# �������
sub tempUnlock {
    # �����ȥ�
    out(<<END);
${HtagBig_}����Υ����������۾ｪλ���ä��褦�Ǥ���<BR>
��å�����������ޤ�����${H_tagBig}$HtempBack
END
}

# hakojima.dat���ʤ�
sub tempNoDataFile {
    out(<<END);
${HtagBig_}�ǡ����ե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɴְ㤤
sub tempWrongPassword {
    out(<<END);
${HtagBig_}�ѥ���ɤ��㤤�ޤ���${H_tagBig}$HtempBack
END
}

# ��������ȯ��
sub tempProblem {
    out(<<END);
${HtagBig_}����ȯ�����Ȥꤢ������äƤ���������${H_tagBig}$HtempBack
END
}
