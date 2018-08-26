#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �Ͽޥ⡼�ɥ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub printIslandMain {
    # ����
    unlock();

    # id�������ֹ�����
    $HcurrentNumber = $HidToNumber{$HcurrentID};

    # �ʤ��������礬�ʤ����
    if($HcurrentNumber eq '') {
	tempProblem();
	return;
    }

    # ̾���μ���
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

    # �Ѹ�����
    tempPrintIslandHead(); # �褦����!!
    islandInfo(); # ��ξ���
    islandMap(0); # ����Ͽޡ��Ѹ��⡼��

    # �����������Ǽ���
    if($HuseLbbs) {
	tempLbbsHead();     # ������Ǽ���
	tempLbbsInput();   # �񤭹��ߥե�����
	tempLbbsContents(); # �Ǽ�������
    }

    # �ᶷ
    tempRecent(0);
}

#----------------------------------------------------------------------
# ��ȯ�⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub ownerMain {
    # ����
    unlock();

    # �⡼�ɤ�����
    $HmainMode = 'owner';

    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	tempWrongPassword();
	return;
    }

    # ��ȯ����
    tempOwner(); # �ֳ�ȯ�ײ��

    # �����������Ǽ���
    if($HuseLbbs) {
	tempLbbsHead();     # ������Ǽ���
	tempLbbsInputOW();   # �񤭹��ߥե�����
	tempLbbsContents(); # �Ǽ�������
    }

    # �ᶷ
    tempRecent(1);
}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commandMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # �⡼�ɤ�ʬ��
    my($command) = $island->{'command'};

    if($HcommandMode eq 'delete') {
	slideFront($command, $HcommandPlanNumber);
	tempCommandDelete();
    } elsif(($HcommandKind == $HcomAutoPrepare) ||
	    ($HcommandKind == $HcomAutoPrepare2)) {
	# �ե����ϡ��ե��Ϥʤ餷
	# ��ɸ�������
	makeRandomPointArray();
	my($land) = $island->{'land'};

	# ���ޥ�ɤμ������
	my($kind) = $HcomPrepare;
	if($HcommandKind == $HcomAutoPrepare2) {
	    $kind = $HcomPrepare2;
	}

	my($i) = 0;
	my($j) = 0;
	while(($j < $HpointNumber) && ($i < $HcommandMax)) {
	    my($x) = $Hrpx[$j];
	    my($y) = $Hrpy[$j];
	    if($land->[$x][$y] == $HlandWaste) {
		slideBack($command, $HcommandPlanNumber);
		$command->[$HcommandPlanNumber] = {
		    'kind' => $kind,
		    'target' => 0,
		    'x' => $x,
		    'y' => $y,
		    'arg' => 0
		    };
		$i++;
	    }
	    $j++;
	}
	tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoDelete) {
	# ���ä�
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    slideFront($command, $HcommandPlanNumber);
	}
	tempCommandDelete();
    } else {
	if($HcommandMode eq 'insert') {
	    slideBack($command, $HcommandPlanNumber);
	}
	tempCommandAdd();
	# ���ޥ�ɤ���Ͽ
	$command->[$HcommandPlanNumber] = {
	    'kind' => $HcommandKind,
	    'target' => $HcommandTarget,
	    'x' => $HcommandX,
	    'y' => $HcommandY,
	    'arg' => $HcommandArg
	    };
    }

    # �ǡ����ν񤭽Ф�
    writeIslandsFile($HcurrentID);

    # owner mode��
    ownerMain();

}

#----------------------------------------------------------------------
# ���������ϥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commentMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �ѥ����
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ��å������򹹿�
    $island->{'comment'} = htmlEscape($Hmessage);

    # �ǡ����ν񤭽Ф�
    writeIslandsFile($HcurrentID);

    # �����ȹ�����å�����
    tempComment();

    # owner mode��
    ownerMain();
}

#----------------------------------------------------------------------
# ������Ǽ��ĥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub localBbsMain {
    # id�������ֹ�����
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];

    # �ʤ��������礬�ʤ����
    if($HcurrentNumber eq '') {
	unlock();
	tempProblem();
	return;
    }

    # ����⡼�ɤ���ʤ���̾������å��������ʤ����
    if($HlbbsMode != 2) {
	if(($HlbbsName eq '') || ($HlbbsName eq '')) {
	    unlock();
	    tempLbbsNoMessage();
	    return;
	}
    }

    # �Ѹ��ԥ⡼�ɤ���ʤ����ϥѥ���ɥ����å�
    if($HlbbsMode != 0) {
	if(!checkPassword($island->{'password'},$HinputPassword)) {
	    # password�ְ㤤
	    unlock();
	    tempWrongPassword();
	    return;
	}
    }

    my($lbbs);
    $lbbs = $island->{'lbbs'};

    # �⡼�ɤ�ʬ��
    if($HlbbsMode == 2) {
	# ����⡼��
	# ��å����������ˤ��餹
	slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	tempLbbsDelete();
    } else {
	# ��Ģ�⡼��
	# ��å���������ˤ��餹
	slideLbbsMessage($lbbs);

	# ��å������񤭹���
	my($message);
	if($HlbbsMode == 0) {
	    $message = '0';
	} else {
	    $message = '1';
	}
	$HlbbsName = "$HislandTurn��" . htmlEscape($HlbbsName);
	$HlbbsMessage = htmlEscape($HlbbsMessage);
	$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage";

	tempLbbsAdd();
    }

    # �ǡ����񤭽Ф�
    writeIslandsFile($HcurrentID);

    # ��ȤΥ⡼�ɤ�
    if($HlbbsMode == 0) {
	printIslandMain();
    } else {
	ownerMain();
    }
}

# ������Ǽ��ĤΥ�å��������ĸ��ˤ��餹
sub slideLbbsMessage {
    my($lbbs) = @_;
    my($i);
#    pop(@$lbbs);
#    push(@$lbbs, $lbbs->[0]);
    pop(@$lbbs);
    unshift(@$lbbs, $lbbs->[0]);
}

# ������Ǽ��ĤΥ�å������������ˤ��餹
sub slideBackLbbsMessage {
    my($lbbs, $number) = @_;
    my($i);
    splice(@$lbbs, $number, 1);
    $lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# ����Ͽ�
#----------------------------------------------------------------------

# �����ɽ��
sub islandInfo {
    my($island) = $Hislands[$HcurrentNumber];
    # ����ɽ��
    my($rank) = $HcurrentNumber + 1;
    my($farm) = $island->{'farm'};
    my($factory) = $island->{'factory'};
    my($mountain) = $island->{'mountain'};
    $farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
    $factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
    $mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";

    my($mStr1) = '';
    my($mStr2) = '';
    if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
	# ̵���ޤ���owner�⡼��
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
    } elsif($HhideMoneyMode == 2) {
	my($mTmp) = aboutMoney($island->{'money'});

	# 1000��ñ�̥⡼��
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
    }
    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�η��쵬��${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${mountain}</NOBR></TD>
</TR>
</TABLE></CENTER>
END
}

# �Ͽޤ�ɽ��
# ������1�ʤ顢�ߥ�����������򤽤Τޤ�ɽ��
sub islandMap {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
    # �Ϸ����Ϸ��ͤ����
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($l, $lv);

    # ���ޥ�ɼ���
    my($command) = $island->{'command'};
    my($com, @comStr, $i);
    if($HmainMode eq 'owner') {
	for($i = 0; $i < $HcommandMax; $i++) {
	    my($j) = $i + 1;
	    $com = $command->[$i];
	    if($com->{'kind'} < 20) {
		$comStr[$com->{'x'}][$com->{'y'}] .=
		    " [${j}]$HcomName[$com->{'kind'}]";
	    }
	}
    }

    # ��ɸ(��)�����
    out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

    # ���Ϸ�����Ӳ��Ԥ����
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# �������ܤʤ��ֹ�����
        if(($y % 2) == 0) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# ���Ϸ������
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
	}

	# ������ܤʤ��ֹ�����
        if(($y % 2) == 1) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# ���Ԥ����
	out("<BR>");
    }
    out("</TD></TR></TABLE></CENTER>\n");
}

sub landString {
    my($l, $lv, $x, $y, $mode, $comStr) = @_;
    my($point) = "($x,$y)";
    my($image, $alt);

    if($l == $HlandSea) {

	if($lv == 1) {
	    # ����
	    $image = 'land14.gif';
	    $alt = '��(����)';
        } else {
            # ��
	    $image = 'land0.gif';
	    $alt = '��';
        }
    } elsif($l == $HlandWaste) {
	# ����
	if($lv == 1) {
	    $image = 'land13.gif'; # ������
	    $alt = '����';
	} else {
	    $image = 'land1.gif';
	    $alt = '����';
	}
    } elsif($l == $HlandPlains) {
	# ʿ��
	$image = 'land2.gif';
	$alt = 'ʿ��';
    } elsif($l == $HlandForest) {
	# ��
	if($mode == 1) {
	    $image = 'land6.gif';
	    $alt = "��(${lv}$HunitTree)";
	} else {
	    # �Ѹ��Ԥξ����ڤ��ܿ�����
	    $image = 'land6.gif';
	    $alt = '��';
	}
    } elsif($l == $HlandTown) {
	# Į
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '¼';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = 'Į';
	} else {
	    $p = 5;
	    $n = '�Ի�';
	}

	$image = "land${p}.gif";
	$alt = "$n(${lv}$HunitPop)";
    } elsif($l == $HlandFarm) {
	# ����
	$image = 'land7.gif';
	$alt = "����(${lv}0${HunitPop}����)";
    } elsif($l == $HlandFactory) {
	# ����
	$image = 'land8.gif';
	$alt = "����(${lv}0${HunitPop}����)";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # �Ѹ��Ԥξ��Ͽ��Τդ�
	    $image = 'land6.gif';
	    $alt = '��';
	} else {
	    # �ߥ��������
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $alt = "�ߥ�������� (��٥� ${level}/�и��� $lv)";
	}
    } elsif($l == $HlandSbase) {
	# �������
	if($mode == 0) {
	    # �Ѹ��Ԥξ��ϳ��Τդ�
	    $image = 'land0.gif';
	    $alt = '��';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $alt = "������� (��٥� ${level}/�и��� $lv)";
	}
    } elsif($l == $HlandDefence) {
	# �ɱһ���
	$image = 'land10.gif';
	$alt = '�ɱһ���';
    } elsif($l == $HlandHaribote) {
	# �ϥ�ܥ�
	$image = 'land10.gif';
	if($mode == 0) {
	    # �Ѹ��Ԥξ����ɱһ��ߤΤդ�
	    $alt = '�ɱһ���';
	} else {
	    $alt = '�ϥ�ܥ�';
	}
    } elsif($l == $HlandOil) {
	# ��������
	$image = 'land16.gif';
	$alt = '��������';
    } elsif($l == $HlandMountain) {
	# ��
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $alt = "��(�η���${lv}0${HunitPop}����)";
	} else {
	    $image = 'land11.gif';
	    $alt = '��';
	}
    } elsif($l == $HlandMonument) {
	# ��ǰ��
	$image = $HmonumentImage[$lv];
	$alt = $HmonumentName[$lv];
    } elsif($l == $HlandMonster) {
	# ����
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# �Ų���?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # �Ų���
	    $image = $HmonsterImage2[$kind];
	}
	$alt = "����$name(����${hp})";
    }


    # ��ȯ���̤ξ��ϡ���ɸ����
    if($mode == 1) {
	out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
    }

    out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

    # ��ɸ�����Ĥ�
    if($mode == 1) {
	out("</A>");
    }
}


#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
# ���̥�ɽ��
sub logPrintLocal {
    my($mode) = @_;
    my($i);
    for($i = 0; $i < $HlogMax; $i++) {
	logFilePrint($i, $HcurrentID, $mode);
    }
}

# ������ؤ褦��������
sub tempPrintIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}�ؤ褦��������${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �����糫ȯ�ײ�
sub tempOwner {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
    document.forms[0].elements[4].options[x].selected = true;
    document.forms[0].elements[5].options[y].selected = true;
    return true;
}

function ns(x) {
    document.forms[0].elements[2].options[x].selected = true;
    return true;
}

//-->
</SCRIPT>
END

    islandInfo();

    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TD $HbgInputCell >
<CENTER>
<FORM action="$HthisFile" method=POST>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER>
END
    # �ײ��ֹ�
    my($j, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }

    out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><BR>
<SELECT NAME=COMMAND>
END

    #���ޥ��
    my($kind, $cost, $s);
    for($i = 0; $i < $HcommandTotal; $i++) {
	$kind = $HcomList[$i];
	$cost = $HcomCost[$kind];
	if($cost == 0) {
	    $cost = '̵��'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} else {
	    $cost .= $HunitMoney;
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>��ɸ(</B>
<SELECT NAME=POINTX>

END
    for($i = 0; $i < $HislandSize; $i++) {
	if($i == $HdefaultX) {
	    out("<OPTION VALUE=$i SELECTED>$i\n");
        } else {
	    out("<OPTION VALUE=$i>$i\n");
        }
    }

    out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

    for($i = 0; $i < $HislandSize; $i++) {
	if($i == $HdefaultY) {
	    out("<OPTION VALUE=$i SELECTED>$i\n");
        } else {
	    out("<OPTION VALUE=$i>$i\n");
        }
    }
    out(<<END);
</SELECT><B>)</B>
<HR>
<B>����</B><SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>��ɸ����</B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>ư��</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>����
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>���<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>���
<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>

</CENTER>
</FORM>
</TD>
<TD $HbgMapCell>
END
    islandMap(1);    # ����Ͽޡ���ͭ�ԥ⡼��
    out(<<END);
</TD>
<TD $HbgCommandCell>
END
    for($i = 0; $i < $HcommandMax; $i++) {
	tempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
    }

    out(<<END);

</TD>
</TR>
</TABLE>
</CENTER>
<HR>
<CENTER>
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
������<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
�ѥ����<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</FORM>
</CENTER>
END

}

# ���ϺѤߥ��ޥ��ɽ��
sub tempCommand {
    my($number, $command) = @_;
    my($kind, $target, $x, $y, $arg) =
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );
    my($name) = "$HtagComName_${HcomName[$kind]}$H_tagComName";
    my($point) = "$HtagName_($x,$y)$H_tagName";
    $target = $HidToName{$target};
    if($target eq '') {
	$target = "̵��";
    }
    $target = "$HtagName_${target}��$H_tagName";
    my($value) = $arg * $HcomCost[$kind];
    if($value == 0) {
	$value = $HcomCost[$kind];
    }
    if($value < 0) {
	$value = -$value;
	$value = "$value$HunitFood";
    } else {
	$value = "$value$HunitMoney";
    }
    $value = "$HtagName_$value$H_tagName";

    my($j) = sprintf("%02d��", $number + 1);

    out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

    if(($kind == $HcomDoNothing) ||
       ($kind == $HcomGiveup)) {
	out("$name");
    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileLD)) {
	# �ߥ������
	my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
	out("$target$point��$name($HtagName_$n$H_tagName)");
    } elsif($kind == $HcomSendMonster) {
	# �����ɸ�
	out("$target��$name");
    } elsif($kind == $HcomSell) {
	# ����͢��
	out("$name$value");
    } elsif($kind == $HcomPropaganda) {
	# Ͷ�׳�ư
	out("$name");
    } elsif(($kind == $HcomMoney) ||
	    ($kind == $HcomFood)) {
	# ���
	out("$target��$name$value");
    } elsif($kind == $HcomDestroy) {
	# ����
	if($arg != 0) {
	    out("$point��$name(ͽ��${value})");
	} else {
	    out("$point��$name");
	}
    } elsif(($kind == $HcomFarm) ||
	     ($kind == $HcomFactory) ||
	     ($kind == $HcomMountain)) {	
	# ����դ�
	if($arg == 0) {
	    out("$point��$name");
	} else {
	    out("$point��$name($arg��)");
	}
    } else {
	# ��ɸ�դ�
	out("$point��$name");
    }

    out("</FONT></NOBR></A><BR>");
}

# ������Ǽ���
sub tempLbbsHead {
    out(<<END);
<HR>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�Ѹ����̿�${H_tagBig}<BR>
</CENTER>
END
}

# ������Ǽ������ϥե�����
sub tempLbbsInput {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH>����</TH>
<TH>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
<TD><INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonSS$HcurrentID"></TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ������Ǽ������ϥե����� owner mode��
sub tempLbbsInputOW {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH COLSPAN=2>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>�ѥ����</TH>
<TH COLSPAN=2>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
�ֹ�
<SELECT NAME=NUMBER>
END
    # ȯ���ֹ�
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�������" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ������Ǽ�������
sub tempLbbsContents {
    my($lbbs, $line);
    $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>�ֹ�</TH>
<TH>��Ģ����</TH>
</TR>
END

    my($i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$line = $lbbs->[$i];
	if($line =~ /([0-9]*)\>(.*)\>(.*)$/) {
	    my($j) = $i + 1;
	    out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");
	    if($1 == 0) {
		# �Ѹ���
		out("<TD>$HtagLbbsSS_$2 > $3$H_tagLbbsSS</TD></TR>");
	    } else {
		# ���
		out("<TD>$HtagLbbsOW_$2 > $3$H_tagLbbsOW</TD></TR>");
	    }
	}
    }

    out(<<END);
</TD></TR></TABLE></CENTER>
END
}

# ������Ǽ��Ĥ�̾������å��������ʤ����
sub tempLbbsNoMessage {
    out(<<END);
${HtagBig_}̾���ޤ������Ƥ��󤬶���Ǥ���${H_tagBig}$HtempBack
END
}

# �񤭤��ߺ��
sub tempLbbsDelete {
    out(<<END);
${HtagBig_}��Ģ���Ƥ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempLbbsAdd {
    out(<<END);
${HtagBig_}��Ģ��Ԥ��ޤ���${H_tagBig}<HR>
END
}

# ���ޥ�ɺ��
sub tempCommandDelete {
    out(<<END);
${HtagBig_}���ޥ�ɤ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempCommandAdd {
    out(<<END);
${HtagBig_}���ޥ�ɤ���Ͽ���ޤ���${H_tagBig}<HR>
END
}

# �������ѹ�����
sub tempComment {
    out(<<END);
${HtagBig_}�����Ȥ򹹿����ޤ���${H_tagBig}<HR>
END
}

# �ᶷ
sub tempRecent {
    my($mode) = @_;
    out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�ζᶷ${H_tagBig}<BR>
END
    logPrintLocal($mode);
}

1;
