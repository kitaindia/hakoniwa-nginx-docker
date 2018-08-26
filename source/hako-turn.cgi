#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������ʹԥ⥸�塼��(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------


#����2�إå����κ�ɸ
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

#----------------------------------------------------------------------
# ��ο��������⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub newIslandMain {
    # �礬���äѤ��Ǥʤ��������å�
    if($HislandNumber >= $HmaxIsland) {
	unlock();
	tempNewIslandFull();
	return;
    }

    # ̾�������뤫�����å�
    if($HcurrentName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # ̾���������������å�
    if($HcurrentName =~ /[,\?\(\)\<\>\$]|^̵��$/) {
	# �Ȥ��ʤ�̾��
	unlock();
	tempNewIslandBadName();
	return;
    }

    # ̾���ν�ʣ�����å�
    if(nameToNumber($HcurrentName) != -1) {
	# ���Ǥ�ȯ������
	unlock();
	tempNewIslandAlready();
	return;
    }

    # password��¸��Ƚ��
    if($HinputPassword eq '') {
	# password̵��
	unlock();
	tempNewIslandNoPassword();
	return;
    }

    # ��ǧ�ѥѥ����
    if($HinputPassword2 ne $HinputPassword) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ����������ֹ�����
    $HcurrentNumber = $HislandNumber;
    $HislandNumber++;
    $Hislands[$HcurrentNumber] = makeNewIsland();
    my($island) = $Hislands[$HcurrentNumber];

    # �Ƽ���ͤ�����
    $island->{'name'} = $HcurrentName;
    $island->{'id'} = $HislandNextID;
    $HislandNextID ++;
    $island->{'absent'} = $HgiveupTurn - 3;
    $island->{'comment'} = '(̤��Ͽ)';
    $island->{'password'} = encode($HinputPassword);
    
    # �͸�����¾����
    estimate($HcurrentNumber);

    # �ǡ����񤭽Ф�
    writeIslandsFile($island->{'id'});
    logDiscover($HcurrentName); # ��

    # ����
    unlock();

    # ȯ������
    tempNewIslandHead($HcurrentName); # ȯ�����ޤ���!!
    islandInfo(); # ��ξ���
    islandMap(1); # ����Ͽޡ�owner�⡼��
}

# ����������������
sub makeNewIsland {
    # �Ϸ�����
    my($land, $landValue) = makeNewLand();

    # ������ޥ�ɤ�����
    my(@command, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	 $command[$i] = {
	     'kind' => $HcomDoNothing,
	     'target' => 0,
	     'x' => 0,
	     'y' => 0,
	     'arg' => 0
	 };
    }

    # ����Ǽ��Ĥ����
    my(@lbbs);
    for($i = 0; $i < $HlbbsMax; $i++) {
	 $lbbs[$i] = "0>>";
    }

    # ��ˤ����֤�
    return {
	'land' => $land,
	'landValue' => $landValue,
	'command' => \@command,
	'lbbs' => \@lbbs,
	'money' => $HinitialMoney,
	'food' => $HinitialFood,
	'prize' => '0,0,',
    };
}

# ����������Ϸ����������
sub makeNewLand {
    # ���ܷ������
    my(@land, @landValue, $x, $y, $i);

    # ���˽����
    for($y = 0; $y < $HislandSize; $y++) {
	 for($x = 0; $x < $HislandSize; $x++) {
	     $land[$x][$y] = $HlandSea;
	     $landValue[$x][$y] = 0;
	 }
    }

    # �����4*4�˹��Ϥ�����
    my($center) = $HislandSize / 2 - 1;
    for($y = $center - 1; $y < $center + 3; $y++) {
	 for($x = $center - 1; $x < $center + 3; $x++) {
	     $land[$x][$y] = $HlandWaste;
	 }
    }

    # 8*8�ϰ����Φ�Ϥ�����
    for($i = 0; $i < 120; $i++) {
	 # �������ɸ
	 $x = random(8) + $center - 3;
	 $y = random(8) + $center - 3;

	 my($tmp) = countAround(\@land, $x, $y, $HlandSea, 7);
	 if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
	     # �����Φ�Ϥ������硢�����ˤ���
	     # �����Ϲ��Ϥˤ���
	     # ���Ϥ�ʿ�Ϥˤ���
	     if($land[$x][$y] == $HlandWaste) {
		 $land[$x][$y] = $HlandPlains;
		 $landValue[$x][$y] = 0;
	     } else {
		 if($landValue[$x][$y] == 1) {
                     $land[$x][$y] = $HlandWaste;
                     $landValue[$x][$y] = 0;
		 } else {
		     $landValue[$x][$y] = 1;
		 }
	     }
	 }
    }

    # ������
    my($count) = 0;
    while($count < 4) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ���������Ǥ˿��Ǥʤ���С�������
	 if($land[$x][$y] != $HlandForest) {
	     $land[$x][$y] = $HlandForest;
	     $landValue[$x][$y] = 5; # �ǽ��500��
	     $count++;
	 }
    }

    # Į����
    $count = 0;
    while($count < 2) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ����������Į�Ǥʤ���С�Į����
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandTown;
	     $landValue[$x][$y] = 5; # �ǽ��500��
	     $count++;
	 }
    }

    # ������
    $count = 0;
    while($count < 1) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ����������Į�Ǥʤ���С�Į����
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandMountain;
	     $landValue[$x][$y] = 0; # �ǽ�Ϻη���ʤ�
	     $count++;
	 }
    }

    # ���Ϥ���
    $count = 0;
    while($count < 1) {
	 # �������ɸ
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ����������Į�����Ǥʤ���С�����
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandBase;
	     $landValue[$x][$y] = 0;
	     $count++;
	 }
    }

    return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeMain {
    # id����������
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($flag) = 0;

    # �ѥ���ɥ����å�
    if($HoldPassword eq $HspecialPassword) {
	# �ü�ѥ����
	$island->{'money'} = 9999;
	$island->{'food'} = 9999;
    } elsif(!checkPassword($island->{'password'},$HoldPassword)) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ��ǧ�ѥѥ����
    if($HinputPassword2 ne $HinputPassword) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    if($HcurrentName ne '') {
	# ̾���ѹ��ξ��	
	# ̾���������������å�
	if($HcurrentName =~ /[,\?\(\)\<\>]|^̵��$/) {
	    # �Ȥ��ʤ�̾��
	    unlock();
	    tempNewIslandBadName();
	    return;
	}

	# ̾���ν�ʣ�����å�
	if(nameToNumber($HcurrentName) != -1) {
	    # ���Ǥ�ȯ������
	    unlock();
	    tempNewIslandAlready();
	    return;
	}

	if($island->{'money'} < $HcostChangeName) {
	    # �⤬­��ʤ�
	    unlock();
	    tempChangeNoMoney();
	    return;
	}

	# ���
	if($HoldPassword ne $HspecialPassword) {
	    $island->{'money'} -= $HcostChangeName;
	}

	# ̾�����ѹ�
	logChangeName($island->{'name'}, $HcurrentName);
	$island->{'name'} = $HcurrentName;
	$flag = 1;
    }

    # password�ѹ��ξ��
    if($HinputPassword ne '') {
	# �ѥ���ɤ��ѹ�
	$island->{'password'} = encode($HinputPassword);
	$flag = 1;
    }

    if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
	# �ɤ�����ѹ�����Ƥ��ʤ�
	unlock();
	tempChangeNothing();
	return;
    }

    # �ǡ����񤭽Ф�
    writeIslandsFile($HcurrentID);
    unlock();

    # �ѹ�����
    tempChange();
}

#----------------------------------------------------------------------
# ������ʹԥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub turnMain {
    # �ǽ��������֤򹹿�
    $HislandLastTime += $HunitTime;

    # ���ե��������ˤ��餹
    my($i, $j, $s, $d);
    for($i = ($HlogMax - 1); $i >= 0; $i--) {
	$j = $i + 1;
	my($s) = "${HdirName}/hakojima.log$i";
	my($d) = "${HdirName}/hakojima.log$j";
	unlink($d);
	rename($s, $d);
    }

    # ��ɸ�������
    makeRandomPointArray();

    # �������ֹ�
    $HislandTurn++;

    # ���ַ��
    my(@order) = randomArray($HislandNumber);

    # ����������ե�����
    for($i = 0; $i < $HislandNumber; $i++) {
	estimate($order[$i]);
	income($Hislands[$order[$i]]);

	# �����󳫻����ο͸������
	$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
    }

    # ���ޥ�ɽ���
    for($i = 0; $i < $HislandNumber; $i++) {
	# �����1�ˤʤ�ޤǷ����֤�
	while(doCommand($Hislands[$order[$i]]) == 0){};
    }

    # ��Ĺ�����ñ�إå����ҳ�
    for($i = 0; $i < $HislandNumber; $i++) {
	doEachHex($Hislands[$order[$i]]);
    }

    # �����ν���
    my($remainNumber) = $HislandNumber;
    my($island);
    for($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$order[$i]];
	doIslandProcess($order[$i], $island); 

	# ����Ƚ��
	if($island->{'dead'} == 1) {
	    $island->{'pop'} = 0;
	    $remainNumber--;
	} elsif($island->{'pop'} == 0) {
	    $island->{'dead'} = 1;
	    $remainNumber--;
	    # ���ǥ�å�����
	    my($tmpid) = $island->{'id'};
	    logDead($tmpid, $island->{'name'});
	    unlink("island.$tmpid");
	}
    }

    # �͸���˥�����
    islandSort();

	

    # ���������оݥ�������ä��顢���ν���
    if(($HislandTurn % $HturnPrizeUnit) == 0) {
	my($island) = $Hislands[0];
	logPrize($island->{'id'}, $island->{'name'}, "$HislandTurn${Hprize[0]}");
	$island->{'prize'} .= "${HislandTurn},";
    }

    # ������å�
    $HislandNumber = $remainNumber;

    # �Хå����åץ�����Ǥ���С�������rename
    if(($HislandTurn % $HbackupTurn) == 0) {
	my($i);
	my($tmp) = $HbackupTimes - 1;
	myrmtree("${HdirName}.bak$tmp");
	for($i = ($HbackupTimes - 1); $i > 0; $i--) {
	    my($j) = $i - 1;
	    rename("${HdirName}.bak$j", "${HdirName}.bak$i");
	}
	rename("${HdirName}", "${HdirName}.bak0");
	mkdir("${HdirName}", $HdirMode);

	# ���ե���������᤹
	for($i = 0; $i <= $HlogMax; $i++) {
	    rename("${HdirName}.bak0/hakojima.log$i",
		   "${HdirName}/hakojima.log$i");
	}
	rename("${HdirName}.bak0/hakojima.his",
	       "${HdirName}/hakojima.his");
    }

    # �ե�����˽񤭽Ф�
    writeIslandsFile(-1);

    # ���񤭽Ф�
    logFlush();

    # ��Ͽ��Ĵ��
    logHistoryTrim();

    # �ȥåפ�
    topPageMain();
}

# �ǥ��쥯�ȥ�ä�
sub myrmtree {
    my($dn) = @_;
    opendir(DIN, "$dn/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	unlink("$dn/$fileName");
    } 
    closedir(DIN);
    rmdir($dn);
}

# ����������ե�����
sub income {
    my($island) = @_;
    my($pop, $farm, $factory, $mountain) = 
	(      
	 $island->{'pop'},
	 $island->{'farm'} * 10,
	 $island->{'factory'},
	 $island->{'mountain'}
	 );

    # ����
    if($pop > $farm) {
	# ���Ȥ�������꤬;����
	$island->{'food'} += $farm; # ����ե��Ư
	$island->{'money'} +=
	    min(int(($pop - $farm) / 10),
		 $factory + $mountain);
    } else {
	# ���Ȥ����Ǽ���դξ��
	$island->{'food'} += $pop; # �������ɻŻ�
    }

    # ��������
    $island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
}


# ���ޥ�ɥե�����
sub doCommand {
    my($island) = @_;

    # ���ޥ�ɼ��Ф�
    my($comArray, $command);
    $comArray = $island->{'command'};
    $command = $comArray->[0]; # �ǽ�Τ���Ф�
    slideFront($comArray, 0); # �ʹߤ�ͤ��

    # �����Ǥμ��Ф�
    my($kind, $target, $x, $y, $arg) = 
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($landKind) = $land->[$x][$y];
    my($lv) = $landValue->[$x][$y];
    my($cost) = $HcomCost[$kind];
    my($comName) = $HcomName[$kind];
    my($point) = "($x, $y)";
    my($landName) = landName($landKind, $lv);

    if($kind == $HcomDoNothing) {
	# ��ⷫ��
	logDoNothing($id, $name, $comName);
	$island->{'money'} += 10;
	$island->{'absent'} ++;
	
	# ��ư����
	if($island->{'absent'} >= $HgiveupTurn) {
	    $comArray->[0] = {
		'kind' => $HcomGiveup,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
	    }
	}
	return 1;
    }

    $island->{'absent'} = 0;

    # �����ȥ����å�
    if($cost > 0) {
	# ��ξ��
	if($island->{'money'} < $cost) {
	    logNoMoney($id, $name, $comName);
	    return 0;
	}
    } elsif($cost < 0) {
	# �����ξ��
	if($island->{'food'} < (-$cost)) {
	    logNoFood($id, $name, $comName);
	    return 0;
	}
    }

    # ���ޥ�ɤ�ʬ��
    if(($kind == $HcomPrepare) ||
       ($kind == $HcomPrepare2)) {
	# ���ϡ��Ϥʤ餷
	if(($landKind == $HlandSea) || 
	   ($landKind == $HlandSbase) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandMountain) ||
	   ($landKind == $HlandMonster)) {
	    # ����������ϡ����ġ��������ä����ϤǤ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ��Ū�ξ���ʿ�Ϥˤ���
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, '����', $point);

	# ��򺹤�����
	$island->{'money'} -= $cost;

	if($kind == $HcomPrepare2) {
	    # �Ϥʤ餷
	    $island->{'prepare2'}++;
	    
	    # ��������񤻤�
	    return 0;
	} else {
	    # ���Ϥʤ顢��¢��β�ǽ������
	    if(random(1000) < $HdisMaizo) {
		my($v) = 100 + random(901);
		$island->{'money'} += $v;
		logMaizo($id, $name, $comName, $v);
	    }
	    return 1;
	}
    } elsif($kind == $HcomReclaim) {
	# ���Ω��
	if(($landKind != $HlandSea) &&
	   ($landKind != $HlandOil) &&
	   ($landKind != $HlandSbase)) {
	    # ����������ϡ����Ĥ������Ω�ƤǤ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# �����Φ�����뤫�����å�
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 7) +
	    countAround($land, $x, $y, $HlandOil, 7) +
            countAround($land, $x, $y, $HlandSbase, 7);

        if($seaCount == 7) {
	    # ���������������Ω����ǽ
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 1)) {
	    # �����ξ��
	    # ��Ū�ξ�����Ϥˤ���
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# ����γ���3�إå�������ʤΤǡ������ˤ���
		my($i, $sx, $sy);

		for($i = 1; $i < 7; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];

		    # �Ԥˤ�����Ĵ��
		    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			$sx--;
		    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		    } else {
			# �ϰ���ξ��
			if($land->[$sx][$sy] == $HlandSea) {
			    $landValue->[$sx][$sy] = 1;
			}
		    }
		}
	    }
	} else {
	    # ���ʤ顢��Ū�ξ��������ˤ���
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, $comName, $point);
	}
	
	# ��򺹤�����
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomDestroy) {
	# ����
	if(($landKind == $HlandSbase) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandMonster)) {
	    # ������ϡ����ġ����äϷ���Ǥ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 0)) {
	    # ���ʤ顢����õ��
	    # ���۷���
	    if($arg == 0) { $arg = 1; }
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost);
	    $island->{'money'} -= $value;

	    # ���Ĥ��뤫Ƚ��
	    if($p > random(100)) {
		# ���ĸ��Ĥ���
		logOilFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOil;
		$landValue->[$x][$y] = 0;
	    } else {
		# ̵�̷���˽����
		logOilFail($id, $name, $point, $comName, $str);
	    }
	    return 1;
	}

	# ��Ū�ξ��򳤤ˤ��롣���ʤ���Ϥˡ������ʤ鳤�ˡ�
	if($landKind == $HlandMountain) {
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	} elsif($landKind == $HlandSea) {
	    $landValue->[$x][$y] = 0;
	} else {
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    $island->{'area'}--;
	}
	logLandSuc($id, $name, $comName, $point);

	# ��򺹤�����
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomSellTree) {
	# Ȳ��
	if($landKind != $HlandForest) {
	    # ���ʳ���Ȳ�ΤǤ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ��Ū�ξ���ʿ�Ϥˤ���
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, $comName, $point);

	# ��Ѷ������
	$island->{'money'} += $HtreeValue * $lv;
	return 1;
    } elsif(($kind == $HcomPlant) ||
	    ($kind == $HcomFarm) ||
	    ($kind == $HcomFactory) ||
	    ($kind == $HcomBase) ||
	    ($kind == $HcomMonument) ||
	    ($kind == $HcomHaribote) ||
	    ($kind == $HcomDbase)) {

	# �Ͼ���߷�
	if(!
	   (($landKind == $HlandPlains) ||
	    ($landKind == $HlandTown) ||
	    (($landKind == $HlandMonument) && ($kind == $HcomMonument)) ||
	    (($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
	    (($landKind == $HlandFactory) && ($kind == $HcomFactory)) ||
	    (($landKind == $HlandDefence) && ($kind == $HcomDbase)))) {
	    # ��Ŭ�����Ϸ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# �����ʬ��
	if($kind == $HcomPlant) {
	    # ��Ū�ξ��򿹤ˤ��롣
	    $land->[$x][$y] = $HlandForest;
	    $landValue->[$x][$y] = 1; # �ڤϺ���ñ��
	    logPBSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomBase) {
	    # ��Ū�ξ���ߥ�������Ϥˤ��롣
	    $land->[$x][$y] = $HlandBase;
	    $landValue->[$x][$y] = 0; # �и���0
	    logPBSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomHaribote) {
	    # ��Ū�ξ���ϥ�ܥƤˤ���
	    $land->[$x][$y] = $HlandHaribote;
	    $landValue->[$x][$y] = 0;
	    logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
	} elsif($kind == $HcomFarm) {
	    # ����
	    if($landKind == $HlandFarm) {
		# ���Ǥ�����ξ��
		$landValue->[$x][$y] += 2; # ���� + 2000��
		if($landValue->[$x][$y] > 50) {
		    $landValue->[$x][$y] = 50; # ���� 50000��
		}
	    } else {
		# ��Ū�ξ��������
		$land->[$x][$y] = $HlandFarm;
		$landValue->[$x][$y] = 10; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomFactory) {
	    # ����
	    if($landKind == $HlandFactory) {
		# ���Ǥ˹���ξ��
		$landValue->[$x][$y] += 10; # ���� + 10000��
		if($landValue->[$x][$y] > 100) {
		    $landValue->[$x][$y] = 100; # ���� 100000��
		}
	    } else {
		# ��Ū�ξ��򹩾��
		$land->[$x][$y] = $HlandFactory;
		$landValue->[$x][$y] = 30; # ���� = 10000��
	    }
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomDbase) {
	    # �ɱһ���
	    if($landKind == $HlandDefence) {
		# ���Ǥ��ɱһ��ߤξ��
		$landValue->[$x][$y] = 1; # �������֥��å�
		logBombSet($id, $name, $landName, $point);
	    } else {
		# ��Ū�ξ����ɱһ��ߤ�
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomMonument) {
	    # ��ǰ��
	    if($landKind == $HlandMonument) {
		# ���Ǥ˵�ǰ��ξ��
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
		    # �������åȤ����Ǥˤʤ�
		    # ������鷺�����
		    return 0;
		}
		my($tIsland) = $Hislands[$tn];
		$tIsland->{'bigmissile'}++;

		# ���ξ��Ϲ��Ϥ�
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		logMonFly($id, $name, $landName, $point);
	    } else {
		# ��Ū�ξ���ǰ���
		$land->[$x][$y] = $HlandMonument;
		if($arg >= $HmonumentNumber) {
		    $arg = 0;
		}
		$landValue->[$x][$y] = $arg;
		logLandSuc($id, $name, $comName, $point);
	    }
	}

	# ��򺹤�����
	$island->{'money'} -= $cost;

	# ����դ��ʤ顢���ޥ�ɤ��᤹
	if(($kind == $HcomFarm) ||
	   ($kind == $HcomFactory)) {
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
	}

	return 1;
    } elsif($kind == $HcomMountain) {
	# �η���
	if($landKind != $HlandMountain) {
	    # ���ʳ��ˤϺ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$landValue->[$x][$y] += 5; # ���� + 5000��
	if($landValue->[$x][$y] > 200) {
	    $landValue->[$x][$y] = 200; # ���� 200000��
	}
	logLandSuc($id, $name, $comName, $point);

	# ��򺹤�����
	$island->{'money'} -= $cost;
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;
    } elsif($kind == $HcomSbase) {
	# �������
	if(($landKind != $HlandSea) || ($lv != 0)){
	    # ���ʳ��ˤϺ��ʤ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSbase;
	$landValue->[$x][$y] = 0; # �и���0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# ��򺹤�����
	$island->{'money'} -= $cost;
	return 1;
    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileLD)) {
	# �ߥ������
	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # �������åȤ����Ǥˤʤ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	my($flag) = 0;
	if($arg == 0) {
	    # 0�ξ��Ϸ�Ƥ����
	    $arg = 10000;
	}

	# ��������
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	# ��̱�ο�
	my($boat) = 0;

	# ��
	if($kind == $HcomMissilePP) {
	    $err = 7;
	} else {
	    $err = 19;
	}

	# �⤬�Ԥ��뤫�������­��뤫������������Ĥޤǥ롼��
	my($bx, $by, $count) = (0,0,0);
	while(($arg > 0) &&
	      ($island->{'money'} >= $cost)) {
	    # ���Ϥ򸫤Ĥ���ޤǥ롼��
	    while($count < $HpointNumber) {
		$bx = $Hrpx[$count];
		$by = $Hrpy[$count];
		if(($land->[$bx][$by] == $HlandBase) ||
		   ($land->[$bx][$by] == $HlandSbase)) {
		    last;
		}
		$count++;
	    }
	    if($count >= $HpointNumber) {
		# ���Ĥ���ʤ��ä��餽���ޤ�
		last;
	    }
	    # �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
	    $flag = 1;	   

	    # ���ϤΥ�٥�򻻽�
	    my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
	    # ������ǥ롼��
	    while(($level > 0) &&
		  ($arg > 0) &&
		  ($island->{'money'} > $cost)) {
		# ��ä��Τ�����ʤΤǡ����ͤ���פ�����
		$level--;
		$arg--;
		$island->{'money'} -= $cost;

		# ����������
		my($r) = random($err);
		$tx = $x + $ax[$r];
		$ty = $y + $ay[$r];
		if((($ty % 2) == 0) && (($y % 2) == 1)) {
		    $tx--;
		}

		# �������ϰ��⳰�����å�
		if(($tx < 0) || ($tx >= $HislandSize) ||
		   ($ty < 0) || ($ty >= $HislandSize)) {
		    # �ϰϳ�
		    if($kind == $HcomMissileST) {
			# ���ƥ륹
			logMsOutS($id, $target, $name, $tName,
				   $comName, $point);
		    } else {
			# �̾��
			logMsOut($id, $target, $name, $tName,
				  $comName, $point);
		    }
		    next;
		}

		# ���������Ϸ�������
		my($tL) = $tLand->[$tx][$ty];
		my($tLv) = $tLandValue->[$tx][$ty];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($tx, $ty)";

		# �ɱһ���Ƚ��
		my($defence) = 0;
		if($HdefenceHex[$id][$tx][$ty] == 1) {
		    $defence = 1;
		} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
		    $defence = 0;
		} else {
		    if($tL == $HlandDefence) {
			# �ɱһ��ߤ�̿��
			# �ե饰�򥯥ꥢ
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 19; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];

			    # �Ԥˤ�����Ĵ��
			    if((($sy % 2) == 0) && (($ty % 2) == 1)) {
				$sx--;
			    }

			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# �ϰϳ��ξ�粿�⤷�ʤ�
			    } else {
				# �ϰ���ξ��
				$HdefenceHex[$id][$sx][$sy] = 0;
			    }
			}
		    } elsif(countAround($tLand, $tx, $ty, $HlandDefence, 19)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } else {
			$HdefenceHex[$id][$tx][$ty] = -1;
			$defence = 0;
		    }
		}
		
		if($defence == 1) {
		    # ��������
		    if($kind == $HcomMissileST) {
			# ���ƥ륹
			logMsCaughtS($id, $target, $name, $tName,
				      $comName, $point, $tPoint);
		    } else {
			# �̾��
			logMsCaught($id, $target, $name, $tName,
				     $comName, $point, $tPoint);
		    }
		    next;
		}

		# �ָ��̤ʤ���hex��ǽ��Ƚ��
		if((($tL == $HlandSea) && ($tLv == 0))|| # ������
		   ((($tL == $HlandSea) ||   # ���ޤ��ϡ�����
		     ($tL == $HlandSbase) ||   # ������Ϥޤ��ϡ�����
		     ($tL == $HlandMountain)) # ���ǡ�����
		    && ($kind != $HcomMissileLD))) { # Φ���ưʳ�
		    # ������Ϥξ�硢���Υե�
		    if($tL == $HlandSbase) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

		    # ̵����
		    if($kind == $HcomMissileST) {
			# ���ƥ륹
			logMsNoDamageS($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } else {
			# �̾��
			logMsNoDamage($id, $target, $name, $tName,
				       $comName, $tLname, $point, $tPoint);
		    }
		    next;
		}

		# �Ƥμ����ʬ��
		if($kind == $HcomMissileLD) {
		    # Φ���˲���
		    if($tL == $HlandMountain) {
			# ��(���Ϥˤʤ�)
			logMsLDMountain($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			# ���Ϥˤʤ�
			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
			next;

		    } elsif($tL == $HlandSbase) {
			# �������
			logMsLDSbase($id, $target, $name, $tName,
				      $comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandMonster) {
			# ����
			logMsLDMonster($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandSea) {
			# ����
			logMsLDSea1($id, $target, $name, $tName,
				    $comName, $tLname, $point, $tPoint);
		    } else {
			# ����¾
			logMsLDLand($id, $target, $name, $tName,
				     $comName, $tLname, $point, $tPoint);
		    }
		    
		    # �и���
		    if($tL == $HlandTown) {
			if(($land->[$bx][$by] == $HlandBase) ||
			   ($land->[$bx][$by] == $HlandSbase)) {
			    # �ޤ����Ϥξ��Τ�
			    $landValue->[$bx][$by] += int($tLv / 20);
			    if($landValue->[$bx][$by] > $HmaxExpPoint) {
				$landValue->[$bx][$by] = $HmaxExpPoint;
			    }
			}
		    }

		    # �����ˤʤ�
		    $tLand->[$tx][$ty] = $HlandSea;
		    $tIsland->{'area'}--;
		    $tLandValue->[$tx][$ty] = 1;

		    # �Ǥ����ġ�������������Ϥ��ä��鳤
		    if(($tL == $HlandOil) ||
			($tL == $HlandSea) ||
		       ($tL == $HlandSbase)) {
			$tLandValue->[$tx][$ty] = 0;
		    }
		} else {
		    # ����¾�ߥ�����
		    if($tL == $HlandWaste) {
			# ����(�ﳲ�ʤ�)
			if($kind == $HcomMissileST) {
			    # ���ƥ륹
			    logMsWasteS($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			} else {
			    # �̾�
			    logMsWaste($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
			}
		    } elsif($tL == $HlandMonster) {
			# ����
			my($mKind, $mName, $mHp) = monsterSpec($tLv);
			my($special) = $HmonsterSpecial[$mKind];

			# �Ų���?
			if((($special == 3) && (($HislandTurn % 2) == 1)) ||
			   (($special == 4) && (($HislandTurn % 2) == 0))) {
			    # �Ų���
			    if($kind == $HcomMissileST) {
				# ���ƥ륹
				logMsMonNoDamageS($id, $target, $name, $tName,
					     $comName, $mName, $point,
					     $tPoint);
			    } else {
				# �̾���
				logMsMonNoDamage($id, $target, $name, $tName,
					     $comName, $mName, $point,
					     $tPoint);
			    }
			    next;
			} else {
			    # �Ų��椸��ʤ�
			    if($mHp == 1) {
				# ���ä��Ȥ᤿
				if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
				    # �и���
				    $landValue->[$bx][$by] += $HmonsterExp[$mKind];
				    if($landValue->[$bx][$by] > $HmaxExpPoint) {
					$landValue->[$bx][$by] = $HmaxExpPoint;
				    }
				}

				if($kind == $HcomMissileST) {
				    # ���ƥ륹
				    logMsMonKillS($id, $target, $name, $tName,
						  $comName, $mName, $point,
						  $tPoint);
				} else {
				    # �̾�
				    logMsMonKill($id, $target, $name, $tName,
						 $comName, $mName, $point,
						 $tPoint);
				}

				# ����
				my($value) = $HmonsterValue[$mKind];
				if($value > 0) {
				    $tIsland->{'money'} += $value;
				    logMsMonMoney($target, $mName, $value);
				}

				# �޴ط�
				my($prize) = $island->{'prize'};
				$prize =~ /([0-9]*),([0-9]*),(.*)/;
				my($flags) = $1;
				my($monsters) = $2;
				my($turns) = $3;
				my($v) = 2 ** $mKind;
				$monsters |= $v;
				$island->{'prize'} = "$flags,$monsters,$turns";
			    } else {
				# ���������Ƥ�
				if($kind == $HcomMissileST) {
				    # ���ƥ륹
				    logMsMonsterS($id, $target, $name, $tName,
						  $comName, $mName, $point,
						  $tPoint);
				} else {
				    # �̾�
				    logMsMonster($id, $target, $name, $tName,
						 $comName, $mName, $point,
						 $tPoint);
				}
				# HP��1����
				$tLandValue->[$tx][$ty]--;
				next;
			    }

			}
		    } else {
			# �̾��Ϸ�
			if($kind == $HcomMissileST) {
			    # ���ƥ륹
			    logMsNormalS($id, $target, $name, $tName,
					   $comName, $tLname, $point,
					   $tPoint);
			} else {
			    # �̾�
			    logMsNormal($id, $target, $name, $tName,
					 $comName, $tLname, $point,
					 $tPoint);
			}
		    }
		    # �и���
		    if($tL == $HlandTown) {
			if(($land->[$bx][$by] == $HlandBase) ||
			    ($land->[$bx][$by] == $HlandSbase)) {
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $boat += $tLv; # �̾�ߥ�����ʤΤ���̱�˥ץ饹
			    if($landValue->[$bx][$by] > $HmaxExpPoint) {
				$landValue->[$bx][$by] = $HmaxExpPoint;
			    }
			}
		    }
		    
                    # ���Ϥˤʤ�
		    $tLand->[$tx][$ty] = $HlandWaste;
		    $tLandValue->[$tx][$ty] = 1; # ������

		    # �Ǥ����Ĥ��ä��鳤
		    if($tL == $HlandOil) {
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
		    }
		} 
	    }

	    # ����������䤷�Ȥ�
	    $count++;
	}


	if($flag == 0) {
	    # ���Ϥ���Ĥ�̵���ä����
	    logMsNoBase($id, $name, $comName);
	    return 0;
	}

	# ��̱Ƚ��
	$boat = int($boat / 2);
	if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
	    # ��̱ɺ��
	    my($achive); # ��ã��̱
	    my($i);
	    for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {
		    # Į�ξ��
		    my($lv) = $landValue->[$bx][$by];
		    if($boat > 50) {
			$lv += 50;
			$boat -= 50;
			$achive += 50;
		    } else {
			$lv += $boat;
			$achive += $boat;
			$boat = 0;
		    }
		    if($lv > 200) {
			$boat += ($lv - 200);
			$achive -= ($lv - 200);
			$lv = 200;
		    }
		    $landValue->[$bx][$by] = $lv;
		} elsif($land->[$bx][$by] == $HlandPlains) {
		    # ʿ�Ϥξ��
		    $land->[$bx][$by] = $HlandTown;;
		    if($boat > 10) {
			$landValue->[$bx][$by] = 5;
			$boat -= 10;
			$achive += 10;
		    } elsif($boat > 5) {
			$landValue->[$bx][$by] = $boat - 5;
			$achive += $boat;
			$boat = 0;
		    }
		}
		if($boat <= 0) {
		    last;
		}
	    }
	    if($achive > 0) {
		# �����Ǥ����夷����硢�����Ǥ�
		logMsBoatPeople($id, $name, $achive);

		# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
		if($achive >= 200) {
		    my($prize) = $island->{'prize'};
		    $prize =~ /([0-9]*),([0-9]*),(.*)/;
		    my($flags) = $1;
		    my($monsters) = $2;
		    my($turns) = $3;

		    if((!($flags & 8)) &&  $achive >= 200){
			$flags |= 8;
			logPrize($id, $name, $Hprize[4]);
		    } elsif((!($flags & 16)) &&  $achive > 500){
			$flags |= 16;
			logPrize($id, $name, $Hprize[5]);
		    } elsif((!($flags & 32)) &&  $achive > 800){
			$flags |= 32;
			logPrize($id, $name, $Hprize[6]);
		    }
		    $island->{'prize'} = "$flags,$monsters,$turns";
		}
	    }
	}
	return 1;
    } elsif($kind == $HcomSendMonster) {
	# �����ɸ�
	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	if($tn eq '') {
	    # �������åȤ����Ǥˤʤ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	# ��å�����
	logMonsSend($id, $target, $name, $tName);
	$tIsland->{'monstersend'}++;

	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomSell) {
	# ͢���̷���
	if($arg == 0) { $arg = 1; }
	my($value) = min($arg * (-$cost), $island->{'food'});

	# ͢�Х�
	logSell($id, $name, $comName, $value);
	$island->{'food'} -=  $value;
	$island->{'money'} += ($value / 10);
	return 0;
    } elsif(($kind == $HcomFood) ||
	    ($kind == $HcomMoney)) {
	# �����
	# �������åȼ���
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	# ����̷���
	if($arg == 0) { $arg = 1; }
	my($value, $str);
	if($cost < 0) {
	    $value = min($arg * (-$cost), $island->{'food'});
	    $str = "$value$HunitFood";
	} else {
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	}

	# �����
	logAid($id, $target, $name, $tName, $comName, $str);

	if($cost < 0) {
	    $island->{'food'} -= $value;
	    $tIsland->{'food'} += $value;
	} else {
	    $island->{'money'} -= $value;
	    $tIsland->{'money'} += $value;
	}
	return 0;
    } elsif($kind == $HcomPropaganda) {
	# Ͷ�׳�ư
	logPropaganda($id, $name, $comName);
	$island->{'propaganda'} = 1;
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomGiveup) {
	# ����
	logGiveup($id, $name);
	$island->{'dead'} = 1;
	unlink("island.$id");
	return 1;
    }

    return 1;
}


# ��Ĺ�����ñ�إå����ҳ�
sub doEachHex {
    my($island) = @_;
    my(@monsterMove);

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # ������͸��Υ�����
    my($addpop)  = 10;  # ¼��Į
    my($addpop2) = 0; # �Ի�
    if($island->{'food'} < 0) {
	# ������­
	$addpop = -30;
    } elsif($island->{'propaganda'} == 1) {
	# Ͷ�׳�ư��
	$addpop = 30;
	$addpop2 = 3;
    }

    # �롼��
    my($x, $y, $i);
    for($i = 0; $i < $HpointNumber; $i++) {
	$x = $Hrpx[$i];
	$y = $Hrpy[$i];
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];

	if($landKind == $HlandTown) {
	    # Į��
	    if($addpop < 0) {
		# ��­
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ʿ�Ϥ��᤹
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ��Ĺ
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    if($lv > 100) {
			$lv = 100;
		    }
		} else {
		    # �ԻԤˤʤ����Ĺ�٤�
		    if($addpop2 > 0) {
			$lv += random($addpop2) + 1;
		    }
		}
	    }
	    if($lv > 200) {
		$lv = 200;
	    }
	    $landValue->[$x][$y] = $lv;
	} elsif($landKind == $HlandPlains) {
	    # ʿ��
	    if(random(5) == 0) {
		# ��������졢Į������С�������Į�ˤʤ�
	        if(countGrow($land, $landValue, $x, $y)){
		    $land->[$x][$y] = $HlandTown;
		    $landValue->[$x][$y] = 1;
		}
	    }
	} elsif($landKind == $HlandForest) {
	    # ��
	    if($lv < 200) {
		# �ڤ����䤹
		$landValue->[$x][$y]++;
	    }
	} elsif($landKind == $HlandDefence) {
	    if($lv == 1) {
		# �ɱһ��߼���
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# �����ﳲ�롼����
		wideDamage($id, $name, $land, $landValue, $x, $y);
	    }
	} elsif($landKind == $HlandOil) {
	    # ��������
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $HoilMoney;
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";

	    # ������
	    logOilMoney($id, $name, $lName, "($x, $y)", $str);

	    # �ϳ�Ƚ��
	    if(random(1000) < $HoilRatio) {
		# �ϳ�
		logOilEnd($id, $name, $lName, "($x, $y)");
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 0;
	    }

	} elsif($landKind == $HlandMonster) {
	    # ����
	    if($monsterMove[$x][$y] == 2) {
		# ���Ǥ�ư������
		next;
	    }

	    # �����Ǥμ��Ф�
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];

	    # �Ų���?
	    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
	       (($special == 4) && (($HislandTurn % 2) == 0))) {
		# �Ų���
		next;
	    }

	    # ư�����������
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# �Ԥˤ�����Ĵ��
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# �ϰϳ�Ƚ��
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# �����������ġ����á�������ǰ��ʳ�
		if(($land->[$sx][$sy] != $HlandSea) &&
		   ($land->[$sx][$sy] != $HlandSbase) &&
		   ($land->[$sx][$sy] != $HlandOil) &&
		   ($land->[$sx][$sy] != $HlandMountain) &&
		   ($land->[$sx][$sy] != $HlandMonument) &&
		   ($land->[$sx][$sy] != $HlandMonster)) {
		    last;
		}
	    }

	    if($i == 3) {
		# ư���ʤ��ä�
		next;
	    }

	    # ư��������Ϸ��ˤ���å�����
	    my($l) = $land->[$sx][$sy];
	    my($lv) = $landValue->[$sx][$sy];
	    my($lName) = landName($l, $lv);
	    my($point) = "($sx, $sy)";

	    # ��ư
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ��ȵ錄���֤���Ϥ�
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;

	    # ��ư�Ѥߥե饰
	    if($HmonsterSpecial[$mKind] == 2) {
		# ��ư�Ѥߥե饰��Ω�Ƥʤ�
	    } elsif($HmonsterSpecial[$mKind] == 1) {
		# ®������
		$monsterMove[$sx][$sy] = $monsterMove[$x][$y] + 1;
	    } else {
		# ���̤β���
		$monsterMove[$sx][$sy] = 2;
	    }

	    if(($l == $HlandDefence) && ($HdBaseAuto == 1)) {
		# �ɱһ��ߤ�Ƨ���
		logMonsMoveDefence($id, $name, $lName, $point, $mName);

		# �����ﳲ�롼����
		wideDamage($id, $name, $land, $landValue, $sx, $sy);
	    } else {
		# �Ԥ��褬���Ϥˤʤ�
		logMonsMove($id, $name, $lName, $point, $mName);
	    }
	}

	# �к�Ƚ��
	if((($landKind == $HlandTown) && ($lv > 30)) ||
	   ($landKind == $HlandHaribote) ||
	   ($landKind == $HlandFactory)) {
	    if(random(1000) < $HdisFire) {
		# ���Ϥο��ȵ�ǰ��������
		if((countAround($land, $x, $y, $HlandForest, 7) +
		    countAround($land, $x, $y, $HlandMonument, 7)) == 0) {
		    # ̵���ä���硢�кҤǲ���
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($point) = "($x, $y)";
		    my($lName) = landName($l, $lv);
		    logFire($id, $name, $lName, $point);
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}
    }
}

# ���Ϥ�Į�����줬���뤫Ƚ��
sub countGrow {
    my($land, $landValue, $x, $y) = @_;
    my($i, $sx, $sy);
    for($i = 1; $i < 7; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];

	 # �Ԥˤ�����Ĵ��
	 if((($sy % 2) == 0) && (($y % 2) == 1)) {
	     $sx--;
	 }

	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	 } else {
	     # �ϰ���ξ��
	     if(($land->[$sx][$sy] == $HlandTown) ||
		($land->[$sx][$sy] == $HlandFarm)) {
		 if($landValue->[$sx][$sy] != 1) {
		     return 1;
		 }
	     }
	 }
    }
    return 0;
}

# ������
sub doIslandProcess {
    my($number, $island) = @_;

    # Ƴ����
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # �Ͽ�Ƚ��
    if(random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake)) {
	# �Ͽ�ȯ��
	logEarthquake($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if((($landKind == $HlandTown) && ($lv >= 100)) ||
	       ($landKind == $HlandHaribote) ||
	       ($landKind == $HlandFactory)) {
		# 1/4�ǲ���
		if(random(4) == 0) {
		    logEQDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }

	}
    }

    # ������­
    if($island->{'food'} <= 0) {
	# ��­��å�����
	logStarve($id, $name);
	$island->{'food'} = 0;

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
	       ($landKind == $HlandFactory) ||
	       ($landKind == $HlandBase) ||
	       ($landKind == $HlandDefence)) {
		# 1/4�ǲ���
		if(random(4) == 0) {
		    logSvDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}
    }

    # ����Ƚ��
    if(random(1000) < $HdisTsunami) {
	# ����ȯ��
	logTsunami($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandTown) ||
	       ($landKind == $HlandFarm) ||
	       ($landKind == $HlandFactory) ||
	       ($landKind == $HlandBase) ||
	       ($landKind == $HlandDefence) ||
	       ($landKind == $HlandHaribote)) {
		# 1d12 <= (���Ϥγ� - 1) ������
		if(random(12) <
		   (countAround($land, $x, $y, $HlandOil, 7) +
		    countAround($land, $x, $y, $HlandSbase, 7) +
		    countAround($land, $x, $y, $HlandSea, 7) - 1)) {
		    logTsunamiDamage($id, $name, landName($landKind, $lv),
				     "($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }

	}
    }

    # ����Ƚ��
    my($r) = random(10000);
    my($pop) = $island->{'pop'};
    do{
	if((($r < ($HdisMonster * $island->{'area'})) &&
	    ($pop >= $HdisMonsBorder1)) ||
	   ($island->{'monstersend'} > 0)) {
	    # ���ýи�
	    # ��������
	    my($lv, $kind);
	    if($island->{'monstersend'} > 0) {
		# ��¤
		$kind = 0;
		$island->{'monstersend'}--;
	    } elsif($pop >= $HdisMonsBorder3) {
		# level3�ޤ�
		$kind = random($HmonsterLevel3) + 1;
	    } elsif($pop >= $HdisMonsBorder2) {
		# level2�ޤ�
		$kind = random($HmonsterLevel2) + 1;
	    } else {
		# level1�Τ�
		$kind = random($HmonsterLevel1) + 1;
	    }

	    # lv���ͤ����
	    $lv = $kind * 10
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);

	    # �ɤ��˸���뤫����
	    my($bx, $by, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {

		    # �Ϸ�̾
		    my($lName) = landName($HlandTown, $landValue->[$bx][$by]);

		    # ���Υإå�������ä�
		    $land->[$bx][$by] = $HlandMonster;
		    $landValue->[$bx][$by] = $lv;

		    # ���þ���
		    my($mKind, $mName, $mHp) = monsterSpec($lv);

		    # ��å�����
		    logMonsCome($id, $name, $mName, "($bx, $by)", $lName);
		    last;
		}
	    }
	}
    } while($island->{'monstersend'} > 0);

    # ��������Ƚ��
    if(($island->{'area'} > $HdisFallBorder) &&
       (random(1000) < $HdisFalldown)) {
	# ��������ȯ��
	logFalldown($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind != $HlandSea) &&
	       ($landKind != $HlandSbase) &&
	       ($landKind != $HlandOil) &&
	       ($landKind != $HlandMountain)) {

		# ���Ϥ˳�������С��ͤ�-1��
		if(countAround($land, $x, $y, $HlandSea, 7) + 
		   countAround($land, $x, $y, $HlandSbase, 7)) {
		    logFalldownLand($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = -1;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}

	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];

	    if($landKind == -1) {
		# -1�ˤʤäƤ�����������
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    } elsif ($landKind == $HlandSea) {
		# �����ϳ���
		$landValue->[$x][$y] = 0;
	    }

	}
    }

    # ����Ƚ��
    if(random(1000) < $HdisTyphoon) {
	# ����ȯ��
	logTyphoon($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
	       ($landKind == $HlandHaribote)) {

		# 1d12 <= (6 - ���Ϥο�) ������
		if(random(12) < 
		   (6
		    - countAround($land, $x, $y, $HlandForest, 7)
		    - countAround($land, $x, $y, $HlandMonument, 7))) {
		    logTyphoonDamage($id, $name, landName($landKind, $lv),
				     "($x, $y)");
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		}
	    }

	}
    }

    # �������Ƚ��
    if(random(1000) < $HdisHugeMeteo) {
	my($x, $y, $landKind, $lv, $point);

	# �
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# ��å�����
	logHugeMeteo($id, $name, $point);

	# �����ﳲ�롼����
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # ����ߥ�����Ƚ��
    while($island->{'bigmissile'} > 0) {
	$island->{'bigmissile'} --;

	my($x, $y, $landKind, $lv, $point);

	# �
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# ��å�����
	logMonDamage($id, $name, $point);

	# �����ﳲ�롼����
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # ���Ƚ��
    if(random(1000) < $HdisMeteo) {
	my($x, $y, $landKind, $lv, $point, $first);
	$first = 1;
	while((random(2) == 0) || ($first == 1)) {
	    $first = 0;
	    
	    # �
	    $x = random($HislandSize);
	    $y = random($HislandSize);
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $point = "($x, $y)";

	    if(($landKind == $HlandSea) && ($lv == 0)){
		# ���ݥ���
		logMeteoSea($id, $name, landName($landKind, $lv),
			    $point);
	    } elsif($landKind == $HlandMountain) {
		# ���˲�
		logMeteoMountain($id, $name, landName($landKind, $lv),
				 $point);
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		next;
	    } elsif($landKind == $HlandSbase) {
		logMeteoSbase($id, $name, landName($landKind, $lv),
			      $point);
	    } elsif($landKind == $HlandMonster) {
		logMeteoMonster($id, $name, landName($landKind, $lv),
				$point);
	    } elsif($landKind == $HlandSea) {
		# ����
		logMeteoSea1($id, $name, landName($landKind, $lv),
			     $point);
	    } else {
		logMeteoNormal($id, $name, landName($landKind, $lv),
			       $point);
	    }
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	}
    }

    # ʮ��Ƚ��
    if(random(1000) < $HdisEruption) {
	my($x, $y, $sx, $sy, $i, $landKind, $lv, $point);
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";
	logEruption($id, $name, landName($landKind, $lv),
		    $point);
	$land->[$x][$y] = $HlandMountain;
	$landValue->[$x][$y] = 0;

	for($i = 1; $i < 7; $i++) {
	    $sx = $x + $ax[$i];
	    $sy = $y + $ay[$i];

	    # �Ԥˤ�����Ĵ��
	    if((($sy % 2) == 0) && (($y % 2) == 1)) {
		$sx--;
	    }

	    $landKind = $land->[$sx][$sy];
	    $lv = $landValue->[$sx][$sy];
	    $point = "($sx, $sy)";

	    if(($sx < 0) || ($sx >= $HislandSize) ||
	       ($sy < 0) || ($sy >= $HislandSize)) {
	    } else {
		# �ϰ���ξ��
		$landKind = $land->[$sx][$sy];
		$lv = $landValue->[$sx][$sy];
		$point = "($sx, $sy)";
		if(($landKind == $HlandSea) ||
		   ($landKind == $HlandOil) ||
		   ($landKind == $HlandSbase)) {
		    # ���ξ��
		    if($lv == 1) {
			# ����
			logEruptionSea1($id, $name, landName($landKind, $lv),
					$point);
		    } else {
			logEruptionSea($id, $name, landName($landKind, $lv),
				       $point);
			$land->[$sx][$sy] = $HlandSea;
			$landValue->[$sx][$sy] = 1;
			next;
		    }
		} elsif(($landKind == $HlandMountain) ||
			($landKind == $HlandMonster) ||
			($landKind == $HlandWaste)) {
		    next;
		} else {
		    # ����ʳ��ξ��
		    logEruptionNormal($id, $name, landName($landKind, $lv),
				      $point);
		}
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    }
	}
    }

    # ���������դ�Ƥ��鴹��
    if($island->{'food'} > 9999) {
	$island->{'money'} += int(($island->{'food'} - 9999) / 10);
	$island->{'food'} = 9999;
    } 

    # �⤬���դ�Ƥ����ڤ�Τ�
    if($island->{'money'} > 9999) {
	$island->{'money'} = 9999;
    } 

    # �Ƽ���ͤ�׻�
    estimate($number);

    # �˱ɡ������
    $pop = $island->{'pop'};
    my($damage) = $island->{'oldPop'} - $pop;
    my($prize) = $island->{'prize'};
    $prize =~ /([0-9]*),([0-9]*),(.*)/;
    my($flags) = $1;
    my($monsters) = $2;
    my($turns) = $3;

    # �˱ɾ�
    if((!($flags & 1)) &&  $pop >= 3000){
	$flags |= 1;
	logPrize($id, $name, $Hprize[1]);
    } elsif((!($flags & 2)) &&  $pop >= 5000){
	$flags |= 2;
	logPrize($id, $name, $Hprize[2]);
    } elsif((!($flags & 4)) &&  $pop >= 10000){
	$flags |= 4;
	logPrize($id, $name, $Hprize[3]);
    }

    # �����
    if((!($flags & 64)) &&  $damage >= 500){
	$flags |= 64;
	logPrize($id, $name, $Hprize[7]);
    } elsif((!($flags & 128)) &&  $damage >= 1000){
	$flags |= 128;
	logPrize($id, $name, $Hprize[8]);
    } elsif((!($flags & 256)) &&  $damage >= 2000){
	$flags |= 256;
	logPrize($id, $name, $Hprize[9]);
    }

    $island->{'prize'} = "$flags,$monsters,$turns";
}

# �͸���˥�����
sub islandSort {
    my($flag, $i, $tmp);

    # �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# �����ﳲ�롼����
sub wideDamage {
    my($id, $name, $land, $landValue, $x, $y) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 19; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];

	# �Ԥˤ�����Ĵ��
	if((($sy % 2) == 0) && (($y % 2) == 1)) {
	    $sx--;
	}
    
	$landKind = $land->[$sx][$sy];
	$lv = $landValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# �ϰϳ�Ƚ��
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# �ϰϤˤ��ʬ��
	if($i < 7) {
	    # �濴�������1�إå���
	    if($landKind == $HlandSea) {
		$landValue->[$sx][$sy] = 0;
		next;
	    } elsif(($landKind == $HlandSbase) ||
		    ($landKind == $HlandOil)) {
		logWideDamageSea2($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = 0;
	    } else {
		if($landKind == $HlandMonster) {
		    logWideDamageMonsterSea($id, $name, $landName, $point);
		} else {
		    logWideDamageSea($id, $name, $landName, $point);
		}
		$land->[$sx][$sy] = $HlandSea;
		if($i == 0) {
		    # ��
		    $landValue->[$sx][$sy] = 0;
		} else {
		    # ����
		    $landValue->[$sx][$sy] = 1;
		}
	    }
	} else {
	    # 2�إå���
	    if(($landKind == $HlandSea) ||
	       ($landKind == $HlandOil) ||
	       ($landKind == $HlandWaste) ||
	       ($landKind == $HlandMountain) ||
	       ($landKind == $HlandSbase)) {
		next;
	    } elsif($landKind == $HlandMonster) {
		logWideDamageMonster($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    } else {
		logWideDamageWaste($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    }
	}
    }
}

# ���ؤν���
# ��1����:��å�����
# ��2����:������
# ��3����:���
# �̾��
sub logOut {
    push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �ٱ��
sub logLate {
    push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��̩��
sub logSecret {
    push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��Ͽ��
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

# ��Ͽ��Ĵ��
sub logHistoryTrim {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l, $count);
    $count = 0;
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
	$count++;
    }
    close(HIN);

    if($count > $HhistoryMax) {
	open(HOUT, ">${HdirName}/hakojima.his");
	my($i);
	for($i = ($count - $HhistoryMax); $i < $count; $i++) {
	    print HOUT "$line[$i]\n";
	}
	close(HOUT);
    }
}

# ���񤭽Ф�
sub logFlush {
    open(LOUT, ">${HdirName}/hakojima.log0");

    # �����ս�ˤ��ƽ񤭽Ф�
    my($i);
    for($i = $#HsecretLogPool; $i >= 0; $i--) {
	print LOUT $HsecretLogPool[$i];
	print LOUT "\n";
    }
    for($i = $#HlateLogPool; $i >= 0; $i--) {
	print LOUT $HlateLogPool[$i];
	print LOUT "\n";
    }
    for($i = $#HlogPool; $i >= 0; $i--) {
	print LOUT $HlogPool[$i];
	print LOUT "\n";
    }
    close(LOUT);
}

#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
# ���­��ʤ�
sub logNoMoney {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ������­�Τ�����ߤ���ޤ�����",$id);
}

# ����­��ʤ�
sub logNoFood {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ����߿�����­�Τ�����ߤ���ޤ�����",$id);
}

# �о��Ϸ��μ���ˤ�뼺��
sub logLandFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}��<B>$kind</B>���ä�������ߤ���ޤ�����",$id);
END
}

# �����Φ���ʤ������Ω�Ƽ���
sub logNoLandAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ�Φ�Ϥ��ʤ��ä�������ߤ���ޤ�����",$id);
END
}

# ���Ϸ�����
sub logLandSuc {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
END
}

# ����ȯ��
sub logOilFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ�졢<B>���Ĥ��������Ƥ��ޤ���</B>��",$id);
END
}

# ����ȯ���ʤ餺
sub logOilFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>��ͽ����Ĥ������${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ����������Ĥϸ��Ĥ���ޤ���Ǥ�����",$id);
END
}

# ���Ĥ���μ���
sub logOilMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>���顢<B>$str</B>�μ��פ��夬��ޤ�����",$id);
END
}

# ���ĸϳ�
sub logOilEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϸϳ餷���褦�Ǥ���",$id);
END
}

# �ɱһ��ߡ��������å�
sub logBombSet {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�������֤����å�</B>����ޤ�����",$id);
END
}

# �ɱһ��ߡ�������ư
sub logBombFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�������ֺ�ư����${H_tagDisaster}",$id);
END
}

# ��ǰ�ꡢȯ��
sub logMonFly {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�첻�ȤȤ������Ω���ޤ���</B>��",$id);
END
}

# ��ǰ�ꡢ�
sub logMonDamage {
    my($id, $name, $point) = @_;
    logOut("<B>�����ȤƤĤ�ʤ����</B>��${HtagName_}${name}��$point${H_tagName}����������ޤ�������",$id);
}

# ����or�ߥ��������
sub logPBSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
    logOut("������ʤ�����${HtagName_}${name}��${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
END
}

# �ϥ�ܥ�
sub logHariSuc {
    my($id, $name, $comName, $comName2, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
    logLandSuc($id, $name, $comName2, $point);
END
}

# �ߥ������Ȥ��Ȥ���(or �����ɸ����褦�Ȥ���)���������åȤ����ʤ�
sub logMsNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ����˿ͤ���������ʤ�������ߤ���ޤ�����",$id);
END
}

# �ߥ������Ȥ��Ȥ��������Ϥ��ʤ�
sub logMsNoBase {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>�ߥ�������������ͭ���Ƥ��ʤ�</B>����˼¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

# �ߥ������ä����ϰϳ�
sub logMsOut {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id, $tId);
}

# ���ƥ륹�ߥ������ä����ϰϳ�
sub logMsOutS {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�ظ�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$tId);
}

# �ߥ������ä����ɱһ��ߤǥ���å�
sub logMsCaught {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$id, $tId);
}

# ���ƥ륹�ߥ������ä����ɱһ��ߤǥ���å�
sub logMsCaughtS {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�ظ�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$tId);
}

# �ߥ������ä������̤ʤ�
sub logMsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);
}

# ���ƥ륹�ߥ������ä������̤ʤ�
sub logMsNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);

    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$tId);
}

# Φ���˲��ơ�����̿��
sub logMsLDMountain {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>�Ͼä����ӡ����ϤȲ����ޤ�����",$id, $tId);
}

# Φ���˲��ơ�������Ϥ�̿��
sub logMsLDSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��������ȯ��Ʊ�����ˤ��ä�<B>$tLname</B>���׷���ʤ��᤭���Ӥޤ�����",$id, $tId);
}

# Φ���˲��ơ����ä�̿��
sub logMsLDMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}�����Ƥ���ȯ��Φ�Ϥ�<B>����$tLname</B>���Ȥ���פ��ޤ�����",$id, $tId);
}

# Φ���˲��ơ�������̿��
sub logMsLDSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ����줬�������ޤ�����",$id, $tId);
}

# Φ���˲��ơ�����¾���Ϸ���̿��
sub logMsLDLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�����ơ�Φ�ϤϿ��פ��ޤ�����",$id, $tId);
}

# �̾�ߥ����롢���Ϥ�����
sub logMsWaste {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id, $tId);
}

# ���ƥ륹�ߥ����롢���Ϥ�����
sub logMsWasteS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$tId);
}

# �̾�ߥ����롢���ä�̿�桢�Ų���ˤ�̵��
sub logMsMonNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$id, $tId);
}

# ���ƥ륹�ߥ����롢���ä�̿�桢�Ų���ˤ�̵��
sub logMsMonNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$id, $tId);
    logOut("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",$tId);
}

# �̾�ߥ����롢���ä�̿�桢����
sub logMsMonKill {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",$id, $tId);
}

# ���ƥ륹�ߥ����롢���ä�̿�桢����
sub logMsMonKillS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����", $tId);
}

# �̾�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$id, $tId);
}

# ���ƥ륹�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonsterS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",$tId);
}

# ���äλ���
sub logMsMonMoney {
    my($tId, $mName, $value) = @_;
    logOut("<B>����$mName</B>�λĳ��ˤϡ�<B>$value$HunitMoney</B>���ͤ��դ��ޤ�����",$tId);
}

# �̾�ߥ������̾��Ϸ���̿��
sub logMsNormal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
}

# ���ƥ륹�ߥ������̾��Ϸ���̿��
sub logMsNormalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
    logLate("<B>���Ԥ�</B>��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$tId);
}

# �ߥ�������̱����
sub logMsBoatPeople {
    my($id, $name, $achive) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$achive${HunitPop}�����̱</B>��ɺ�夷�ޤ�����${HtagName_}${name}��${H_tagName}�ϲ����������줿�褦�Ǥ���",$id);
}

# �����ɸ�
sub logMonsSend {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>��¤����</B>���¤��${HtagName_}${tName}��${H_tagName}�����ꤳ�ߤޤ�����",$id, $tId);
}

# ��ⷫ��
sub logDoNothing {
    my($id, $name, $comName) = @_;
#    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ͢��
sub logSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$value$HunitFood</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}

# ���
sub logAid {
    my($id, $tId, $name, $tName, $comName, $str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id, $tId);
}

# Ͷ�׳�ư
sub logPropaganda {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ����
sub logGiveup {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}���������졢<B>̵����</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}����������<B>̵����</B>�Ȥʤ롣");
}

# ����
sub logDead {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����ͤ����ʤ��ʤꡢ<B>̵����</B>�ˤʤ�ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}���ͤ����ʤ��ʤ�<B>̵����</B>�Ȥʤ롣");
}

# ȯ��
sub logDiscover {
    my($name) = @_;
    logHistory("${HtagName_}${name}��${H_tagName}��ȯ������롣");
}

# ̾�����ѹ�
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagName_}${name1}��${H_tagName}��̾�Τ�${HtagName_}${name2}��${H_tagName}���ѹ����롣");
}

# ����
sub logStarve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}

# ���ø���
sub logMonsCome {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>����$mName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>��Ƨ�߹Ӥ餵��ޤ�����",$id);
}

# ����ư��
sub logMonsMove {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>����$mName</B>��Ƨ�߹Ӥ餵��ޤ�����",$id);
}

# ���á��ɱһ��ߤ�Ƨ��
sub logMonsMoveDefence {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>����$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}�μ������֤���ư����</B>",$id);
}

# �к�
sub logFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�к�${H_tagDisaster}�ˤ����Ǥ��ޤ�����",$id);
}

# ��¢��
sub logMaizo {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�Ǥ�${HtagComName_}$comName${H_tagComName}��ˡ�<B>$value$HunitMoney�����¢��</B>��ȯ������ޤ�����",$id);
}

# �Ͽ�ȯ��
sub logEarthquake {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}���絬�Ϥ�${HtagDisaster_}�Ͽ�${H_tagDisaster}��ȯ������",$id);
}

# �Ͽ��ﳲ
sub logEQDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ͽ�${H_tagDisaster}�ˤ����Ǥ��ޤ�����",$id);
}

# ������­�ﳲ
sub logSvDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>�ϲ��Ǥ��ޤ�����",$id);
}

# ����ȯ��
sub logTsunami {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ն��${HtagDisaster_}����${H_tagDisaster}ȯ������",$id);
}

# �����ﳲ
sub logTsunamiDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�ˤ���������ޤ�����",$id);
}

# ����ȯ��
sub logTyphoon {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}����${H_tagDisaster}��Φ����",$id);
}

# �����ﳲ
sub logTyphoonDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�����Ф���ޤ�����",$id);
}

# ��С���
sub logMeteoSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}������ޤ�����",$id);
}

# ��С���
sub logMeteoMountain {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# ��С��������
sub logMeteoSbase {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>���������ޤ�����",$id);
}

# ��С�����
sub logMeteoMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("<B>����$lName</B>������${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}�����Φ�Ϥ�<B>����$lName</B>���Ȥ���פ��ޤ�����",$id);
}

# ��С�����
sub logMeteoSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}��������줬�������ޤ�����",$id);
}

# ��С�����¾
sub logMeteoNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}��������Ӥ����פ��ޤ�����",$id);
}

# ��С�����¾
sub logHugeMeteo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}�������${H_tagDisaster}�������",$id);
}

# ʮ��
sub logEruption {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������${HtagDisaster_}�л���ʮ��${H_tagDisaster}��<B>��</B>������ޤ�����",$id);
}

# ʮ�С�����
sub logEruptionSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ���Φ�Ϥˤʤ�ޤ�����",$id);
}

# ʮ�С���or����
sub logEruptionSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǳ��줬δ���������ˤʤ�ޤ�����",$id);
}

# ʮ�С�����¾
sub logEruptionNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǲ��Ǥ��ޤ�����",$id);
}

# ��������ȯ��
sub logFalldown {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������${H_tagDisaster}��ȯ�����ޤ�������",$id);
}

# ���������ﳲ
sub logFalldownLand {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϳ���������ߤޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>����</B>���ޤ�����",$id);
}

# �����ﳲ�����η���
sub logWideDamageSea2 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>���׷���ʤ��ʤ�ޤ�����",$id);
}

# �����ﳲ�����ÿ���
sub logWideDamageMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��Φ�Ϥ�<B>����$lName</B>���Ȥ���פ��ޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>����$lName</B>�Ͼä����Ӥޤ�����",$id);
}

# �����ﳲ������
sub logWideDamageWaste {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϰ�֤ˤ���<B>����</B>�Ȳ����ޤ�����",$id);
}

# ����
sub logPrize {
    my($id, $name, $pName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$pName</B>����ޤ��ޤ�����",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>$pName</B>�����");
}

# �礬���äѤ��ʾ��
sub tempNewIslandFull {
    out(<<END);
${HtagBig_}����������ޤ����礬���դ���Ͽ�Ǥ��ޤ��󡪡�${H_tagBig}$HtempBack
END
}

# ������̾�����ʤ����
sub tempNewIslandNoName {
    out(<<END);
${HtagBig_}��ˤĤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ������̾���������ʾ��
sub tempNewIslandBadName {
    out(<<END);
${HtagBig_}',?()<>\$'�Ȥ����äƤ��ꡢ��̵����פȤ����ä��Ѥ�̾���Ϥ��ޤ��礦���${H_tagBig}$HtempBack
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewIslandAlready {
    out(<<END);
${HtagBig_}������ʤ餹�Ǥ�ȯ������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɤ��ʤ����
sub tempNewIslandNoPassword {
    out(<<END);
${HtagBig_}�ѥ���ɤ�ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ���ȯ�����ޤ���!!
sub tempNewIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}���ȯ�����ޤ�������${H_tagBig}<BR>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}��̿̾���ޤ���${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �Ϸ��θƤ���
sub landName {
    my($land, $lv) = @_;
    if($land == $HlandSea) {
	if($lv == 1) {
            return '����';
        } else {
            return '��';
	}
    } elsif($land == $HlandWaste) {
	return '����';
    } elsif($land == $HlandPlains) {
	return 'ʿ��';
    } elsif($land == $HlandTown) {
	if($lv < 30) {
	    return '¼';
	} elsif($lv < 100) {
	    return 'Į';
	} else {
	    return '�Ի�';
	}
    } elsif($land == $HlandForest) {
	return '��';
    } elsif($land == $HlandFarm) {
	return '����';
    } elsif($land == $HlandFactory) {
	return '����';
    } elsif($land == $HlandBase) {
	return '�ߥ��������';
    } elsif($land == $HlandDefence) {
	return '�ɱһ���';
    } elsif($land == $HlandMountain) {
	return '��';
    } elsif($land == $HlandMonster) {
	my($kind, $name, $hp) = monsterSpec($lv);
	return $name;
    } elsif($land == $HlandSbase) {
	return '�������';
    } elsif($land == $HlandOil) {
	return '��������';
    } elsif($land == $HlandMonument) {
	return $HmonumentName[$lv];
    } elsif($land == $HlandHaribote) {
	return '�ϥ�ܥ�';
    }
}

# �͸�����¾���ͤ򻻽�
sub estimate {
    my($number) = $_[0];
    my($island);
    my($pop, $area, $farm, $factory, $mountain) = (0, 0, 0, 0, 0, 0);

    # �Ϸ������
    $island = $Hislands[$number];
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # ������
    my($x, $y, $kind, $value);
    for($y = 0; $y < $HislandSize; $y++) {
	for($x = 0; $x < $HislandSize; $x++) {
	    $kind = $land->[$x][$y];
	    $value = $landValue->[$x][$y];
	    if(($kind != $HlandSea) &&
	       ($kind != $HlandSbase) &&
	       ($kind != $HlandOil)){
		$area++;
		if($kind == $HlandTown) {
		    # Į
		    $pop += $value;
		} elsif($kind == $HlandFarm) {
		    # ����
		    $farm += $value;
		} elsif($kind == $HlandFactory) {
		    # ����
		    $factory += $value;
		} elsif($kind == $HlandMountain) {
		    # ��
		    $mountain += $value;
		}
	    }
	}
    }

    # ����
    $island->{'pop'}      = $pop;
    $island->{'area'}     = $area;
    $island->{'farm'}     = $farm;
    $island->{'factory'}  = $factory;
    $island->{'mountain'} = $mountain;
}


# �ϰ�����Ϸ��������
sub countAround {
    my($land, $x, $y, $kind, $range) = @_;
    my($i, $count, $sx, $sy);
    $count = 0;
    for($i = 0; $i < $range; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];

	 # �Ԥˤ�����Ĵ��
	 if((($sy % 2) == 0) && (($y % 2) == 1)) {
	     $sx--;
	 }

	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	     # �ϰϳ��ξ��
	     if($kind == $HlandSea) {
		 # ���ʤ�û�
		 $count++;
	     }
	 } else {
	     # �ϰ���ξ��
	     if($land->[$sx][$sy] == $kind) {
		 $count++;
	     }
	 }
    }
    return $count;
}

# 0����(n - 1)�ޤǤο��������ŤĽФƤ���������
sub randomArray {
    my($n) = @_;
    my(@list, $i);

    # �����
    if($n == 0) {
	$n = 1;
    }
    @list = (0..$n-1);

    # ����åե�
    for ($i = $n; --$i; ) {
	my($j) = int(rand($i+1));
	if($i == $j) { next; };
	@list[$i,$j] = @list[$j,$i];
    }

    return @list;
}

# ̾���ѹ�����
sub tempChangeNothing {
    out(<<END);
${HtagBig_}̾�����ѥ���ɤȤ�˶���Ǥ�${H_tagBig}$HtempBack
END
}

# ̾���ѹ����­�ꤺ
sub tempChangeNoMoney {
    out(<<END);
${HtagBig_}�����­�Τ����ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ�����
sub tempChange {
    out(<<END);
${HtagBig_}�ѹ���λ���ޤ���${H_tagBig}$HtempBack
END
}

1;
