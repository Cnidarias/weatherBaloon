// What am I doing with my life?
#include <Arduino.h>

#include "config.h"
#include "afsk_avr.h"
#include "afsk_pic32.h"
#include "aprs.h"


void getSerialData();

unsigned long last_sent = 0;
const unsigned long APRS_WAIT = 10000L;

unsigned long last_request = 0;
const unsigned long REQUEST_WAIT = 5000L;

const byte buffer_size = 255;
char buffer[buffer_size];

const char * funk_ready = "FUNK READY";
bool recv_packet = false;

const char * strs[]= {
  "/175722h5021.41N/0735.34EO/A=65.61\0",
  "{0_1_GLGgjCYr7Ky!M5d/GB5Od&g/t.Z%Qy/9MmKucKG7j10>`7nCSy=|vs$qA}_Bz5x!<IacYjzlc?5dw{wXh1l[1v4|G>lnK[Go[|ECdb@+8!u=5tG>J4wCb?XB5]F7i3Xlt+I;11.Oa|,IaX7MM06NMQHFPp7JRVb4!SC8%P3)Wvak:#]L7%;=[])I)<q(lw87ICZL!U/@q)PEAqlJYYU%+2Z+YIS!y}E4(!0c@j5JX;%@vSc$c5xZ7gzrR$.}\0",
  //"{0_0_d+sW4Acc!cnx5FQAAABAEABtin.hIA3nHj2K,W2Z$Y@!FH8_7PRVc%/.U!!06!.AMlWZ1RIGv#}KN7*#H8$Y%~qf\"^]~B\"!T7}B\"~]*>Z~d+tWwA5WuWYBDHRtIAKcNtMA@QRtlBAAAAAAAAAAAAAA6Fa\"*BFO0WjLXLhtUE[hFBIO{WAAAAAAS\"|LdL;y[FKOGM[wU*XjqI6DZYgSUSTz71w)@9NA&ABA+>J\"_zqNx2Ezze0D$[]iBMR$v\0",
  //"{0_2_8b%d+0K:n}?*S:V=3((L,o$:${4[J56SUj@N4`>x/2Vnn>qq&wc&R29H]=FTRb#;b/~RCUT_%H&b/\"ojU#h@JBc,jzUvIAi%2+FYMeNf[BPDl2jzlD3HGP}nc,eX=zak$8Hp\"[dF!Ly~(]iyZ2$Rh9c>~%%rIK(:q@MN#wK``|>i;K&rZy.6)lq}I`@NZJozR2<i:f??A>i@3G8uOTNjoem]e))0[073|,Yk$+&*GS]CkU(by2`wLCX0=a9\0",
  //"{0_3_ZH)/z$cZGufsTP1e!DmCecR;)+<S;,br,~C>l}j>Kd2ok_eE.XbHS5vI=IV;:CiR2:pG`Bzd=?d`{K;Y8q!wxIEPmDkMS<FtoUNtBFX!HfE4\"gS~j0SY/DmPUpPym?0P^Z6A>4e|ZKE/9{a+1GT);<$HguwFPdEWq&!vXD3,M{0k5|fo`$i|z.rIzlLa.w+mazDWcIEQA[9)dAbhp_{N3+!Vew^7&JH`Saqo^`0~3.;C<ep.f$!*N<dyjW*\0",
  //"{0_4_F2%xJq>L;HE)J$\"c}wfxJL8eMh{:Hy^Z;%kzOCPOs4*BFAoIgc&Go^?jr)[E}cA:b6PON%8LV^|j}]F^3mqM\"m!]_&63BzH#xf[IF#A{HjEz`2LKfOS*5wvWwDWcgY9MAA:abY=1Rz3G}w&&K|_E/f931fgAZzGeOUnw&<|bXMXM)9`auIu<P,0pn!}PFN5,jg]OG7/JzWC\"[tCARA95AY4O4L8;Y@bph%7GRDiiwJ66i]7]N[oS7&QU,!t\0",
  //"{0_5_9LTp4y+Av|P%5?iWn_Td?L>.gEGC##(@Q:C.\"vWQOGw@cBMuVI?Ket2)x\"T&V/\"n6Vy0{8cr~DEI*{5!CC.Ggu<ruG1M.aIB>5IPR|2LlKx#ri;^~`+AAVE44(yvWmORfLzF5M~^|`?NML4*)L~A5`Z5z24T}?i!qt}5px5cV[n&Zh{7n3x,W7d]{9H*s`cYz_%OlI4K+,.r!yv^wETWA,,:ESA/Yp7[f~Rc3_sB}r[eM`CG*[V&x[0z|to\0",
  //"{0_6_Qo1^}j^~A}P!;SlSYk`|7`&j15UM|R.ZzhVC!&ip):4{3@c0^*zS1^o:5YM!gw=0OCdx/NPM[+~,+{k^*\"*GmYaxGa1TBQsY4=##U@\"219B~Z99zF85?lvT%I1?,AED$(ZygJzMxgX=zv%9gch(K$a~7C3~|4FUUY9@J2=MecgT#bJ=@kCT<Q`dhYZ<uwdaZw/*=%h2/M,ow/+_])2Fz_nH5[rz&xpl1^HD|iW}XF#%I0*\"$TGg`__pr0SN\0",
  //"{0_7_v~x[joI/*G2Ro)o)d5ujMo^w?|)d3;,(+ri,,@OL4j$]wd.86v@4SOQihPo=1aG&*702J\"!sb<mQmK()mZ`W8vo3w:4wfL>|]5rh0c?x02d#P2|&VE1,EkNUZd?#[uf,dVbI>:rc;y$@1NqrWQ.2THN^Z%>;9}YFnL}T{bU]wh#|6W~hYk]Xb:[yxg6@R=Uk+XhLZ?:3Zh}tfH{>M|CDt=T$qy]bQUU,[psa#C%)D`l5rYf>0RZkaA;BFv_\0",
  //"{0_8_k]4%LI9LFT`ZCd55M|vRg,O;p{XrsO^P;ba[6O}NEK0!T+D`F}_(ShHzFVbp!)%6/$>TTJ}#vw[^>L;eN%=tfGq5e*)xh=rmVQLV;ZvDQAO2I|tr)}EtYyuhdjI^i3!3yd2)L@2i+<TdxC#Yu0Cp(m;@F9:t>tbM#srO2T_x`o\"cqjv~=d}MP3+)e`B|!nN:|F!o=Os<NNek*SO=daq8}Yk4~`r9F3`:NR<a=#=@kN%/]t)\"XLsAAAKC%0V\0",
  //"{0_9__WW7=$7cNEO&nH:SHx@*KeHJECFS1~o0|\"o,7jk5QAT>:mse>w+A(gyJe<YtzP[zFd.yVL:}e6e@S?Rypm^zuehEo8,;Kzj$q0=~atR.k3g(xjHD_Y/Pe#RbuDR3$8sCc_eZxcYLO&\"cX?DbCC\"uWh]4atq_u{~[QN;!_N`gjg)dwyNK{|%~i#glq9>U]#j(Z0r[Lpbf=fz6e[5/p:Zi|y,<$2Q,@}qJ]uP67fy??C+NlZ#A55Jlg|4AC>$\0",
  //"{0_10_y*7N7@p{/OIhw}{v+09>:V,:e0;T+~:CGHx72iTNfLsAUE$4Ny39T@4uef^T7_4B,YAn!wj1t.Lja$NEbGh;elK9kP}nyrKsOV=f1T!X/zWo@hQ,6JpdJ5^&NOA;236@`i`/&I>cjV#ZTlqQ=QM+EhTq:*lIh!^IY+p(_d4L>SHMojEX/hoX0EzO5S(?qeEIhy{V%p*q{~vWb6[i&{hJs(@ZZ,r5z+N$>%M}*T)7a7oX]7cUnmcImoM6W[\0",
  //"{0_11_jxR=)K`{f)&NI662]U3*_MM[~[Zj>KKt~J{5suNJUrDMN.&z{I=Y:!Oo#)SLny#lz8U,^SQB==br%~2~Gs}Lo2~F[0BY#MoUG:V|{VG{l2orMQm#G_IG?~Et][SV+j[iI}GsU,bE9(=#V8*o<K`?7+.N2{4?@*}byfz;we8.2F0IW,a<KN_+my,b:X<lQ||eksBHj@{XZYDz6wXE$ZY3=TV/DKm{s[$Dmg{LpPBxs}DeFrD&JN\"sSqtjCY\0",
  //"{0_12_mKAGW1AYcNit?`tPus(@0^qz.<c!e[zus9z:p,fmhEd>X6YQGR3p6[eWiomv]/2ft:2B7aRQ(@Ie73Uf^Xq7FdSih*kHru*)*S[|p7/vi$1{5=Y2]!2XbhWap=6xaJ[0BYdiv/#B1kFdnuRgh$OJ;zgyl=$QPS96#B2DWcZ`{1<wB!gHzailtz~Y!@jz!pBYbvnR:5#*@cXkWwA2|tby>bURhk0vY1Bl2%;D.Va2>#XkHnXjmKAGUbCwp,\0",
  //"{0_13_0wEb/Z,Fs4*BtIB1<NzUZO5e\",#A2\"#!;cuCtWfz3Tm#G2_z>+D6TaC\"}v47X,IM:RS^gM@;By,*<(shfhV!YhEJF24S./u3++(zIT2P2gH/a#B__END\0"
};

bool test_strings = true;

void setup()
{
  Serial.begin(9600);
  afsk_setup();
}

void loop()
{
  if (test_strings) {
    int i = 0;
    for (; i < 2; i++)  {
      aprs_send(strs[i]);
      Serial.println(strs[i]);
      while (afsk_flush()) {}
      delay(15000);
    }
    delay(15000);
  }
  else {
    if (recv_packet) {
      last_sent = millis();
      aprs_send(buffer);
      while (afsk_flush()) {
      }
      recv_packet = false;
    }
    else {
      if (millis() - last_sent > APRS_WAIT) {
        if (millis() - last_request > REQUEST_WAIT) {
          Serial.println(funk_ready);
          last_request = millis();
        }
        getSerialData();
      }
    }
  }
}


void getSerialData()
{
  static byte ndx = 0;
  char rc;
  while (Serial.available() > 0) {
    rc = Serial.read();
    if (rc != '\n') {
      buffer[ndx++] = rc;
      if (ndx >= buffer_size) {
        ndx = buffer_size - 1;
      }
    } else {
      buffer[ndx] = '\0'; // terminate the string
      ndx = 0;
      recv_packet = true;
    }
  }
}
