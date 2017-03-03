# Tetris

##Utworzony w Pythonie 3.5.2
###PyCharm

Cel projektu:
Celem projektu jest zaliczenie przedmiotu jakim jest Programowanie Gier. Gra zostanie wykonana w języku Python w wersji 3.5.2 w środowisku programistycznym PyCharm. 

Opis gry:
Gra rozpoczyna się na prostokątnej planszy początkowo, ułożonej krótszym bokiem w poziomie. W trakcie gry, pośrodku górnej krawędzi planszy, pojawiają się pojedynczo klocki złożone z czterech małych kwadratów nazywanych też blokami. Klocki te przemieszczają się w kierunku dolnej krawędzi w miarę możliwości. Kiedy jedno klocek opadnie na samo dno, zostaje unieruchomiony, a następne ukazuje się u góry planszy. Gra trwa aż do momentu, w którym klocek nie będzie mógł pojawić się na planszy. Zadaniem gracza jest układanie bloków na planszy (poprzez wykorzystanie rotacji i przesuwanie klocków w poziomie) w taki sposób, aby kwadraty składające się na nie utworzyły wiersz na całej szerokości prostokąta. W takiej sytuacji wiersz ten zostaje usunięty, a pozostałe klocki opadają w kierunku dna, tworząc więcej przestrzeni dla następnych elementów. Możliwe jest jednoczesne usunięcie maksymalnie 4 wierszy. Sytuacja taka nosi nazwę identyczną jak gra, czyli „tetris”.
Na zestaw klocków składa się siedem różnych klocków złożonych z kwadratowych elementów:
 
Tetrimino „I” – cztery elementy w jednym szeregu;
Tetrimino „T” – trzy elementy w rzędzie i jeden dołączony do środkowego elementu;
Tetrimino „O” – cztery elementy połączone w kwadrat;
Tetrimino „L” – trzy elementy w rzędzie i jeden dołączony do lewego elementu od spodu;
Tetrimino „J” – trzy elementy w rzędzie i jeden dołączony do prawego elementu od spodu;
Tetrimino „S” – tetrimino „O” po przesunięciu dwóch górnych elementów w prawo;
Tetrimino „Z” – tetrimino „O” po przesunięciu dwóch górnych elementów w lewo.
Pary „L” i „J” oraz „S” i „Z” przedstawiają lustrzane odbicia, jednak nie można poprzez obrót jednego utworzyć drugiego.

