#!/usr/local/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������

#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ���ƥʥ󥹥ġ���(ver1.01)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------


# ������������������������������������������������������������
# �Ƽ�������
# ������������������������������������������������������������

# �ޥ������ѥ����
my($masterpassword) = 'yourpassword';

# 1�����󤬲��ä�
my($unitTime) = 21600; # 6����

# �ǥ��쥯�ȥ�Υѡ��ߥå����
my($dirMode) = 0755;

# ���Υե�����
my($thisFile) = 'http://���/hako-mente.cgi';

# �ǡ����ǥ��쥯�ȥ��̾��
# hakojima.cgi��Τ�Τȹ�碌�Ƥ���������
my($dirName) = 'data';


# use Time::Local���Ȥ��ʤ��Ķ��Ǥϡ�'use Time::Local'�ιԤ�ä��Ʋ�������
# ���������������֤��ѹ���'�û�����ѹ�'�����Ǥ��ʤ��ʤ�ޤ���
use Time::Local;

# ������������������������������������������������������������
# ������ܤϰʾ�
# ������������������������������������������������������������

# �Ƽ��ѿ�
my($mainMode);
my($inputPass);
my($deleteID);
my($currentID);
my($ctYear);
my($ctMon);
my($ctDate);
my($ctHour);
my($ctMin);
my($ctSec);

print <<END;
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Ȣ�磲 ���ƥʥ󥹥ġ���</TITLE>
</HEAD>
<BODY>
END

cgiInput();

if($mainMode eq 'delete') {
    if(passCheck()) {
	deleteMode();
    }
} elsif($mainMode eq 'current') {
    if(passCheck()) {
	currentMode();
    }
} elsif($mainMode eq 'time') {
    if(passCheck()) {
	timeMode();
    }
} elsif($mainMode eq 'stime') {
    if(passCheck()) {
	stimeMode();
    }
} elsif($mainMode eq 'new') {
    if(passCheck()) {
	newMode();
    }
}
mainMode();

print <<END;
</FORM>
</BODY>
</HTML>
END

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

sub currentMode {
    myrmtree "${dirName}";
    mkdir("${dirName}", $dirMode);
    opendir(DIN, "${dirName}.bak$currentID/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	fileCopy("${dirName}.bak$currentID/$fileName", "${dirName}/$fileName");
    } 
    closedir(DIN);
}

sub deleteMode {
    if($deleteID eq '') {
	myrmtree "${dirName}";
    } else {
	myrmtree "${dirName}.bak$deleteID";
    }
    unlink "hakojimalockflock";
}

sub newMode {
    mkdir($dirName, $dirMode);

    # ���ߤλ��֤����
    my($now) = time;
    $now = $now - ($now % ($unitTime));

    open(OUT, ">$dirName/hakojima.dat"); # �ե�����򳫤�
    print OUT "1\n";         # �������1
    print OUT "$now\n";      # ���ϻ���
    print OUT "0\n";         # ��ο�
    print OUT "1\n";         # ���˳�����Ƥ�ID

    # �ե�������Ĥ���
    close(OUT);
}

sub timeMode {
    $ctMon--;
    $ctYear -= 1900;
    $ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
    stimeMode();
}

sub stimeMode {
    my($t) = $ctSec;
    open(IN, "${dirName}/hakojima.dat");
    my(@lines);
    @lines = <IN>;
    close(IN);

    $lines[1] = "$t\n";

    open(OUT, ">${dirName}/hakojima.dat");
    print OUT @lines;
    close(OUT);
}

sub mainMode {
    opendir(DIN, "./");

    print <<END;
<FORM action="$thisFile" method="POST">
<H1>Ȣ�磲 ���ƥʥ󥹥ġ���</H1>
<B>�ѥ����:</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD></TD>
END

    # ����ǡ���
    if(-d "${dirName}") {
	dataPrint("");
    } else {
	print <<END;
    <HR>
    <INPUT TYPE="submit" VALUE="�������ǡ�������" NAME="NEW">
END
    }

    # �Хå����åץǡ���
    my($dn);
    while($dn = readdir(DIN)) {
	if($dn =~ /^${dirName}.bak(.*)/) {
	    dataPrint($1);
	}
    } 
    closedir(DIN);
}

# ɽ���⡼��
sub dataPrint {
    my($suf) = @_;

    print "<HR>";
    if($suf eq "") {
	open(IN, "${dirName}/hakojima.dat");
	print "<H1>����ǡ���</H1>";
    } else {
	open(IN, "${dirName}.bak$suf/hakojima.dat");
	print "<H1>�Хå����å�$suf</H1>";
    }

    my($lastTurn);
    $lastTurn = <IN>;
    my($lastTime);
    $lastTime = <IN>;

    my($timeString) = timeToString($lastTime);

    print <<END;
    <B>������$lastTurn</B><BR>
    <B>�ǽ���������</B>:$timeString<BR>
    <B>�ǽ���������(�ÿ�ɽ��)</B>:1970ǯ1��1������$lastTime ��<BR>
    <INPUT TYPE="submit" VALUE="���Υǡ�������" NAME="DELETE$suf">
END

    if($suf eq "") {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	    localtime($lastTime);
	$mon++;
	$year += 1900;

	print <<END;
    <H2>�ǽ��������֤��ѹ�</H2>
    <INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">ǯ
    <INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">��
    <INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">��
    <INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">��
    <INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">ʬ
    <INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">��
    <INPUT TYPE="submit" VALUE="�ѹ�" NAME="NTIME"><BR>
    1970ǯ1��1������<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">��
    <INPUT TYPE="submit" VALUE="�û�����ѹ�" NAME="STIME">

END
    } else {
	print <<END;
	<INPUT TYPE="submit" VALUE="���Υǡ��������" NAME="CURRENT$suf">
END
    }
}

sub timeToString {
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
    $mon++;
    $year += 1900;

    return "${year}ǯ ${mon}�� ${date}�� ${hour}�� ${min}ʬ ${sec}��";
}

# CGI���ɤߤ���
sub cgiInput {
    my($line);

    # ���Ϥ�������
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

    if($line =~ /DELETE([0-9]*)/) {
	$mainMode = 'delete';
	$deleteID = $1;
    } elsif($line =~ /CURRENT([0-9]*)/) {
	$mainMode = 'current';
	$currentID = $1;
    } elsif($line =~ /NEW/) {
	$mainMode = 'new';
    } elsif($line =~ /NTIME/) {
	$mainMode = 'time';
	if($line =~ /YEAR=([0-9]*)/) {
	    $ctYear = $1; 
	}
	if($line =~ /MON=([0-9]*)/) {
	    $ctMon = $1; 
	}
	if($line =~ /DATE=([0-9]*)/) {
	    $ctDate = $1; 
	}
	if($line =~ /HOUR=([0-9]*)/) {
	    $ctHour = $1; 
	}
	if($line =~ /MIN=([0-9]*)/) {
	    $ctMin = $1; 
	}
	if($line =~ /NSEC=([0-9]*)/) {
	    $ctSec = $1; 
	}
    } elsif($line =~ /STIME/) {
	$mainMode = 'stime';
	if($line =~ /SSEC=([0-9]*)/) {
	    $ctSec = $1; 
	}
    }

    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$inputPass = $1;
    }
}

# �ե�����Υ��ԡ�
sub fileCopy {
    my($src, $dist) = @_;
    open(IN, $src);
    open(OUT, ">$dist");
    while(<IN>) {
	print OUT;
    }
    close(IN);
    close(OUT);
}

# �ѥ������å�
sub passCheck {
    if($inputPass eq $masterpassword) {
	return 1;
    } else {
	print <<END;
   <FONT SIZE=7>�ѥ���ɤ��㤤�ޤ���</FONT>
END
        return 0;
    }
}

1;
