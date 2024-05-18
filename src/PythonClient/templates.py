
template = """Машинист поезда №2120  на 5-м пути станции К». 
Слушаю Вас, машинист поезда №2120 Иванов.
Приказ №1 время 1:30 (один час, тридцать минут). Разрешаю поезду №2120 отправиться
с 5-го пути по четному главному пути при запрещающем показании выходного светофора Ч5 и следовать до выхода на перегон со скоростью 20 км/час, а далее руководствоваться сигналами локомотивного светофора. 
ДСП Петрова.
Понятно.
Приказ №1 :30 (один час, тридцать минут). Разрешаете поезду №2120 отправиться с 5-го пути по четному главному пути при запрещающем показании выходного светофораЧ5 и следовать до выхода на перегон со скоростью 20 км/час, а далее руководствоваться сигналами локомотивного светофора. 
Машинист поезда №2120 Иванов.
 Верно, выполняйте 
"""

template2 = """Машинист поезда №2120на приближении к станции К.
Слушаю Вас, машинист поезда №2120 Иванов.
Машинист поезда 2120, следующего к станции К
По входной стрелке №2, скорость не более 40 км/час. Приказ №5 от 23.04.2024 г. (допускается сказать цифрами и словами) подписывает ПЧ Федоров.
ДСП Петрова.
Понятно.
По входной стрелке №2 скорость не более 40 км/час. Приказ № 5 от 23.04.2024 г. подписывает подписывает ПЧ Федоров.
Машинист поезда №2120 Иванов.
Верно. 
"""

template3 = """Машинист поезда №2120 на приближении к станции К». 
Слушаю Вас, машинист поезда №2120 Иванов.
Указание № 2 время  1 час 40мин. Машинисту поезда № 2120 
Я, дежурный по станции К, разрешаю Вам следовать на свободный участок занятого 6 пути при запрещающем показании входного  светофора Ч.  Маршрут приема готов. Участок приема от выходного светофора  Н6 свободен на 20 вагонов. 
ДСП Петрова
Понятно.
Указание № 2время 1 час 40минут. Разрешаете следовать на свободный участок занятого 6 пути при запрещающем показании входного  светофора Ч.  Маршрут приема готов. Участок приема от выходного светофора  Н6 свободен на 20 вагонов. 
Машинист поезда № 2120 Иванов.
 Верно выполняйте. 

"""

template4 = """«Составитель Иванов, машинист 34.
Довожу план маневровой работы. С 1 пути 10 вагонов переставьте со стороны нечетной горловины на 2 путь и объедините с 15 вагонами. Вытягиваться будем по направлению четного пути с выездом за светофор М5
ДСП  Петрова
«Понятно. По плану маневровой работы будем с 1 пути 10 вагонов переставлять со стороны нечетной горловины на 2 путь и объединять с 15 вагонами. Вытягиваться будем по направлению четного пути с выездом за светофор М5
Составитель  Сидоров.
«Понятно. По плану маневровой работы будем с 1 пути 10 вагонов переставлять со стороны нечетной горловины на 2 путь и объединять с 15 вагонами. Вытягиваться будем по направлению четного пути  с выездом за светофор М5
Машинист 34».
«Верно».
"""


template5 = """«Машинист 34, составитель Сидоров.
Открываю Вам светофор М1 до М9 запрещающего.  
ДСП Петрова».
«Понятно, светофор М1 открываете до М9 запрещающего.  
Составитель Сидоров».
«Верно. ДСП Петрова».
Открывает светофор М1 до М9.
«Машинист 34, поехали вперед до М9 запрещающего. М1 белый, я на подножке справа (слева, на площадке, в тамбуре, иду пешком справа по ходу и т.д.)».
«Понятно, еду вперед до М9 запрещающего. М1 белый».
«Машинист 34, остановка».
"""


template6 = """«Составитель Сидоров. Машинист 34.
На 5 пути прекратите маневры, на 6 путь принимаю поезд. ДСП Петрова».
«Машинист 34, остановка».
«Дежурный, на 5 пути маневры прекращены, стоим. Составитель Сидоров».
«Дежурный, на 5 пути маневры прекращены, стоим. Машинист 34».
"""

template7 = """«Машинист 34.
Довожу план маневровой работы. С 1 пути  будем переезжать через нечетную горловину на 4 свободный (занятый) путь. Вытягиваться будем по направлению нечетного пути с выездом за светофор М1.
ДСП Сидорова.»
«Понятно. По плану маневровой работы. С 1 пути  будем переезжать через нечетную горловину на 4 свободный (занятый) путь. Вытягиваться будем по направлению нечетного пути  с выездом за светофор М1.
Машинист 34 ».
«Верно.»
"""


TMP = [template, template2,template3, template4, template5, template6, template7]