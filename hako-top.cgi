#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ȥåץ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# �ȥåץڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub topPageMain {
    # ����
    unlock();

    # �ƥ�ץ졼�Ƚ���
    tempTopPage();
}

# �ȥåץڡ���
sub tempTopPage {
    # �����ȥ�
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # �ǥХå��⡼�ɤʤ�֥������ʤ��ץܥ���
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�������ʤ��" NAME="TurnButton">
</FORM>
END
    }

    my($mStr1) = '';
    if($HhideMoneyMode != 0) {
	$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
    }

    # �ե�����
    out(<<END);
<H1>${HtagHeader_}������$HislandTurn${H_tagHeader}</H1>

<HR>
<H1>${HtagHeader_}��ʬ�����${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
���ʤ������̾���ϡ�<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>

�ѥ���ɤ�ɤ�������<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="��ȯ���˹Ԥ�" NAME="OwnerButton"><BR>
</FORM>

<HR>

<H1>${HtagHeader_}����ξ���${H_tagHeader}</H1>
<P>
���̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�η��쵬��${H_tagTH}</NOBR></TH>
</TR>
END

    my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	$id = $island->{'id'};
	$farm = $island->{'farm'};
	$factory = $island->{'factory'};
	$mountain = $island->{'mountain'};
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
	}

	$prize = $island->{'prize'};
	my($flags, $monsters, $turns);
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	$flags = $1;
	$monsters= $2;
	$turns = $3;
	$prize = '';

	# �������դ�ɽ��
	while($turns =~ s/([0-9]*),//) {
	    $prize .= "<IMG SRC=\"prize0.gif\" ALT=\"$1${Hprize[0]}\" WIDTH=16 HEIGHT=16> ";
	}

	# ̾���˾ޤ�ʸ�����ɲ�
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f *= 2;
	}

	# �ݤ������åꥹ��
	$f = 1;
	my($max) = -1;
	my($mNameList) = '';
	for($i = 0; $i < $HmonsterNumber; $i++) {
	    if($monsters & $f) {
		$mNameList .= "[$HmonsterName[$i]] ";
		$max = $i;
	    }
	    $f *= 2;
	}
	if($max != -1) {
	    $prize .= "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> ";
	}


	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
	    my($mTmp) = aboutMoney($island->{'money'});
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}

	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}">
$name
</A>
</NOBR><BR>
$prize
</TD>
<TD $HbgInfoCell align=right nowrap=nowrap>
<NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
$mStr1
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$farm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$factory</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mountain</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=7 align=left nowrap=nowrap><NOBR>${HtagTH_}�����ȡ�${H_tagTH}$island->{'comment'}</NOBR></TD>
</TR>
END
    }

    out(<<END);
</TABLE>

<HR>
<H1>${HtagHeader_}���������õ��${H_tagHeader}</H1>
END

    if($HislandNumber < $HmaxIsland) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
�ɤ��̾����Ĥ���ͽ�ꡩ<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="õ���˹Ԥ�" NAME="NewIslandButton">
</FORM>
END
    } else {
	out(<<END);
        ��ο���������Ǥ�������������Ͽ�Ǥ��ޤ���
END
    }

    out(<<END);
<HR>
<H1>${HtagHeader_}���̾���ȥѥ���ɤ��ѹ�${H_tagHeader}</H1>
<P>
(���)̾�����ѹ��ˤ�$HcostChangeName${HunitMoney}������ޤ���
</P>
<FORM action="$HthisFile" method="POST">
�ɤ���Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�ɤ��̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�(ɬ��)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�������ѥ���ɤϡ�(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeInfoButton">
</FORM>

<HR>

<H1>${HtagHeader_}�Ƕ�ν����${H_tagHeader}</H1>
END
    logPrintTop();
    out(<<END);
<H1>${HtagHeader_}ȯ���ε�Ͽ${H_tagHeader}</H1>
END
    historyPrint();
}

# �ȥåץڡ����ѥ�ɽ��
sub logPrintTop {
    my($i);
    for($i = 0; $i < $HtopLogTurn; $i++) {
	logFilePrint($i, 0, 0);
    }
}

# ��Ͽ�ե�����ɽ��
sub historyPrint {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l);
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
    }
    @line = reverse(@line);

    foreach $l (@line) {
	$l =~ /^([0-9]*),(.*)$/;
	out("<NOBR>${HtagNumber_}������${1}${H_tagNumber}��${2}</NOBR><BR>\n");
    }
    close(HIN);
}

1;
