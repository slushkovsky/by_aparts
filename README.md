# Поиск квартир на onliner.by
Парсер позволяет найти квартиру на onliner.by, используя более глубокие фильтры (например - без мебели)  
  
Алгоритм работы:  
Делается запрос на API (с фильтрами onliner'а) -> получается список всех страниц объявлений -> страницы обходятся и при сходстве по параметрам добавляются в список true_aparts, который в конце выводится в консоль

## Использование
Найти 1,2 комнатные квартиры от $420 до $1000 без мебели от собственника (этот фильтр включен по умолчанию в коде):  
`python3.6 parser.py 420 1000 1 2 --without-opts Мебель`

## Минорные моменты
Написано на python3.6
