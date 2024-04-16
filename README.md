# Пятая лабораторная работа по программированию 
## Суть задания: создать клиент-сервер с шифрованием, который: 
1. При запуске клиент и сервер генерируют каждый свою пару ключей.
2. При подключении клиент посылает серверу свой открытый ключ.
3. В ответ, сервер посылает клиенту открытый ключ сервера.
4. Клиент посылает сообщение серверу, шифруя его своим закрытым ключом и открытым ключом сервера.
5. Сервер принимает сообщение, расшифровывает его сначала своим закрытым ключом, а потом - открытым ключом клиента.
6. Обратное сообщение посылается аналогично.

## Дополнительные задания:
1. Модифицируйте код клиента и сервера так, чтобы приватный и публичный ключ хранились в текстовых файлах на диске и, таким образом, переиспользовались между запусками. (100% done)
2. Проведите рефакторинг кода клиента и сервера так, чтобы все, относящееся к генерации ключей, установлению режима шифрования, шифрованию исходящих и дешифрованию входящих сообщений было отделено от основного алгоритма обмена сообщениями. (75% done)
3. Модифицируйте код клиента и сервера таким образом, чтобы установление режима шифрования происходило при подключении на один порт, а основное общение - на другом порту. Номер порта можно передавать как первое зашифрованное сообщение. (100% done)
