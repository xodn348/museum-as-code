from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from pipeline.config import NATIONAL_TREASURES_DIR
from pipeline.hgl_generator import HglGenerator

_FALLBACK_ARTIFACTS: list[dict] = [
    {"ccbaMnm1": "흥인지문", "ccbaMnm2": "Heunginjimun Gate", "ccbaKdcd": "11", "ccbaAsno": "0001", "ccbsChrcd": "조선시대", "ccmiName": "석재, 목재", "ccmaName": "서울특별시 종로구", "ccbaClas": "유적건조물", "ccbaCncl": "조선 태조 4년(1395)에 한양 도성 동쪽에 세운 처량으로, 홍희문이라고도 한다.", "ccbaImage": "/images/relic/11/0001.jpg", "ccbaSize": "정면 5칸, 측면 2칸"},
    {"ccbaMnm1": "원각사지십층석탑", "ccbaMnm2": "Wongaksa Temple Ten-Story Stone Pagoda", "ccbaKdcd": "11", "ccbaAsno": "0002", "ccbsChrcd": "통일신라시대", "ccmiName": "화강석", "ccmaName": "서울특별시 종로구", "ccbaClas": "불교시설", "ccbaCncl": "통일신라 시대인 광개토왕 2년(497)에 원각사지에 세운 십층석탑으로, 육각형 기단에 십층의 살이 올라간다.", "ccbaImage": "/images/relic/11/0002.jpg", "ccbaSize": "높이 8.26m"},
    {"ccbaMnm1": "서울 숭례문", "ccbaMnm2": "Seoul Sungnyemun Gate", "ccbaKdcd": "11", "ccbaAsno": "0001", "ccbsChrcd": "조선시대", "ccmiName": "목재, 벽돌", "ccmaName": "서울특별시 중구", "ccbaClas": "유적건조물", "ccbaCncl": "조선 태조 3년(1394)에 한양 도성 남쪽에 세운 처량으로, 이녕문이라고도 한다.", "ccbaImage": "/images/relic/11/0004.jpg", "ccbaSize": "정면 5칸, 측면 2칸"},
    {"ccbaMnm1": "감은사지동종", "ccbaMnm2": "Gaeunsa Temple Bronze Bell", "ccbaKdcd": "11", "ccbaAsno": "0005", "ccbsChrcd": "통일신라시대", "ccmiName": "청동", "ccmaName": "경상북도 경주시", "ccbaClas": "금속류", "ccbaCncl": "통일신라 시대인 효공왕 8년(771)에 감은사지에铸造된 거대한 금속으로, 한국에서 가장 큰 종 중 하나이다.", "ccbaImage": "/images/relic/11/0005.jpg", "ccbaSize": "높이 3.42m, 지름 2.28m"},
    {"ccbaMnm1": "부석사소조석가여래좌상", "ccbaMnm2": "Buseoksa Temple Stone Buddha", "ccbaKdcd": "11", "ccbaAsno": "0006", "ccbsChrcd": "통일신라시대", "ccmiName": "화강암", "ccmaName": "충청북도 증평군", "ccbaClas": "불교 조각", "ccbaCncl": "통일신라 말기인 9세기에 부석사지에 세운 것으로, 통일신라 불교 조각의 거대한 규모를 대표한다.", "ccbaImage": "/images/relic/11/0006.jpg", "ccbaSize": "높이 10.74m"},
    {"ccbaMnm1": "浮石寺石탑", "ccbaMnm2": "Buksisa Temple Stone Pagoda", "ccbaKdcd": "11", "ccbaAsno": "0007", "ccbsChrcd": "통일신라시대", "ccmiName": "화강암", "ccmaName": "경상북도 영주시", "ccbaClas": "불교시설", "ccbaCncl": "통일신라 시대에 축조된 무석사지의 석탑으로, 자연석을 그대로 이용하여 통일신라 특유의 자연주의적 석재 조형 양식을 잘 보여준다.", "ccbaImage": "/images/relic/11/0007.jpg", "ccbaSize": "높이 8.23m"},
    {"ccbaMnm1": "흥덕사지현존이층석탑", "ccbaMnm2": "Heungdeoksa Temple Two-Story Stone Pagoda", "ccbaKdcd": "11", "ccbaAsno": "0008", "ccbsChrcd": "통일신라시대", "ccmiName": "화강석", "ccmaName": "충청북도 제천시", "ccbaClas": "불교시설", "ccbaCncl": "통일신라 시대인 9세기에 흥덕사지에 세운 이층석탑으로, 상층과 하층이 하나의 돌로 이루어진 단일석탑이다.", "ccbaImage": "/images/relic/11/0008.jpg", "ccbaSize": "높이 5.7m"},
    {"ccbaMnm1": "흥왕사지칠층석탑", "ccbaMnm2": "Heungwangsa Temple Seven-Story Stone Pagoda", "ccbaKdcd": "11", "ccbaAsno": "0009", "ccbsChrcd": "통일신라시대", "ccmiName": "화강석", "ccmaName": "경상북도 경주시", "ccbaClas": "불교시설", "ccbaCncl": "통일신라 시대 흥왕사지에 세운 칠층석탑으로, 기단에서부터 일곱 층의 살이 올라가는 전통 양식이다.", "ccbaImage": "/images/relic/11/0009.jpg", "ccbaSize": "높이 6.6m"},
    {"ccbaMnm1": "정림사지오층석탑", "ccbaMnm2": "Jeongnimsaji Temple Five-Story Stone Pagoda", "ccbaKdcd": "11", "ccbaAsno": "0010", "ccbsChrcd": "통일신라시대", "ccmiName": "화강석", "ccmaName": "경상북도 달성군", "ccbaClas": "불교시설", "ccbaCncl": "통일신라 시대 정림사지의 오층석탑으로, 명확한 비늘각와와 장식적 기둥이 특징이다.", "ccbaImage": "/images/relic/11/0010.jpg", "ccbaSize": "높이 8.18m"},
    {"ccbaMnm1": "한석塔", "ccbaMnm2": "One-Stone Pagoda", "ccbaKdcd": "11", "ccbaAsno": "0020", "ccbsChrcd": "삼국시대", "ccmiName": "화강암", "ccmaName": "충청남도 부여군", "ccbaClas": "불교시설", "ccbaCncl": "백제 시대의 한석塔로, 하나의 돌로 이루어진 독특한 형태가 특징이다.", "ccbaImage": "/images/relic/11/0020.jpg", "ccbaSize": "높이 3.8m"},
    {"ccbaMnm1": "불국사다보탑", "ccbaMnm2": "Dabotap Pagoda of Bulguksa Temple", "ccbaKdcd": "11", "ccbaAsno": "0022", "ccbsChrcd": "통일신라시대", "ccmiName": "화강암", "ccmaName": "경상북도 경주시", "ccbaClas": "불교시설", "ccbaCncl": "불국사의 다보탑으로, 통일신라 시대인 751년에 조성되었다. 꽃을 받드는 다보여래를 형상화한 것으로 세계적으로 유명하다.", "ccbaImage": "/images/relic/11/0022.jpg", "ccbaSize": "높이 10.4m"},
    {"ccbaMnm1": "불국사석가탑", "ccbaMnm2": "Seokgatap Pagoda of Bulguksa Temple", "ccbaKdcd": "11", "ccbaAsno": "0021", "ccbsChrcd": "통일신라시대", "ccmiName": "화강암", "ccmaName": "경상북도 경주시", "ccbaClas": "불교시설", "ccbaCncl": "불국사의 석가탑으로, 통일신라 시대인 751년에 조성되었다. 통일신라 석조 건축의 최고 작품으로 꼽힌다.", "ccbaImage": "/images/relic/11/0021.jpg", "ccbaSize": "높이 8.2m"},
    {"ccbaMnm1": "첨성대", "ccbaMnm2": "Cheomseongdae Observatory", "ccbaKdcd": "11", "ccbaAsno": "0031", "ccbsChrcd": "삼국시대", "ccmiName": "화강암", "ccmaName": "경상북도 경주시", "ccbaClas": "과학기술유적", "ccbaCncl": "신라 시대의 천문 관측 대대로, 세계에서 가장 오래된 천문대 중 하나이다.", "ccbaImage": "/images/relic/11/0031.jpg", "ccbaSize": "높이 9.4m"},
    {"ccbaMnm1": "팔만대장경", "ccbaMnm2": "Palman Daejanggyeong", "ccbaKdcd": "11", "ccbaAsno": "0032", "ccbsChrcd": "고려시대", "ccmiName": "목판", "ccmaName": "경상남도 합천군", "ccbaClas": "전적류", "ccbaCncl": "고려 광종 13년(962)에 시작하여 숙종 3년(1098)에 완성된 팔만대장경의 목판으로, 총 81,258매의 목판이 있다.", "ccbaImage": "/images/relic/11/0032.jpg", "ccbaSize": "가로 69.5cm, 세로 23.8cm"},
    {"ccbaMnm1": "신라금관", "ccbaMnm2": "Silla Gold Crown", "ccbaKdcd": "11", "ccbaAsno": "0087", "ccbsChrcd": "삼국시대", "ccmiName": "금", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "경주 금관총에서 출토된 금관으로, 순금 박판을 가공하여 만든 원형의 관에 새와 십이지신 등의 장식이 달려 있다.", "ccbaImage": "/images/relic/11/0087.jpg", "ccbaSize": "높이 27.2cm"},
    {"ccbaMnm1": "금관총금관", "ccbaMnm2": "Geumgwanchong Gold Crown", "ccbaKdcd": "11", "ccbaAsno": "0088", "ccbsChrcd": "삼국시대", "ccmiName": "금", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "경주 금관총에서 출토된 금관으로, 순금 박판을 가공하여 만든 원형의 관에 새와 십이지신 등의 장식이 달려 있다.", "ccbaImage": "/images/relic/11/0088.jpg", "ccbaSize": "높이 32.7cm"},
    {"ccbaMnm1": "금동미륵보살반가사유상", "ccbaMnm2": "Gilt-bronze Maitreya Bodhisattva in Pensive Posture", "ccbaKdcd": "11", "ccbaAsno": "0078", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 조각", "ccbaCncl": "삼국시대 금동으로 제작된 미륵보살 반가사유상으로, 한 손을 턱에 괴고 사유의 자세로 앉아 있다.", "ccbaImage": "/images/relic/11/0083.jpg", "ccbaSize": "높이 93.5cm"},
    {"ccbaMnm1": "금동미륵보살반가사유상", "ccbaMnm2": "Gilt-bronze Maitreya Bodhisattva in Pensive Posture", "ccbaKdcd": "11", "ccbaAsno": "0083", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 조각", "ccbaCncl": "삼산관에서 발견된 삼국시대 금동 미륵보살 반가사유상으로, 예술성이 뛰어나다.", "ccbaImage": "/images/relic/11/0083.jpg", "ccbaSize": "높이 118.6cm"},
    {"ccbaMnm1": "금동대향로", "ccbaMnm2": "Gilt-bronze Censer", "ccbaKdcd": "11", "ccbaAsno": "0068", "ccbsChrcd": "고려시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "금속류", "ccbaCncl": "고려시대의 대표적인 금동 대향로로, 연꽃 모양의 뚜껫과 십이지신 문양이 새겨진 몸통이 정교하게 제작되었다.", "ccbaImage": "/images/relic/11/0068.jpg", "ccbaSize": "높이 36.9cm"},
    {"ccbaMnm1": "청동은입사포류수금문정병", "ccbaMnm2": "Bronze Inlaid Vessel with Grape Design", "ccbaKdcd": "11", "ccbaAsno": "0092", "ccbsChrcd": "고려시대", "ccmiName": "청동", "ccmaName": "국립중앙박물관", "ccbaClas": "금속류", "ccbaCncl": "고려시대의 청동 은입사 정병으로, 포도 문양이 정교하게 새겨져 있다. 고려 청동기의 은입사 기법을 대표하는 명작이다.", "ccbaImage": "/images/relic/11/0092.jpg", "ccbaSize": "높이 24.2cm"},
    {"ccbaMnm1": "금동용두보당", "ccbaMnm2": "Gilt-bronze Dragon Head Finial", "ccbaKdcd": "11", "ccbaAsno": "0136", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "삼국시대 금동으로 제작된 용 모양 보배로, 용의 형태가 역동적이고 생동감이 넘친다.", "ccbaImage": "/images/relic/11/0136.jpg", "ccbaSize": "높이 25.8cm"},
    {"ccbaMnm1": "칠성도", "ccbaMnm2": "Chilseongdo", "ccbaKdcd": "11", "ccbaAsno": "0080", "ccbsChrcd": "조선시대", "ccmiName": "종이, 채색, 금박", "ccmaName": "국립민속박물관", "ccbaClas": "민화", "ccbaCncl": "조선시대의 민화인 칠성도로, 칠성과칠성君을 그린 것으로 가정과 풍요를 기원하는 의미를 담고 있다.", "ccbaImage": "/images/relic/11/0080.jpg", "ccbaSize": "가로 120cm, 세로 210cm"},
    {"ccbaMnm1": "호랑이그림", "ccbaMnm2": "Tiger Painting", "ccbaKdcd": "11", "ccbaAsno": "0081", "ccbsChrcd": "조선시대", "ccmiName": "종이, 먹, 채색", "ccmaName": "국립민속박물관", "ccbaClas": "민화", "ccbaCncl": "조선시대의 호랑이 민화로, 힘찬 필치로 호랑이를 그렸다. 호랑이는 부적과 같은 의미를 지닌다.", "ccbaImage": "/images/relic/11/0081.jpg", "ccbaSize": "가로 150cm, 세로 80cm"},
    {"ccbaMnm1": "용왕상", "ccbaMnm2": "Dragon King Painting", "ccbaKdcd": "11", "ccbaAsno": "0082", "ccbsChrcd": "조선시대", "ccmiName": "종이, 채색", "ccmaName": "국립민속박물관", "ccbaClas": "민화", "ccbaCncl": "조선시대의 용왕상으로, 물의 신을 형상화하였다. 풍수와 물의 개념을 담아 농경 사회에서 중요시되었다.", "ccbaImage": "/images/relic/11/0082.jpg", "ccbaSize": "가로 100cm, 세로 180cm"},
    {"ccbaMnm1": "낙엽호랑이", "ccbaMnm2": "Tiger under Magnolia", "ccbaKdcd": "11", "ccbaAsno": "0079", "ccbsChrcd": "조선시대", "ccmiName": "종이, 채색", "ccmaName": "국립민속박물관", "ccbaClas": "민화", "ccbaCncl": "조선시대의 상징적 민화로, 목련 화살에 호랑이를 그렸다.", "ccbaImage": "/images/relic/11/0079.jpg", "ccbaSize": "가로 130cm, 세로 75cm"},
    {"ccbaMnm1": "금동관음보살좌상", "ccbaMnm2": "Gilt-bronze Avalokitesvara Bodhisattva Seated Statue", "ccbaKdcd": "11", "ccbaAsno": "0089", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 조각", "ccbaCncl": "삼국시대 금동으로 제작된 관음보살좌상으로, 조각이 정교하고 예술성이 높다.", "ccbaImage": "/images/relic/11/0089.jpg", "ccbaSize": "높이 71.2cm"},
    {"ccbaMnm1": "금동아미타여래좌상", "ccbaMnm2": "Gilt-bronze Amitabha Buddha Seated Statue", "ccbaKdcd": "11", "ccbaAsno": "0090", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 조각", "ccbaCncl": "삼국시대 금동으로 제작된 아미타여래좌상으로, 불교 조각의 정수이다.", "ccbaImage": "/images/relic/11/0090.jpg", "ccbaSize": "높이 117cm"},
    {"ccbaMnm1": "금동약사여래좌상", "ccbaMnm2": "Gilt-bronze Bhaisajyaguru Buddha Seated Statue", "ccbaKdcd": "11", "ccbaAsno": "0121", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 조각", "ccbaCncl": "삼국시대 금동으로 제작된 약사여래좌상으로, 한국 불교 조각의 걸작이다.", "ccbaImage": "/images/relic/11/0121.jpg", "ccbaSize": "높이 109cm"},
    {"ccbaMnm1": "금동아미타여래입상", "ccbaMnm2": "Gilt-bronze Amitabha Buddha Standing Statue", "ccbaKdcd": "11", "ccbaAsno": "0122", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 조각", "ccbaCncl": "삼국시대 금동으로 제작된 아미타여래 입상이다.", "ccbaImage": "/images/relic/11/0122.jpg", "ccbaSize": "높이 104cm"},
    {"ccbaMnm1": "신라금관", "ccbaMnm2": "Silla Gold Crown in National Museum", "ccbaKdcd": "11", "ccbaAsno": "0124", "ccbsChrcd": "삼국시대", "ccmiName": "금, 은, 유리", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "신라 시대의 금관으로, 유리 장식이 남아 있어 당시의 장신구 문화를 보여준다.", "ccbaImage": "/images/relic/11/0124.jpg", "ccbaSize": "높이 29cm"},
    {"ccbaMnm1": "마애여래삼존상", "ccbaMnm2": "Rock-carved Buddha Triad", "ccbaKdcd": "11", "ccbaAsno": "0113", "ccbsChrcd": "삼국시대", "ccmiName": "화강암", "ccmaName": "경상북도 경주시", "ccbaClas": "불교 조각", "ccbaCncl": "삼국시대 화강암에 새긴 마애여래삼존상으로, 대규모岩刻이다.", "ccbaImage": "/images/relic/11/0113.jpg", "ccbaSize": "높이 5.5m"},
    {"ccbaMnm1": "백제금동대향로", "ccbaMnm2": "Baekje Gilt-bronze Censer", "ccbaKdcd": "11", "ccbaAsno": "0287", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 신앙器材", "ccbaCncl": "백제 시대의 금동대향로로, 고도한 금속 공예 기술을 보여준다.", "ccbaImage": "/images/relic/11/0287.jpg", "ccbaSize": "높이 30cm"},
    {"ccbaMnm1": "백자병", "ccbaMnm2": "White Porcelain Bottle", "ccbaKdcd": "11", "ccbaAsno": "0069", "ccbsChrcd": "조선시대", "ccmiName": "백토", "ccmaName": "국립중앙박물관", "ccbaClas": "도자기", "ccbaCncl": "조선시대의 백자 병으로, 검은斑点이 특징적인 명작이다.", "ccbaImage": "/images/relic/11/0069.jpg", "ccbaSize": "높이 22.3cm"},
    {"ccbaMnm1": "분청사자수도완", "ccbaMnm2": "Underglaze-blue White Porcelain Bottle", "ccbaKdcd": "11", "ccbaAsno": "0067", "ccbsChrcd": "조선시대", "ccmiName": "백토, 안료", "ccmaName": "국립중앙박물관", "ccbaClas": "도자기", "ccbaCncl": "조선시대의 분청사기로, 청자색 그림자가 특징적인 독특한 작품이다.", "ccbaImage": "/images/relic/11/0067.jpg", "ccbaSize": "높이 18.2cm"},
    {"ccbaMnm1": "청자어패문항아리", "ccbaMnm2": "Celadon with Shell and Wave Design", "ccbaKdcd": "11", "ccbaAsno": "0065", "ccbsChrcd": "고려시대", "ccmiName": "청자", "ccmaName": "국립중앙박물관", "ccbaClas": "도자기", "ccbaCncl": "고려시대의 대표적인 청자로, 어패(魚貝) 문양이 정교하게 표현된 작품이다.", "ccbaImage": "/images/relic/11/0065.jpg", "ccbaSize": "높이 22.8cm"},
    {"ccbaMnm1": "청자상감학문호", "ccbaMnm2": "Celadon with Crane Design", "ccbaKdcd": "11", "ccbaAsno": "0066", "ccbsChrcd": "고려시대", "ccmiName": "청자", "ccmaName": "국립중앙박물관", "ccbaClas": "도자기", "ccbaCncl": "고려 청자의 상감 기법이 도입된 초기 작품으로, 학(鶴) 문양이 정교하게 새겨졌다.", "ccbaImage": "/images/relic/11/0066.jpg", "ccbaSize": "높이 19.8cm"},
    {"ccbaMnm1": "금은화鞋", "ccbaMnm2": "Gold and Silver Thread-woven Shoes", "ccbaKdcd": "11", "ccbaAsno": "0023", "ccbsChrcd": "고려시대", "ccmiName": "비단, 금은실", "ccmaName": "국립중앙박물관", "ccbaClas": "직물", "ccbaCncl": "고려시대의 직물로, 금은실을 사용하여 정교하게 제작되었다.", "ccbaImage": "/images/relic/11/0023.jpg", "ccbaSize": "길이 26cm"},
    {"ccbaMnm1": "금속활자", "ccbaMnm2": "Metal Movable Type", "ccbaKdcd": "11", "ccbaAsno": "0015", "ccbsChrcd": "고려시대", "ccmiName": "청동", "ccmaName": "한국국학진흥원", "ccbaClas": "전적류", "ccbaCncl": "고려 시대의 금속활자로, 세계 최고 수준의 인쇄 기술을 보여주는 유물이다.", "ccbaImage": "/images/relic/11/0015.jpg", "ccbaSize": "가로 7cm, 세로 10cm"},
    {"ccbaMnm1": "평창대관도", "ccbaMnm2": "Pyeongchang Daegwando", "ccbaKdcd": "11", "ccbaAsno": "0006", "ccbsChrcd": "조선시대", "ccmiName": "종이, 채색", "ccmaName": "한국민속박물관", "ccbaClas": "지형도", "ccbaCncl": "조선시대 강원도 평창 지역을 그린 대관도로, 역사 지리학적으로 중요하다.", "ccbaImage": "/images/relic/11/0006.jpg", "ccbaSize": "가로 180cm, 세로 380cm"},
    {"ccbaMnm1": "용두사지석등", "ccbaMnm2": "Yongdusa Temple Stone Lantern", "ccbaKdcd": "11", "ccbaAsno": "0009", "ccbsChrcd": "통일신라시대", "ccmiName": "화강암", "ccmaName": "경상북도 경주시", "ccbaClas": "불교 관련 석조물", "ccbaCncl": "신라 용두사지에서 발견된 석등으로, 통일신라 시대의 정형화된 불교 예술을 보여준다.", "ccbaImage": "/images/relic/11/0009.jpg", "ccbaSize": "높이 60cm"},
    {"ccbaMnm1": "경복사지철기", "ccbaMnm2": "Iron Pagoda of Gyeongboksa Temple", "ccbaKdcd": "11", "ccbaAsno": "0041", "ccbsChrcd": "삼국시대", "ccmiName": "철", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 관련 철조물", "ccbaCncl": "삼국시대 철기로 제작된 기둥 구조물이다.", "ccbaImage": "/images/relic/11/0041.jpg", "ccbaSize": "높이 4.2m"},
    {"ccbaMnm1": "금강문학", "ccbaMnm2": "Geumgang Seated Inscription", "ccbaKdcd": "11", "ccbaAsno": "0016", "ccbsChrcd": "고려시대", "ccmiName": "금석", "ccmaName": "국립중앙박물관", "ccbaClas": "금석문", "ccbaCncl": "금강에 새겨진 금석문으로, 고려 시대의 역사 자료이다.", "ccbaImage": "/images/relic/11/0016.jpg", "ccbaSize": "가로 50cm, 세로 80cm"},
    {"ccbaMnm1": "백제무녕왕릉석곽", "ccbaMnm2": "Baekje King Munyeong Stone Coffin", "ccbaKdcd": "11", "ccbaAsno": "0045", "ccbsChrcd": "삼국시대", "ccmiName": "화강암", "ccmaName": "국립중앙박물관", "ccbaClas": "고분 유물", "ccbaCncl": "백제 무녕왕릉에서 출토된 돌棺으로, 백제 문화의 정수를 보여준다.", "ccbaImage": "/images/relic/11/0045.jpg", "ccbaSize": "가로 3m, 세로 2m"},
    {"ccbaMnm1": "동아시아서예발파도", "ccbaMnm2": "East Asian Calligraphy Diagram", "ccbaKdcd": "11", "ccbaAsno": "0132", "ccbsChrcd": "조선시대", "ccmiName": "종이, 먹", "ccmaName": "국립중앙박물관", "ccbaClas": "서예", "ccbaCncl": "조선시대 서예 발파도로, 동아시아 서예의 특징을 보여준다.", "ccbaImage": "/images/relic/11/0132.jpg", "ccbaSize": "가로 100cm, 세로 200cm"},
    {"ccbaMnm1": "조선왕조실록", "ccbaMnm2": "Annals of the Joseon Dynasty", "ccbaKdcd": "11", "ccbaAsno": "0131", "ccbsChrcd": "조선시대", "ccmiName": "종이, 먹", "ccmaName": "국립중앙박물관", "ccbaClas": "전적류", "ccbaCncl": "조선시대의 역대 왕의 실록으로, 약 900년간의 한국 역사를 기록한 세계 최대의 사서이다.", "ccbaImage": "/images/relic/11/0131.jpg", "ccbaSize": "가로 30.5cm, 세로 21cm"},
    {"ccbaMnm1": "고려사찰壁画", "ccbaMnm2": "Goryeo Temple Mural", "ccbaKdcd": "11", "ccbaAsno": "0061", "ccbsChrcd": "고려시대", "ccmiName": "석회, 안료", "ccmaName": "국립중앙박물관", "ccbaClas": "회화", "ccbaCncl": "고려 사찰 벽화로, 당시의 생활과 신앙을 보여준다.", "ccbaImage": "/images/relic/11/0061.jpg", "ccbaSize": "가로 250cm, 세로 200cm"},
    {"ccbaMnm1": "금동보살머리장식", "ccbaMnm2": "Gilt-bronze Bodhisattva Hair Ornament", "ccbaKdcd": "11", "ccbaAsno": "0091", "ccbsChrcd": "삼국시대", "ccmiName": "금동", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "삼국시대 보살상 장신구로, 머리카락 모양의 세공이 특징적이다.", "ccbaImage": "/images/relic/11/0091.jpg", "ccbaSize": "길이 35cm"},
    {"ccbaMnm1": "신라인서", "ccbaMnm2": "Silla Royal Sutra", "ccbaKdcd": "11", "ccbaAsno": "0030", "ccbsChrcd": "삼국시대", "ccmiName": "금박, 종이", "ccmaName": "국립중앙박물관", "ccbaClas": "전적류", "ccbaCncl": "신라 왕실에서 사용한 경전으로, 금박 입사 기법이 사용되었다.", "ccbaImage": "/images/relic/11/0030.jpg", "ccbaSize": "가로 6.5cm, 세로 50cm"},
    {"ccbaMnm1": "고려명종명성왕후묘지", "ccbaMnm2": "Goryeo Queen Myeongseong Epitaph", "ccbaKdcd": "11", "ccbaAsno": "0129", "ccbsChrcd": "고려시대", "ccmiName": "화강암", "ccmaName": "국립중앙박물관", "ccbaClas": "비문", "ccbaCncl": "고려 명종 명성 왕후의 묘지로, 고려 시대의 역사 자료이다.", "ccbaImage": "/images/relic/11/0129.jpg", "ccbaSize": "가로 70cm, 세로 100cm"},
    {"ccbaMnm1": "평산토기", "ccbaMnm2": "Pyeongsan Earthenware", "ccbaKdcd": "11", "ccbaAsno": "0037", "ccbsChrcd": "삼국시대", "ccmiName": "토기", "ccmaName": "국립중앙박물관", "ccbaClas": "토기", "ccbaCncl": "삼국시대 토기로, 평산 지역에서 출토되었다.", "ccbaImage": "/images/relic/11/0037.jpg", "ccbaSize": "높이 30cm"},
    {"ccbaMnm1": "남기고분금관", "ccbaMnm2": "Gold Crown from Namsan Tomb", "ccbaKdcd": "11", "ccbaAsno": "0086", "ccbsChrcd": "삼국시대", "ccmiName": "금, 은", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "남산 고분에서 출토된 금관으로, 신라 왕실의 유물이다.", "ccbaImage": "/images/relic/11/0086.jpg", "ccbaSize": "높이 31cm"},
    {"ccbaMnm1": "가야금관", "ccbaMnm2": "Gaya Gold Crown", "ccbaKdcd": "11", "ccbaAsno": "0085", "ccbsChrcd": "삼국시대", "ccmiName": "금", "ccmaName": "국립중앙박물관", "ccbaClas": "금속공예", "ccbaCncl": "가야 왕국의 금관으로, 남아시아와의文化交流를 보여준다.", "ccbaImage": "/images/relic/11/0085.jpg", "ccbaSize": "높이 18cm"},
    {"ccbaMnm1": "황토기기", "ccbaMnm2": "Yellow Earthenware", "ccbaKdcd": "11", "ccbaAsno": "0038", "ccbsChrcd": "삼국시대", "ccmiName": "토기", "ccmaName": "국립중앙박물관", "ccbaClas": "토기", "ccbaCncl": "삼국시대 토기로, 황토색 유약이 특징적이다.", "ccbaImage": "/images/relic/11/0038.jpg", "ccbaSize": "높이 25cm"},
    {"ccbaMnm1": "신라연화문비단", "ccbaMnm2": "Silla Lotus Pattern Brocade", "ccbaKdcd": "11", "ccbaAsno": "0033", "ccbsChrcd": "삼국시대", "ccmiName": "비단", "ccmaName": "국립중앙박물관", "ccbaClas": "직물", "ccbaCncl": "신라 시대 비단직물로, 연화문이 정교하게 표현되었다.", "ccbaImage": "/images/relic/11/0033.jpg", "ccbaSize": "가로 45cm, 세로 120cm"},
    {"ccbaMnm1": "궁예릉", "ccbaMnm2": "King Gungye Tomb", "ccbaKdcd": "11", "ccbaAsno": "0197", "ccbsChrcd": "고려시대", "ccmiName": "돌, 벽돌", "ccmaName": "황해도 봉산군", "ccbaClas": "고분", "ccbaCncl": "후고구려의 왕 궁예의 능묘로, 고려 건국과 관련된 역사적 유적이다.", "ccbaImage": "/images/relic/11/0197.jpg", "ccbaSize": "직경 약 47m"},
    {"ccbaMnm1": "금책", "ccbaMnm2": "Golden Investiture Record", "ccbaKdcd": "11", "ccbaAsno": "0071", "ccbsChrcd": "고려시대", "ccmiName": "금", "ccmaName": "국립중앙박물관", "ccbaClas": "금속류", "ccbaCncl": "고려 현종 2년(1011)에 대방군 왕인에게 내린 금책으로, 고려 왕조의 왕위 계승과 왕실의 위엄을 증명하는 중요한 역사 자료이다.", "ccbaImage": "/images/relic/11/0071.jpg", "ccbaSize": "가로 21cm, 세로 45cm"},
    {"ccbaMnm1": "아미타쌍상도", "ccbaMnm2": "Amitabha Twin Statues Painting", "ccbaKdcd": "11", "ccbaAsno": "0531", "ccbsChrcd": "고려시대", "ccmiName": "석채, 금박, 견죽", "ccmaName": "국립중앙박물관", "ccbaClas": "불교 화", "ccbaCncl": "고려시대의 아미타쌍상도로, 아미타如来来往坐着自己的 쌍상을 그린 불화이다.", "ccbaImage": "/images/relic/11/0531.jpg", "ccbaSize": "가로 150cm, 세로 195cm"},
]

HAN_BINARY = Path("/Users/jnnj92/han/target/debug/hgl")


def _run_hgl_check(path: Path) -> bool:
    result = subprocess.run(
        [str(HAN_BINARY), "check", str(path)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate .hgl + .json artifact pairs")
    parser.add_argument("--fallback", action="store_true", help="Generate from built-in fallback data")
    parser.add_argument("--resume", action="store_true", help="Skip existing artifacts")
    args = parser.parse_args()

    if not args.fallback:
        parser.print_help()
        print("\nError: --fallback flag is required (no API key available).")
        sys.exit(1)

    generator = HglGenerator()
    NATIONAL_TREASURES_DIR.mkdir(parents=True, exist_ok=True)

    existing: set[str] = set()
    if args.resume:
        for f in NATIONAL_TREASURES_DIR.glob("nb_*.hgl"):
            existing.add(f.stem)
        print(f"Resume mode: {len(existing)} existing artifact(s) found, will skip.")

    total = 0
    passed = 0
    failed_ids: list[str] = []

    for i, artifact in enumerate(_FALLBACK_ARTIFACTS, 1):
        nb_id = f"nb_{i:03d}"
        if args.resume and nb_id in existing:
            continue

        hgl_content, json_content = generator.generate(artifact)
        hgl_path = NATIONAL_TREASURES_DIR / f"{nb_id}.hgl"
        json_path = NATIONAL_TREASURES_DIR / f"{nb_id}.json"

        hgl_path.write_text(hgl_content, encoding="utf-8")
        json_path.write_text(json_content, encoding="utf-8")
        total += 1

        ok = _run_hgl_check(hgl_path)
        if ok:
            print(f"  PASS {nb_id}: {artifact['ccbaMnm1']} ({artifact['ccbaAsno']})")
            passed += 1
        else:
            print(f"  FAIL {nb_id}: {artifact['ccbaMnm1']} ({artifact['ccbaAsno']})")
            failed_ids.append(nb_id)

    print(f"\n=== Summary: {passed}/{total} .hgl files pass hgl check ===")
    if failed_ids:
        print(f"Failed: {', '.join(failed_ids)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
